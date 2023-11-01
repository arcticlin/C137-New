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
from app.handler.case.case_handler_new import CaseHandler
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.case.crud.case_crud import ApiCaseCrud
from app.services.api_case_new.settings.asserts.asserts_service import AssertService
from app.services.api_case_new.settings.extract.extract_service import ExtractService
from app.services.api_case_new.settings.suffix.schema.info import DebugCaseSuffixInfo, OutCaseSuffixInfo
from app.services.common_config.env_service import EnvService
from app.services.common_config.schema.env.responses import EnvDetailOut
from app.services.common_config.schema.script.news import RequestScriptDebugByForm
from app.services.common_config.schema.sql.news import RequestSqlCommandDebug
from app.services.common_config.script_service import ScriptService
from app.services.common_config.sql_service import SqlService
from app.utils.time_utils import TimeUtils


SuffixInfo = Union[DebugCaseSuffixInfo, OutCaseSuffixInfo]


class SuffixService:
    def __init__(self, rds: ApiRedis, env_detail: EnvDetailOut):
        self.rds = rds
        self.env_detail = env_detail

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

    async def execute_to_case(self, case_id: int, is_prefix: bool = False, is_env: bool = False):
        temp_case = await ApiCaseCrud.query_case_detail(case_id)
        # 前置Case执行用例前置, 但是执行变量和日志应当存储在环境Redis中
        if is_env:
            await self.execute_env_prefix(temp_case.prefix_info, True)
        else:
            await self.execute_case_prefix(temp_case.prefix_info, True)
        # 执行用例
        c_server = CaseHandler(temp_case, self.env_detail, self.rds)
        response = await c_server.case_executor()
        if is_env:
            await self.execute_env_prefix(temp_case.prefix_info, False)
        else:
            await self.execute_case_prefix(temp_case.prefix_info, False)
        c_assert_server = AssertService(self.rds)
        case_assert_result = [await c_assert_server.assert_result(response, x) for x in temp_case.assert_info]
        c_extract_server = ExtractService(self.rds)
        await c_extract_server.extract(response, temp_case.extract_info)
        return response

    async def _executor(self, data: SuffixInfo, is_prefix: bool = False, is_env: bool = False):
        """
        前/后置执行器
        """
        var = dict()
        log = []
        t = TimeUtils.get_current_time_without_year()
        if not data.enable:
            return None, None
        if data.execute_type == 1:
            # 执行公共脚本
            result = await self.execute_to_common_script(data.script_id)
            log.append(f"[{t}]: [公共脚本] -> 执行: 设置变量: {result}")
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
        elif data.execute_type == 6:
            result = await self.execute_to_case(data.run_case_id, is_prefix, is_env)
            log.append(f"[{t}]: [Case] -> 执行: 执行用例: {data.run_case_id} = 接口状态: {result.status_code}")
            return None, log
        else:
            # 执行临时脚本
            result = await self.execute_to_temp_script(data.run_out_name, data.run_command)
            if data.run_out_name not in result.keys():
                raise CustomException(PYTHON_SCRIPT_OUT_NAME_WRONG)
            log.append(f"[{t}]: [Python] -> 执行: 设置变量: {data.run_out_name} = {result[data.run_out_name]}")
            return result, log

    async def execute_env_prefix(
        self,
        data: List[SuffixInfo],
        is_prefix: bool,
        run_each_time: bool = False,
    ):
        for p in data:
            if not p.enable:
                continue
            if run_each_time and not p.run_each_case:
                continue

            result, log = await self._executor(p, is_prefix)
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
            result, log = await self._executor(p, is_prefix)
            if result is not None:
                await self.rds.set_case_var(result)
            if is_prefix:
                log = {"case_prefix": log}
            else:
                log = {"case_suffix": log}
            await self.rds.set_case_log(log)
