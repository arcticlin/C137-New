# coding=utf-8
"""
File: new_suffix_service.py
Author: bot
Created: 2023/9/22
Description:
"""
import asyncio
from typing import List, Union, Dict

from app.crud.api_case.suffix_crud import SuffixCrud
from app.crud.cconfig.cconfig_crud import CommonConfigCrud
from app.exceptions.cconfig_exp import SQL_NOT_EXISTS
from app.exceptions.custom_exception import CustomException
from app.handler.api_redis_handle import RedisCli
from app.handler.db_handler import DataBaseConnect
from app.handler.response_handler import C137Response
from app.handler.script_handler import ScriptHandler
from app.models.api_settings.suffix_settings import SuffixModel
from app.schemas.api_case.api_case_schemas import Orm2CaseSuffix
from app.schemas.api_settings.suffix_schema import SchemaCaseSuffix
from app.utils.time_utils import TimeUtils


class SuffixService:
    def __init__(self, env_id: int, trace_id: str, case_id: int, is_temp: bool = False):
        self.env_id = env_id
        self.case_id = case_id
        self.trace_id = trace_id
        self.is_temp = is_temp
        self.rds = RedisCli(trace_id)
        self.env_var = dict()
        self.case_var = dict()
        self.env_log: Dict[str, List] = dict(env_prefix=[], env_suffix=[])
        self.case_log = dict(
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

    @staticmethod
    async def execute_method_delay(delay: int):
        """执行延迟"""
        await asyncio.sleep(delay / 1000)

    @staticmethod
    async def execute_method_sql(sql_id: int, run_command: str):
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
            await cursor.execute(run_command)
            result = await cursor.fetchall()
            return result

    @staticmethod
    async def execute_common_script(script: SchemaCaseSuffix):
        script_info = await CommonConfigCrud.query_script_detail(script_id=script.script_id)
        run_out_name, run_command = script_info.var_key, script_info.var_script
        result = await ScriptHandler.python_executor(run_out_name, run_command)
        return result, run_out_name

    @staticmethod
    async def execute_temp_script(script: SchemaCaseSuffix):
        run_out_name, run_command = script.run_out_name, script.run_command
        result = await ScriptHandler.python_executor(run_out_name, run_command)
        return result

    async def _execute(self, model: Union[SuffixModel, SchemaCaseSuffix]):
        if model.env_id:
            if not model.run_each_case:
                log_ = self.env_log["env_prefix" if model.suffix_type == 1 else "env_suffix"]
            else:
                log_ = self.case_log["env_prefix" if model.suffix_type == 1 else "env_suffix"]
        else:
            log_ = self.case_log["case_prefix" if model.suffix_type == 1 else "case_suffix"]
        if model.env_id:
            if not model.run_each_case:
                var_ = self.env_var
            else:
                var_ = self.case_var
        else:
            var_ = self.case_var
        t = TimeUtils.get_current_time_without_year()
        if model.enable:
            if model.execute_type == 1:
                result = await self.execute_temp_script(model)
                var_[model.run_out_name] = result[model.run_out_name]
                log_.append(f"[{t}]: [Python] -> 执行: 设置{model.run_out_name} == {result[model.run_out_name]}")
            elif model.execute_type == 2:
                result = await self.execute_method_sql(model.sql_id, model.run_command)
                if model.run_out_name:
                    var_[model.run_out_name] = result[model.run_out_name]
                log_.append(f"[{t}]: [SQL] -> {model.run_command}")
            elif model.execute_type == 3:
                pass
            elif model.execute_type == 4:
                await self.execute_method_delay(model.run_delay)
                log_.append(f"[{t}]: [延迟执行] -> {model.run_delay}ms")
            else:
                result, run_out_name = await self.execute_common_script(model)
                var_[run_out_name] = result[run_out_name]
                log_.append(f"[{t}]: [公共脚本: {model.name}] -> 设置{run_out_name} == {result[run_out_name]}")
        if model.env_id:
            if not model.run_each_case:
                await self.rds.set_env_var(self.env_id, self.env_var)
                await self.rds.set_env_log(self.env_id, self.env_log)
            else:
                await self.rds.set_case_log(self.case_id, self.case_log)
                await self.rds.set_case_var(self.case_id, self.case_var)
        else:
            await self.rds.set_case_log(self.case_id, self.case_log)
            await self.rds.set_case_var(self.case_id, self.case_var)

    async def execute_env_prefix(self, is_prefix: bool):
        if is_prefix:
            collect_prefix = await self.get_prefix(env_id=self.env_id)
        else:
            collect_prefix = await self.get_suffix(env_id=self.env_id)

        for p in collect_prefix:
            if not p.run_each_case:
                await self._execute(model=p)

    async def execute_case_prefix(self, is_prefix: bool, temp_prefix: List[Orm2CaseSuffix] = None):
        if is_prefix:
            collect_e_prefix = await self.get_prefix(env_id=self.env_id)
        else:
            collect_e_prefix = await self.get_suffix(env_id=self.env_id)
        if is_prefix:
            collect_prefix = await self.get_prefix(case_id=self.case_id, temp=temp_prefix)
        else:
            collect_prefix = await self.get_suffix(case_id=self.case_id, temp=temp_prefix)
        for p in collect_e_prefix:
            if p.run_each_case:
                await self._execute(model=p)
        for p in collect_prefix:
            await self._execute(model=p)
