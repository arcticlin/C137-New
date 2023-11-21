# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/11/21
Description:
"""
from typing import List

from pydantic import Field

from app.core.basic_schema import CommonResponse
from app.services.ws_test.schema.ws_result.info import OutResultBasicInfo, OutStaticPlanResult


class ResponseWsCaseResult(CommonResponse):
    data: List[OutResultBasicInfo] = Field(..., description="用例结果列表")


class ResponseStatisResult(CommonResponse):
    data: OutStaticPlanResult = Field(..., description="统计结果")
