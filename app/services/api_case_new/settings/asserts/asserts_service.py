# coding=utf-8
"""
File: asserts_service.py
Author: bot
Created: 2023/10/25
Description:
"""
import json, re
from typing import Union, List, Any

import jsonpath

from app.handler.case.schemas import AsyncResponseSchema
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.settings.asserts.schema.info import DebugAssertInfo, OutAssertInfo, OutAssertResult
from app.utils.time_utils import TimeUtils

AssertInfo = Union[DebugAssertInfo, OutAssertInfo]


class AssertService:
    def __init__(self, rds: ApiRedis):
        self.rds = rds
        self.log = dict(env_assert=[], case_assert=[])

    @staticmethod
    def _equal(actual: int, expect: Union[str, list], is_equal: bool = True) -> tuple[Any, Any, bool]:
        if isinstance(expect, str):
            expect = int(expect)
        if is_equal:
            return actual, expect, actual == expect
        return actual, expect, actual != expect

    @staticmethod
    def _ge(actual: int, expect: Union[str, list], is_ge: bool = True) -> tuple[Any, Any, bool]:
        if isinstance(expect, str):
            expect = int(expect)
        if is_ge:
            return actual, expect, actual >= expect
        return actual, expect, actual <= expect

    @staticmethod
    def _in_list(actual, expect: Union[str, list], is_in: bool = True) -> tuple[Any, Any, bool]:
        try:
            if isinstance(expect, str):
                expect = json.loads(expect)
        except Exception as e:
            pass
        if is_in:
            return actual, expect, actual in expect
        return actual, expect, actual not in expect

    @staticmethod
    def _contains(actual: str, expect: str, is_contains: bool = True) -> tuple[Any, Any, bool]:
        if is_contains:
            return actual, expect, actual in expect
        return actual, expect, actual not in expect

    @staticmethod
    def _start_with(actual: str, expect: str, is_start: bool = True) -> tuple[Any, Any, bool]:
        if is_start:
            return actual, expect, actual.startswith(expect)
        return actual, expect, actual.endswith(expect)

    @staticmethod
    def _re(actual: str, exp: str, expect=None) -> tuple[Any, Any, bool]:
        result = re.findall(exp, actual)
        if result:
            if expect is not None:
                return f"'{exp}'返回'{result}'", expect, str(expect) in str(result)
            return f"'{exp}'返回'{result}'", expect, True
        return f"'{exp}'返回'{result}'", expect, False

    @staticmethod
    def _jsonpath(actual: Union[list, dict], exp: str, expect=None) -> tuple[Any, Any, bool]:
        result = jsonpath.jsonpath(actual, exp)
        if result:
            if expect is not None:
                return f"'{exp}'返回'{result}'", expect, str(expect) in str(result)
            return f"'{exp}'返回'{result}'", expect, True
        return f"'{exp}'返回'{result}'", expect, False

    async def assert_result(
        self, response_form: AsyncResponseSchema, assert_form: AssertInfo, is_env: bool = False
    ) -> OutAssertResult:
        if is_env:
            log = self.log["env_assert"]
        else:
            log = self.log["case_assert"]
        # 提取来源, 1: res_header 2: res_body 3: res_status_code 4: res_elapsed
        if assert_form.assert_from == 1:
            source = response_form.response_headers
        elif assert_form.assert_from == 2:
            source = response_form.response
        elif assert_form.assert_from == 3:
            source = response_form.status_code
        else:
            source = response_form.elapsed

        # 断言方式:
        # 1: equal 2: n-equal
        # 3:GE 4: LE
        # 5:in-list 6: not-in-list
        # 7: contain 8: not-contain
        # 9: start-with 10: end-with
        # 11: Re_Gex 12:Json-Path
        t = TimeUtils.get_current_time_without_year()
        if assert_form.assert_type == 1:
            result, expect, is_pass = self._equal(source, assert_form.assert_value)
            log.append(f"[{t}]: [断言-相等] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 2:
            result, expect, is_pass = self._equal(source, assert_form.assert_value, False)
            log.append(f"[{t}]: [断言-不相等] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 3:
            result, expect, is_pass = self._ge(source, assert_form.assert_value)
            log.append(f"[{t}]: [断言-大于等于] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 4:
            result, expect, is_pass = self._ge(source, assert_form.assert_value, False)
            log.append(f"[{t}]: [断言-小于等于] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 5:
            result, expect, is_pass = self._in_list(source, assert_form.assert_value)
            log.append(f"[{t}]: [断言-数组中] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 6:
            result, expect, is_pass = self._in_list(source, assert_form.assert_value, False)
            log.append(f"[{t}]: [断言-非数组中] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 7:
            result, expect, is_pass = self._contains(source, assert_form.assert_value)
            log.append(f"[{t}]: [断言-包含] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 8:
            result, expect, is_pass = self._contains(source, assert_form.assert_value, False)
            log.append(f"[{t}]: [断言-不包含] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 9:
            result, expect, is_pass = self._start_with(source, assert_form.assert_value)
            log.append(f"[{t}]: [断言-以XX开头] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 10:
            result, expect, is_pass = self._start_with(source, assert_form.assert_value, False)
            log.append(f"[{t}]: [断言-以XX结尾] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        elif assert_form.assert_type == 11:
            result, expect, is_pass = self._re(source, assert_form.assert_exp, assert_form.assert_value)
            log.append(f"[{t}]: [断言-正则匹配] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        else:
            result, expect, is_pass = self._jsonpath(source, assert_form.assert_exp, assert_form.assert_value)
            log.append(f"[{t}]: [断言-JsonPath] -> 断言结果: {is_pass}, 断言实际值: {result}, 断言期望值: {expect}")
        print("11", self.log)
        await self.rds.set_case_log(self.log)
        return OutAssertResult(
            name=assert_form.name,
            assert_from=assert_form.assert_from,
            assert_type=assert_form.assert_type,
            assert_exp=assert_form.assert_exp,
            expect=assert_form.assert_value,
            actual=result,
            is_pass=is_pass,
        )

    @staticmethod
    def assert_response_result(env_result: List[OutAssertResult], case_result: List[OutAssertResult]):
        """
        当环境断言与用例断言对应的断言来源都是3或4时, 取用例断言结果
        """
        _flag = []
        for e in env_result:
            if e.assert_from in (3, 4) and any(case.assert_from in (3, 4) for case in case_result):
                _flag.append(all(c.is_pass for c in case_result if c.assert_from in (3, 4)))
            else:
                _flag.append(e.is_pass)
        for c in case_result:
            _flag.append(c.is_pass)
        return _flag
