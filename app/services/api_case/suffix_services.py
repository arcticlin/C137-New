# coding=utf-8
"""
File: suffix_services.py
Author: bot
Created: 2023/8/8
Description: 执行Suffix
"""
from app.crud.api_case.suffix_crud import SuffixCrud
import asyncio

from app.crud.cconfig.cconfig_crud import CommonConfigCrud
from app.exceptions.cconfig_exp import SQL_NOT_EXISTS, SCRIPT_NOT_EXISTS
from app.exceptions.commom_exception import CustomException
from app.handler.db_handler import DataBaseConnect
from app.handler.response_handler import C137Response
from app.handler.script_handler import ScriptHandler
from app.models.api_settings.suffix_settings import SuffixModel
from app.handler.redis_handler import redis_client
from app.utils.case_log import CaseLog


class SuffixServices:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = CaseLog()
        self.g_var = {}
        self.redis_key = trace_id

    def record_log(self, redis_key: str):
        pass

    @staticmethod
    async def get_prefix(case_id: int = None, env_id: int = None):
        prefix_info = await SuffixCrud.get_prefix(env_id, case_id)
        return prefix_info

    @staticmethod
    async def get_suffix(case_id: int = None, env_id: int = None):
        suffix_info = await SuffixCrud.get_suffix(env_id, case_id)
        return suffix_info

    async def execute_delay(self, delay: int):
        await asyncio.sleep(delay / 1000)

    async def execute_sql(self, sql_id: int, text: str):
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
            await cursor.execute(text)
            result = await cursor.fetchall()
            return result

    async def execute_script(self, script_id: int):
        script_info = await CommonConfigCrud.query_script_detail(script_id)
        if not script_info:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await ScriptHandler.python_executor(script_info.var_key, script_info.var_script)
        self.g_var[script_info.var_key] = result[script_info.var_key]
        return result

    async def execute_suffix(self, model: SuffixModel, log_type: str):
        is_end = model.suffix_type == 2
        if model.enable:
            if model.execute_type == 1:
                self.log.log_append(f"执行脚本: {model.script_id}", log_type)
                await self.execute_script(model.script_id)
            elif model.execute_type == 2:
                self.log.log_append(f"执行sql: {model.sql_id} -> {model.run_command}", log_type)
                await self.execute_sql(model.sql_id, model.run_command)
                # elif item.suffix_type == 3:
                #     await SuffixServices.execute_redis(item.suffix_content)
            elif model.execute_type == 4:
                self.log.log_append(f"执行延迟: 延迟{model.run_delay}ms执行", log_type)
                await self.execute_delay(model.run_delay)

    async def execute_env_prefix(self, env_id: int):
        prefix = await self.get_prefix(env_id=env_id)
        if prefix:
            for p in prefix:
                await self.execute_suffix(p, "env_prefix")
            await redis_client.set_case_var_load(self.redis_key, self.g_var)
            await redis_client.set_case_log_load(self.redis_key, self.log.logs, "env_prefix")

    async def execute_env_suffix(self, env_id: int):
        prefix = await self.get_suffix(env_id=env_id)
        if prefix:
            for p in prefix:
                await self.execute_suffix(p, "env_suffix")
            await redis_client.set_case_var_load(self.redis_key, self.g_var)
            await redis_client.set_case_log_load(self.redis_key, self.log.logs, "env_suffix")

    async def execute_case_prefix(self, case_id: int):
        prefix = await self.get_prefix(case_id=case_id)
        if prefix:
            for p in prefix:
                await self.execute_suffix(p, "case_prefix")
            await redis_client.set_case_var_load(self.redis_key, self.g_var)
            await redis_client.set_case_log_load(self.redis_key, self.log.logs, "case_prefix")

    async def execute_case_suffix(self, case_id: int):
        prefix = await self.get_suffix(case_id=case_id)
        if prefix:
            for p in prefix:
                await self.execute_suffix(p, "case_prefix")
            await redis_client.set_case_var_load(self.redis_key, self.g_var)
            await redis_client.set_case_log_load(self.redis_key, self.log.logs, "case_prefix")
