# coding=utf-8
"""
File: extract_service.py
Author: bot
Created: 2023/10/25
Description:
"""
import re
from typing import Any

import jsonpath

from app.handler.redis.api_redis_new import ApiRedis


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
        result = re.findall(expression, source)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result}

    @staticmethod
    def extract_with_jsonpath(source: dict, expression: str, out_name: str, index: int = None):
        result = jsonpath.jsonpath(source, expression)
        if result and index is not None:
            return {out_name: result[index]}
        return {out_name: result if result else []}
