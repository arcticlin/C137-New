# coding=utf-8
"""
File: new_assert_services.py
Author: bot
Created: 2023/9/7
Description:
"""
import json
from typing import Union, Tuple, List

import jsonpath

from app.exceptions.case_exp import ASSERT_NOT_EXISTS
from app.exceptions.commom_exception import CustomException
from app.handler.async_http_client import AsyncRequest
from app.crud.api_case.assert_crud import AssertCurd
from app.handler.response_handler import C137Response
from app.handler.redis_handler import redis_client
import re

from app.models.api_settings.assert_settings import AssertModel
from app.schemas.api_case.api_request_temp import TempRequestAssert
from app.utils.case_log import CaseLog


class NewAssertServices:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = CaseLog()

    @staticmethod
    def _equal(actual: int, expect: Union[str, list], is_equal: bool = True) -> dict:
        if isinstance(expect, str):
            expect = int(expect)
        if is_equal:
            return {"actual": actual, "expect": expect, "result": actual == expect}
        return {"actual": actual, "expect": expect, "result": actual != expect}

    @staticmethod
    def _ge(actual: int, expect: Union[str, list], is_ge: bool = True) -> dict:
        if isinstance(expect, str):
            expect = int(expect)
        if is_ge:
            return {"actual": actual, "expect": expect, "result": actual >= expect}
        return {"actual": actual, "expect": expect, "result": actual <= expect}

    @staticmethod
    def _in_list(actual, expect: Union[str, list], is_in: bool = True) -> dict:
        try:
            if isinstance(expect, str):
                expect = json.loads(expect)
        except Exception as e:
            pass
        if is_in:
            return {"actual": actual, "expect": expect, "result": actual in expect}
        return {"actual": actual, "expect": expect, "result": actual not in expect}

    @staticmethod
    def _contains(actual: str, expect: str, is_contains: bool = True) -> dict:
        if is_contains:
            return {"actual": actual, "expect": expect, "result": actual in expect}
        return {"actual": actual, "expect": expect, "result": actual not in expect}

    @staticmethod
    def _start_with(actual: str, expect: str, is_start: bool = True) -> dict:
        if is_start:
            return {"actual": actual, "expect": expect, "result": actual.startswith(expect)}
        return {"actual": actual, "expect": expect, "result": actual.endswith(expect)}

    @staticmethod
    def _re(actual: str, exp: str, expect=None) -> dict:
        result = re.findall(exp, actual)
        if result:
            if expect is not None:
                return {"actual": f"'{exp}'返回'{result}'", "expect": expect, "result": expect in result}
                # return result, expect in result
            return {"actual": f"'{exp}'返回'{result}'", "expect": "存在", "result": True}
        return {"actual": f"'{exp}'返回'{result}'", "expect": "不存在", "result": False}

    @staticmethod
    def _jsonpath(actual: Union[list, dict], exp: str, expect=None) -> dict:
        result = jsonpath.jsonpath(actual, exp)
        if result:
            if expect is not None:
                return {"actual": f"'{exp}'返回'{result}'", "expect": expect, "result": expect in result}

            return {"actual": f"'{exp}'返回'{result}'", "expect": "存在", "result": True}
        return {"actual": f"'{exp}'返回'{result}'", "expect": "不存在", "result": False}

    async def assert_from_env(self, env_id: int, async_response: dict):
        env_assert = await AssertCurd.query_assert_detail(env_id=env_id)
        result = [await self.assert_result(e, async_response, self.trace_id, "env_assert") for e in env_assert]
        return result

    async def assert_from_case(self, case_id: int, response: dict) -> List:
        case_assert_detail = await AssertCurd.query_assert_detail(case_id=case_id)
        result = [await self.assert_result(e, response, self.trace_id, "case_assert") for e in case_assert_detail]
        return result

    async def assert_from_temp(self, data: list[TempRequestAssert], response: dict) -> list:
        result = [await self.assert_result(e, response, self.trace_id, "case_assert") for e in data]
        return result

    async def assert_result(
        self,
        assert_detail: Union[AssertModel, TempRequestAssert],
        response: dict,
        trace_id: str = None,
        log_type: str = None,
    ):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(response)
        if assert_detail.assert_from == 1:
            src = response_header
        elif assert_detail.assert_from == 2:
            src = response_body
        elif assert_detail.assert_from == 3:
            src = status_code
        else:
            src = response_elapsed
        if assert_detail.assert_type == 1:
            # 相等
            result = self._equal(src, assert_detail.assert_value, True)
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
