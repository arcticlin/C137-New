# coding=utf-8
"""
File: assert_services.py
Author: bot
Created: 2023/8/10
Description:
"""
import jsonpath

from app.exceptions.case_exp import ASSERT_NOT_EXISTS
from app.exceptions.commom_exception import CustomException
from app.handler.async_http_client import AsyncRequest
from app.crud.api_case.assert_crud import AssertCurd
from app.handler.response_handler import C137Response
from app.handler.redis_handler import redis_client
import re

from app.utils.case_log import CaseLog


class AssertServices:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = CaseLog()

    def _equal(self, src, target, is_equal: bool = True):
        if isinstance(src, int):
            target = int(target)
        if is_equal:
            return src == target
        return src != target

    def _ge(self, src: int, target: int, is_ge: bool = True):
        if isinstance(src, int):
            target = int(target)
        if is_ge:
            return src >= target
        return src <= target

    def _in_list(self, src, target: list, is_in: bool = True):
        if is_in:
            return src in target
        return src not in target

    def _contains(self, src: str, target: str, is_contains: bool = True):
        if is_contains:
            return target in src
        return target not in src

    def _start_with(self, src: str, target: str, is_start: bool = True):
        if is_start:
            return src.startswith(target)
        return not src.endswith(target)

    def _re(self, src: str, exp: str):
        result = re.findall(exp, src)
        if result:
            return True
        return False

    def _jsonpath(self, src: (list, dict), exp: str):
        result = jsonpath.jsonpath(src, exp)
        return result

    async def assert_from_env(self, env_id: int, response: dict):
        env_assert_detail = await AssertCurd.query_assert_detail(env_id=env_id)
        result = [await self.assert_result(e, response, self.trace_id, "env_assert") for e in env_assert_detail]
        return result

    async def assert_from_case(self, case_id: int, response: dict):
        case_assert_detail = await AssertCurd.query_assert_detail(case_id=case_id)
        result = [await self.assert_result(e, response, self.trace_id, "case_assert") for e in case_assert_detail]
        return result

    async def assert_result(self, assert_detail, response: dict, trace_id: str = None, log_type: str = None):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(response)
        if assert_detail.enable == 0:
            return
        if assert_detail.assert_from == 1:
            src = response_header
        elif assert_detail.assert_from == 2:
            src = response_body
        elif assert_detail.assert_from == 3:
            src = status_code
        else:
            src = response_elapsed
        if assert_detail.assert_type == 1:
            result = self._equal(src, assert_detail.assert_value)
            self.log.log_append(f"断言-相等 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 2:
            result = self._equal(src, assert_detail.assert_value, False)
            self.log.log_append(f"断言-不相等 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 3:
            result = self._ge(src, assert_detail.assert_value)
            self.log.log_append(f"断言-大于等于 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 4:
            result = self._ge(src, assert_detail.assert_value, False)
            self.log.log_append(f"断言-小于等于 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 5:
            result = self._in_list(src, assert_detail.assert_value)
            self.log.log_append(f"断言-存在数组中 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 6:
            result = self._in_list(src, assert_detail.assert_value, False)
            self.log.log_append(f"断言-不存在数组中 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 7:
            result = self._contains(src, assert_detail.assert_value)
            self.log.log_append(f"断言-包含在内 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 8:
            result = self._contains(src, assert_detail.assert_value, False)
            self.log.log_append(f"断言-不包含在内 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 9:
            result = self._start_with(src, assert_detail.assert_value)
            self.log.log_append(f"断言-以XX开头 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 10:
            result = self._start_with(src, assert_detail.assert_value, False)
            self.log.log_append(f"断言-以XX结尾 -> 实际: {src} 期望: {assert_detail.assert_value} 结果: {result}", log_type)

        elif assert_detail.assert_type == 11:
            result = self._re(src, assert_detail.assert_exp)
            self.log.log_append(f"断言-匹配到RE表达式 -> 实际: {src} 期望: {assert_detail.assert_exp} 结果: {result}", log_type)

        else:
            result = self._jsonpath(src, assert_detail.assert_exp)
            self.log.log_append(f"断言-匹配到JP表达式 -> 实际: {src} 期望: {assert_detail.assert_exp} 结果: {result}", log_type)

        await redis_client.set_case_log_load(trace_id, self.log.logs, log_type)
        return result
