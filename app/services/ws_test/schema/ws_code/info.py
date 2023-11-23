# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/20
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class OutWsCodeBasicInfo(BaseModel):
    ws_id: int
    project_id: int
    code_value: int
    desc: str
    status: int


class OutWsCodeBasicInfoSimply(BaseModel):
    ws_id: int
    project_id: int
    code_value: int
    status: int
    desc: str = None


class ResponseWsCodeList(CommonResponse):
    data: List[OutWsCodeBasicInfoSimply] = Field(..., description="WS_CODE列表")
    total = Field(0, description="总数")


class ResponseWsCodeDetail(CommonResponse):
    data: OutWsCodeBasicInfo = Field(..., description="WS_CODE详情")
