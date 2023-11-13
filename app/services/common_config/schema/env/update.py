# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/10/23
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.services.api_case.case_params.headers.schema.update import RequestHeaderUpdate
from app.services.api_case.case_params.query.schema.update import RequestQueryUpdate
from app.services.api_case.settings.asserts.schema.update import RequestAssertUpdate
from app.services.api_case.settings.suffix.schema.update import RequestSuffixUpdate


class RequestEnvUpdate(BaseModel):
    name: str = Field(..., description="环境名称")
    domain: str = Field(..., description="环境URL")
    headers_info: List[RequestHeaderUpdate] = Field([], description="请求头信息")
    query_info: List[RequestQueryUpdate] = Field([], description="查询信息")
    prefix_info: List[RequestSuffixUpdate] = Field([], description="前置信息")
    suffix_info: List[RequestSuffixUpdate] = Field([], description="后缀信息")
    assert_info: List[RequestAssertUpdate] = Field([], description="断言信息")
