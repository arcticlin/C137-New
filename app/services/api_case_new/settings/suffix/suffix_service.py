# coding=utf-8
"""
File: suffix_service.py
Author: bot
Created: 2023/10/25
Description:
"""
import asyncio
from typing import List, Union

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_480_case import PYTHON_SCRIPT_OUT_NAME_WRONG
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.settings.suffix.schema.info import DebugCaseSuffixInfo, OutCaseSuffixInfo
from app.services.common_config.schema.script.news import RequestScriptDebugByForm
from app.services.common_config.schema.sql.news import RequestSqlCommandDebug
from app.services.common_config.script_service import ScriptService
from app.services.common_config.sql_service import SqlService
from app.utils.time_utils import TimeUtils


class SuffixService:
    def __init__(self, rds: ApiRedis):
        self.rds = rds

    @staticmethod
    async def execute_to_delay(delay: int):
        """
        延迟执行
        """
        await asyncio.sleep(delay)

    @staticmethod
    async def execute_to_sql(sql_id: int, command: str, fetch_one: bool):
        """
        执行sql
        """
        form = RequestSqlCommandDebug(sql_id=sql_id, command=command, fetch_one=fetch_one)
        result = await SqlService.debug_sql_command(form)
        return result

    @staticmethod
    async def execute_to_common_script(script_id: int) -> dict:
        """
        执行公共脚本
        """
        result = await ScriptService.debug_script_by_id(script_id)
        return result

    @staticmethod
    async def execute_to_temp_script(var_key: str, var_script: str):
        """
        执行临时脚本
        """
        form = RequestScriptDebugByForm(var_key=var_key, var_script=var_script)
        result = await ScriptService.debug_script_by_form(form)
        return result

    @staticmethod
    async def execute_to_redis():
        pass

    async def _executor(self, data: Union[DebugCaseSuffixInfo, OutCaseSuffixInfo]):
        """
        前/后置执行器
        """
        var = dict()
        log = []
        t = TimeUtils.get_current_time_without_year()
        if not data.enable:
            return None, None
        if data.execute_type == 1:
            # 执行python脚本
            result = await self.execute_to_common_script(data.script_id)
            print(result)
            if data.run_out_name not in result.keys():
                raise CustomException(PYTHON_SCRIPT_OUT_NAME_WRONG)
            log.append(f"[{t}]: [公共脚本] -> 执行: 设置变量: {data.run_out_name} = {result[data.run_out_name]}")
            return result, log
        elif data.execute_type == 2:
            # 执行sql
            log.append(f"[{t}]: [SQL] -> 执行SQL语句: {data.run_command}")
            result = await self.execute_to_sql(data.sql_id, data.run_command, data.fetch_one)
            if data.run_out_name:
                log.append(f"[{t}]: [SQL] -> 执行: 设置变量: {data.run_out_name} = {result}")
                return result, log
            return None, log
        elif data.execute_type == 3:
            # 执行redis
            result = await self.execute_to_redis()
        elif data.execute_type == 4:
            # 执行延迟
            await self.execute_to_delay(data.run_delay)
            return None, log
        else:
            # 执行临时脚本
            result = await self.execute_to_temp_script(data.run_out_name, data.run_command)
            log.append(f"[{t}]: [Python] -> 执行: 设置变量: {data.run_out_name} = {result[data.run_out_name]}")
            return result, log

    async def execute_env_prefix(
        self, data: Union[List[DebugCaseSuffixInfo], List[OutCaseSuffixInfo]], is_prefix: bool
    ):
        for p in data:
            if not p.enable:
                continue
            result, log = await self._executor(p)
            if result is not None:
                await self.rds.set_env_var(result)
            if is_prefix:
                log = {"env_prefix": log}
            else:
                log = {"env_suffix": log}
            await self.rds.set_env_log(log)

    async def execute_case_prefix(
        self, data: Union[List[DebugCaseSuffixInfo], List[OutCaseSuffixInfo]], is_prefix: bool
    ):
        for p in data:
            if not p.enable:
                continue
            result, log = await self._executor(p)
            if result is not None:
                await self.rds.set_env_var(result)
            if is_prefix:
                log = {"env_prefix": log}
            else:
                log = {"env_suffix": log}
            await self.rds.set_env_log(log)
