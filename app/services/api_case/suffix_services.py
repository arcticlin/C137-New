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
from app.handler.script_handler import ScriptHandler
from app.models.api_settings.suffix_settings import SuffixModel
from app.handler.redis_handler import redis_client


class SuffixServices:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = []
        self.g_var = {}
        self.redis_key = f"c:runner_{trace_id}"

    def clear_log(self):
        self.log = []

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
        self.log.append(f"延迟{delay}ms执行")
        await asyncio.sleep(delay / 1000)

    async def execute_sql(self, sql_id: int, text: str):
        self.log.append(f"执行sql: {sql_id} -> {text}")
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
        self.log.append(f"执行脚本: {script_id}")
        script_info = await CommonConfigCrud.query_script_detail(script_id)
        if not script_info:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await ScriptHandler.python_executor(script_info.var_key, script_info.var_script)
        self.g_var[script_info.var_key] = result[script_info.var_key]
        return result

    async def execute_suffix(self, model: SuffixModel):
        if model.enable:
            if model.execute_type == 1:
                await self.execute_script(model.script_id)
            elif model.execute_type == 2:
                await self.execute_sql(model.sql_id, model.run_command)
                # elif item.suffix_type == 3:
                #     await SuffixServices.execute_redis(item.suffix_content)
            elif model.execute_type == 4:
                await self.execute_delay(model.run_delay)

    async def execute_env_prefix(self, env_id: int):
        prefix = await self.get_prefix(env_id=env_id)
        if prefix:
            for p in prefix:
                await self.execute_suffix(p)
            temp = {"vars": self.g_var, "log": {"env_prefix": self.log}}
            await redis_client.set_kv_load(self.redis_key, temp, 600)
