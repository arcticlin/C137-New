import json
import re
from typing import Union

import jsonpath

from app.crud.api_case.assert_crud import AssertCurd
from app.handler.async_http_client import AsyncRequest
from app.handler.new_redis_handler import redis_client
from app.schemas.api_case.api_case_schemas import Orm2CaseAssert
from app.utils.time_utils import TimeUtils


class AssertService:
    def __init__(self, env_id: int, user_id: int, async_response: dict, case_id: int = None):
        self.env_id = env_id
        self.user_id = user_id
        self.case_id = case_id
        self.async_response = async_response
        self.log = dict(env_assert=[], case_assert=[])

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
                return {"actual": f"'{exp}'返回'{result}'", "expect": expect, "result": str(expect) in str(result)}
                # return result, expect in result
            return {"actual": f"'{exp}'返回'{result}'", "expect": "存在", "result": True}
        return {"actual": f"'{exp}'返回'{result}'", "expect": "不存在", "result": False}

    @staticmethod
    def _jsonpath(actual: Union[list, dict], exp: str, expect=None) -> dict:
        result = jsonpath.jsonpath(actual, exp)
        if result:
            if expect is not None:
                return {"actual": f"'{exp}'返回'{result}'", "expect": expect, "result": str(expect) in str(result)}

            return {"actual": f"'{exp}'返回'{result}'", "expect": "存在", "result": True}
        return {"actual": f"'{exp}'返回'{result}'", "expect": "不存在", "result": False}

    async def assert_from_env(self):
        """
        从环境变量中获取断言
        """
        env_assert = await AssertCurd.query_assert_detail(env_id=self.env_id)
        result = [await self.assert_result(e, "env_assert") for e in env_assert]
        return result

    async def assert_from_case(self, data: list[Orm2CaseAssert]):
        result = [await self.assert_result(e, "case_assert") for e in data]
        return result

    async def assert_result(self, assert_info: Orm2CaseAssert, log_type: str):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(self.async_response)
        # 提取来源, 1: res_header 2: res_body 3: res_status_code 4: res_elapsed
        if assert_info.assert_from == 1:
            src = response_header
        elif assert_info.assert_from == 2:
            src = response_body
        elif assert_info.assert_from == 3:
            src = status_code
        else:
            src = response_elapsed

        # 断言方式:
        # 1: equal 2: n-equal
        # 3:GE 4: LE
        # 5:in-list 6: not-in-list
        # 7: contain 8: not-contain
        # 9: start-with 10: end-with
        # 11: Re_Gex 12:Json-Path
        t = TimeUtils.get_current_time_without_year()
        if assert_info.assert_type == 1:
            # 相等
            result = self._equal(src, assert_info.assert_value, True)

            self.log[log_type].append(
                f"[{t}]: [断言-相等] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 2:
            result = self._equal(src, assert_info.assert_value, False)
            self.log[log_type].append(
                f"[{t}]: [断言-不相等] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 3:
            result = self._ge(src, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-大于等于] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 4:
            result = self._ge(src, assert_info.assert_value, False)

            self.log[log_type].append(
                f"[{t}]: [断言-小于等于] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 5:
            result = self._in_list(src, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-存在数组中] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 6:
            result = self._in_list(src, assert_info.assert_value, False)
            self.log[log_type].append(
                f"[{t}]: [断言-不存在数组中] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 7:
            result = self._contains(src, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-包含在内] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 8:
            result = self._contains(src, assert_info.assert_value, False)
            self.log[log_type].append(
                f"[{t}]: [断言-不包含在内] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 9:
            result = self._start_with(src, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-以XX开头] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 10:
            result = self._start_with(src, assert_info.assert_value, False)
            self.log[log_type].append(
                f"[{t}]: [断言-以XX结尾] -> 实际: {src} 期望: {assert_info.assert_value} 结果: {result['result']}"
            )

        elif assert_info.assert_type == 11:
            result = self._re(src, assert_info.assert_exp, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-匹配到RE表达式] -> 实际: {src} 期望: {assert_info.assert_exp} 结果: {result['result']}"
            )

        else:
            result = self._jsonpath(src, assert_info.assert_exp, assert_info.assert_value)
            self.log[log_type].append(
                f"[{t}]: [断言-匹配到JP表达式] -> 实际: {src} 期望: {assert_info.assert_exp} 结果: {result['result']}"
            )

        await redis_client.set_case_log(user_id=self.user_id, value=self.log, case_id=self.case_id, is_update=True)
        result["name"] = assert_info.name
        result["assert_from"] = assert_info.assert_from
        result["assert_type"] = assert_info.assert_type
        return result

    @staticmethod
    def assert_response_result(env_result: list, case_result: dict):
        _flag = []
        for e in env_result:
            # 特殊处理判断状态码和响应时长的字段
            if e["assert_from"] in (3, 4) and any(c["assert_from"] in (3, 4) for c in case_result):
                _flag.append(all(c["result"] for c in case_result if c["assert_from"] in (3, 4)))
            else:
                _flag.append(e["result"])
        for c in case_result:
            _flag.append(c["result"])

        return _flag
