# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/10/25
Description:
"""
from typing import List

from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse
from app.services.api_case.case.schema.debug_form import OutDebugResponse
from app.services.api_case.case.schema.info import OutCaseDetailInfo, OutCaseSimpleInfo
from app.services.api_case.case.schema.new import OutApiCaseNew


class ResponseCaseNew(CommonResponse):
    data: OutApiCaseNew = Field(..., title="用例id")


class ResponseCaseDetail(CommonResponse):
    data: OutCaseDetailInfo = Field(..., title="用例详情")


class ResponseCaseList(CommonResponse):
    data: List[OutCaseSimpleInfo] = Field(..., title="用例列表")


class ResponseDebugResult(CommonResponse):
    data: OutDebugResponse = Field(..., title="调试结果")
