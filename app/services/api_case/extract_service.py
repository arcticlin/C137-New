import re

import jsonpath

from app.handler.async_http_client import AsyncRequest
from app.handler.new_redis_handler import redis_client
from app.schemas.api_case.api_case_schemas import Orm2CaseExtract


class ExtractService:
    def __init__(self, env_id: int, user_id: int, async_response: dict, case_id: int = None):
        self.env_id = env_id
        self.user_id = user_id
        self.case_id = case_id
        self.async_response = async_response
        self.log = dict(extract=[])
        self.g_var = dict()

    @staticmethod
    async def extract_with_re(src: str, exp: str, out_name: str, index: int = None):
        """
        正则提取
        :param src: 数据来源
        :param exp: re表达式
        :param out_name: 出参名
        :param index: 下标
        :return:
        """

        result = re.findall(exp, src)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result}

    @staticmethod
    async def extract_with_jsonpath(src: dict, exp: str, out_name: str, index: int = None):
        result = jsonpath.jsonpath(src, exp)
        print(out_name, index, bool(index is not None), result)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result if result else []}

    async def extract(self, extract_data: list[Orm2CaseExtract]):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(self.async_response)

        temp_result = []

        for e in extract_data:
            if not e.enable:
                continue
            if e.extract_from == 1:
                src = response_header
            elif e.extract_from == 2:
                src = response_body
            else:
                src = response_cookie
            if e.extract_type == 2:
                result = await self.extract_with_re(src, e.extract_exp, e.extract_out_name, e.extract_index)
            else:
                result = await self.extract_with_jsonpath(src, e.extract_exp, e.extract_out_name, e.extract_index)
            if result:
                temp_result.append(
                    {
                        "name": e.extract_out_name,
                        "extract_key": e.extract_out_name,
                        "extract_result": result[e.extract_out_name],
                    }
                )

                self.log["extract"].append(f"提取响应生成变量: {e.extract_out_name}")
                self.g_var[e.extract_out_name] = result[e.extract_out_name]
            else:
                temp_result.append(
                    {
                        "name": e.extract_out_name,
                        "extract_key": e.extract_out_name,
                        "extract_value": None,
                    }
                )
                self.log["extract"].append(f"提取响应生成变量: {e.extract_out_name}")
                self.g_var[e.extract_out_name] = None
        await redis_client.set_case_log(user_id=self.user_id, value=self.log, case_id=self.case_id, is_update=True)
        await redis_client.set_env_var(env_id=self.env_id, value=self.g_var, user_id=self.user_id)
        return temp_result
