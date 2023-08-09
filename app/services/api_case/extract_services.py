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
from app.utils.case_log import CaseLog


class ExtractServices:
    case = CaseLog()

    @staticmethod
    async def extract_with_re(src: str, exp: str, out_name: str, index: int = None):
        """
        正则提取
        :param src: 数据来源
        :param exp: re表达式
        :param out_name: 出参名
        :return:
        """

        result = re.findall(exp, src)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result}

    @staticmethod
    async def extract_with_jsonpath(src: dict, exp: str, out_name: str, index: int = None):
        print(exp, src)
        result = jsonpath.jsonpath(src, exp)
        print(result)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result if result else []}

    @staticmethod
    async def extract(extract_id: int, response: dict, trace_id: str):
        (
            status_code,
            response_header,
            response_cookie,
            response_body,
            response_elapsed,
        ) = AsyncRequest.collect_response_for_test(response)
        extract_detail = await ExtractCrud.query_extract_detail(extract_id)
        print(extract_detail)
        print(C137Response.orm_to_dict(extract_detail))
        if extract_detail is None:
            raise CustomException(EXTRACT_NOT_EXISTS)
        if extract_detail.enable == 0:
            return
        if extract_detail.extract_from == "1":
            src = response_header
        elif extract_detail.extract_from == "2":
            src = response_body
        else:
            src = response_cookie
        print("1", src)
        if extract_detail.extract_type == 2:
            result = await ExtractServices.extract_with_re(
                src, extract_detail.extract_exp, extract_detail.extract_out_name, extract_detail.extract_index
            )
        else:
            result = await ExtractServices.extract_with_jsonpath(
                src, extract_detail.extract_exp, extract_detail.extract_out_name, extract_detail.extract_index
            )

        if result:
            ExtractServices.case.append(f"提取响应生成变量: {extract_detail.extract_out_name}")
            await redis_client.set_case_var_load(trace_id, result)
            await redis_client.set_case_log_load(trace_id, ExtractServices.case.log)
