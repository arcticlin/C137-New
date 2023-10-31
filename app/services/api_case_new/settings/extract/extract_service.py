# coding=utf-8
"""
File: extract_service.py
Author: bot
Created: 2023/10/25
Description:
"""
import json
import re
from typing import Any, List, Union

import jsonpath

from app.handler.case.schemas import AsyncResponseSchema
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.settings.extract.schema.info import DebugExtractInfo, OutExtractInfo, OutExtractResult

ExtractInfo = Union[DebugExtractInfo, OutExtractInfo]


class ExtractService:
    def __init__(self, rds: ApiRedis):
        self.rds = rds
        self.log = dict(env_extract=[], case_extract=[])

    @staticmethod
    def extract_with_re(source: Any, expression: str, out_name: str, index: int = None):
        """
        正则提取
        :param source: 数据来源
        :param expression: re表达式
        :param out_name: 出参名
        :param index: 下标
        :return:
        """
        try:
            pattern = re.compile(expression)
        except Exception as e:
            return {out_name: ""}, str(e)
        if isinstance(source, list) or isinstance(source, dict):
            source = json.dumps(source, ensure_ascii=False)
        result = re.findall(pattern, source)
        if result and index is not None:
            return {out_name: result[index]}, True
        return {out_name: result}, True

    @staticmethod
    def extract_with_jsonpath(source: dict, expression: str, out_name: str, index: int = None):
        result = jsonpath.jsonpath(source, expression)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result if result else []}

    async def extract(
        self, response_form: AsyncResponseSchema, extract_form: List[ExtractInfo]
    ) -> List[OutExtractResult]:
        temp_result = []
        for e in extract_form:
            re_flag = False
            if not e.enable:
                continue
            if e.extract_from == 1:
                source = response_form.response_headers
            elif e.extract_from == 2:
                source = response_form.response
            else:
                source = response_form.cookies

            if e.extract_type == 2:
                result, _flag = ExtractService.extract_with_re(
                    source, e.extract_exp, e.extract_out_name, e.extract_index
                )
                re_flag = _flag
            else:
                result = ExtractService.extract_with_jsonpath(
                    source, e.extract_exp, e.extract_out_name, e.extract_index
                )

            temp_result.append(
                OutExtractResult(name=e.name, extract_key=e.extract_out_name, extract_value=result if result else "")
            )
            if isinstance(re_flag, str):
                if e.extract_to == 1:
                    self.log["env_extract"].append(f"提取环境生成变量[{e.extract_out_name}]失败: 正则表达式异常: {re_flag}")
                else:
                    self.log["case_extract"].append(f"提取响应生成变量[{e.extract_out_name}]失败: 正则表达式异常: {re_flag}")
            else:
                if e.extract_to == 1:
                    self.log["env_extract"].append(f"提取环境生成变量[{e.extract_out_name}] => {result[e.extract_out_name]} ")
                else:

                    self.log["case_extract"].append(f"提取响应生成变量[{e.extract_out_name}] => {result[e.extract_out_name]} ")
            if e.extract_to == 1:
                await self.rds.set_env_var(result)
                await self.rds.set_env_log(self.log)
            else:
                await self.rds.set_case_var(result)
                await self.rds.set_case_log(self.log)
        return temp_result
