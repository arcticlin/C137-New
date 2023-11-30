# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse
from app.services.ws_test.schema.ws_case.info import OutWsCaseBasicInfo
from app.services.ws_test.schema.ws_case.new import OutAddWsCase


class ResponseWsCaseList(CommonResponse):
    data: list[OutWsCaseBasicInfo] = Field(..., description="WS_CASE列表")
    # total = Field(0, description="总数")


class ResponseWsCaseDetail(CommonResponse):
    data: OutWsCaseBasicInfo = Field(..., description="WS_CASE详情")


class ResponseAddWsCase(CommonResponse):
    data: OutAddWsCase = Field(..., description="添加WS_CASE后返回的ID")
