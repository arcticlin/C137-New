# coding=utf-8
"""
File: extract_services.py
Author: bot
Created: 2023/8/8
Description:
"""
from typing import Union

from app.crud.api_case.extract_crud import ExtractCrud
import re, jsonpath

from app.exceptions.case_exp import EXTRACT_NOT_EXISTS
from app.exceptions.commom_exception import CustomException
from app.handler.async_http_client import AsyncRequest
from app.handler.redis_handler import redis_client
from app.handler.response_handler import C137Response
from app.schemas.api_case.api_request_temp import TempRequestExtract
from app.utils.case_log import CaseLog


class ExtractServices:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = CaseLog()

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
            print("1asda", result)
            print(result[0])
            return {out_name: result[index]}
        return {out_name: result if result else []}

    async def extract(
        self,
        response: dict,
        temp_extract: list[TempRequestExtract] = None,
        case_id: int = None,
    ):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(response)
        if case_id != None:
            extract_detail = await ExtractCrud.query_case_extract(case_id)
        else:
            extract_detail = temp_extract
        temp_result = []

        for e in extract_detail:
            print(e)
            if e.enable == 0:
                continue
            if e.extract_from == 1:
                src = response_header
            elif e.extract_from == 2:
                src = response_body
            else:
                src = response_cookie
            if e.extract_type == 2:
                result = await ExtractServices.extract_with_re(src, e.extract_exp, e.extract_out_name, e.extract_index)
            else:
                result = await ExtractServices.extract_with_jsonpath(
                    src, e.extract_exp, e.extract_out_name, e.extract_index
                )
            if result:
                temp_result.append(
                    {
                        "name": e.extract_out_name,
                        "extract_key": e.extract_out_name,
                        "extract_result": result[e.extract_out_name],
                    }
                )
                self.log.log_append(f"提取响应生成变量: {e.extract_out_name}", "extract")
            else:
                temp_result.append(
                    {
                        "name": e.extract_out_name,
                        "extract_key": e.extract_out_name,
                        "extract_value": None,
                    }
                )
                self.log.log_append(f"提取响应生成变量失败: {e.extract_out_name}", "extract")
            await redis_client.set_case_var_load(self.trace_id, result)
            await redis_client.set_case_log_load(self.trace_id, self.log.logs, "extract")
        return temp_result
