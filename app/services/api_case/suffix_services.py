# coding=utf-8
"""
File: suffix_services.py
Author: bot
Created: 2023/9/14
Description:
"""
import asyncio
from typing import List, Union

from app.crud.api_case.suffix_crud import SuffixCrud
from app.crud.cconfig.cconfig_crud import CommonConfigCrud
from app.exceptions.cconfig_exp import SQL_NOT_EXISTS
from app.exceptions.commom_exception import CustomException
from app.handler.db_handler import DataBaseConnect
from app.handler.new_redis_handler import redis_client
from app.handler.script_handler import ScriptHandler
from app.models.api_settings.suffix_settings import SuffixModel
from app.schemas.api_case.api_case_schemas import OrmFullCase, Orm2CaseSuffix
from app.schemas.api_settings.suffix_schema import SchemaCaseSuffix
from app.utils.time_utils import TimeUtils


class NewSuffixServices:
    def __init__(self, env_id: int, user_id: int, case_id: int = None):
        self.env_id = env_id
        self.case_id = case_id
        self.user_id = user_id
        self.g_var = dict()
        self.log = dict(
            env_prefix=[],
            case_prefix=[],
            case_suffix=[],
            env_suffix=[],
        )

    @staticmethod
    async def get_prefix(
        env_id: int = None, case_id: int = None, temp: List[SchemaCaseSuffix] = None
    ) -> List[Union[SuffixModel, SchemaCaseSuffix]]:
        if env_id is not None or case_id is not None:
            prefix_info = await SuffixCrud.get_prefix(env_id, case_id)
        else:
            prefix_info = temp
        return prefix_info

    @staticmethod
    async def get_suffix(
        env_id: int = None, case_id: int = None, temp: List[SchemaCaseSuffix] = None
    ) -> List[Union[SuffixModel, SchemaCaseSuffix]]:
        if env_id is not None or case_id is not None:
            suffix_info = await SuffixCrud.get_suffix(env_id, case_id)
        else:
            suffix_info = temp
        return suffix_info

    async def execute_method_delay(self, delay: int, log_type: str):
        """执行延迟"""
        await asyncio.sleep(delay / 1000)
        t = TimeUtils.get_current_time_without_year()
        self.log[log_type].append(f"[{t}]: [延迟执行] -> {delay}ms")

    async def execute_method_sql(self, sql_id: int, run_command: str, log_type: str, run_out_name: str = None):
        """执行SQL语句"""
        sql_info = await CommonConfigCrud.query_sql_detail(sql_id)
        if not sql_info:
            raise CustomException(SQL_NOT_EXISTS)
        c = await DataBaseConnect.mysql_connection(
            host=sql_info.host,
            port=sql_info.port,
            username=sql_info.db_user,
            password=sql_info.db_password,
            db=sql_info.db_name,
        )
        async with c.cursor() as cursor:
            t = TimeUtils.get_current_time_without_year()
            await cursor.execute(run_command)
            result = await cursor.fetchall()
            self.log[log_type].append(f"[{t}]: [SQL] -> {run_command}")
            if run_out_name:
                self.g_var[run_out_name] = result[run_out_name]
            return result

    async def execute_method_script(self, log_type: str, script: SchemaCaseSuffix = None):
        print()
        if script.script_id is not None:
            script_info = await CommonConfigCrud.query_script_detail(script_id=script.script_id)
            run_out_name, run_command = script_info.var_key, script_info.var_script
        else:
            run_out_name, run_command = script.run_out_name, script.run_command
        result = await ScriptHandler.python_executor(run_out_name, run_command)
        t = TimeUtils.get_current_time_without_year()
        self.log[log_type].append(f"[{t}]: [Python] -> 设置{run_out_name} == {result[run_out_name]}")
        self.g_var[run_out_name] = result[run_out_name]
        return result

    async def _execute(self, model: Union[SuffixModel, SchemaCaseSuffix], log_type: str):
        if model.enable:
            if model.execute_type == 1:
                await self.execute_method_script(log_type=log_type, script=model)
            elif model.execute_type == 2:
                await self.execute_method_sql(model.sql_id, model.run_command, log_type, model.run_out_name)
            elif model.execute_type == 3:
                pass
            elif model.execute_type == 4:
                await self.execute_method_delay(model.run_delay, log_type)
            else:
                await self.execute_method_script(log_type, model.script_id)
            await redis_client.set_case_log(user_id=self.user_id, value=self.log, case_id=self.case_id, is_update=True)
            await redis_client.set_env_var(self.env_id, self.user_id, self.g_var)

    async def execute_env_prefix(self, is_prefix: bool):
        if is_prefix:
            collect_prefix = await self.get_prefix(env_id=self.env_id)
        else:
            collect_prefix = await self.get_suffix(env_id=self.env_id)

        for p in collect_prefix:
            await self._execute(model=p, log_type="env_prefix" if is_prefix else "env_suffix")

    async def execute_case_prefix(self, is_prefix: bool, temp_prefix: List[Orm2CaseSuffix] = None):
        if is_prefix:
            collect_prefix = await self.get_prefix(case_id=self.case_id, temp=temp_prefix)
        else:
            collect_prefix = await self.get_suffix(case_id=self.case_id, temp=temp_prefix)

        for p in collect_prefix:
            await self._execute(model=p, log_type="case_prefix" if is_prefix else "case_suffix")
