# coding=utf-8
"""
File: news.py
Author: bot
Created: 2023/10/23
Description:
"""
from pydantic import BaseModel, Field

from app.services.api_case.schema.asserts.news import RequestTempAssertNew
from app.services.api_case.schema.query.news import RequestTempQueryNew
from typing import List

from app.services.api_case.schema.suffix.news import RequestTempSuffixNew
from app.services.api_case_new.case_params.headers.schema.news import RequestTempHeaderNew


class RequestEnvNew(BaseModel):
    name: str = Field(..., description="环境名称")
    domain: str = Field(..., description="环境URL")
    headers_info: List[RequestTempHeaderNew] = Field([], description="请求头信息")
    query_info: List[RequestTempQueryNew] = Field([], description="查询信息")
    suffix_info: List[RequestTempSuffixNew] = Field([], description="后缀信息")
    assert_info: List[RequestTempAssertNew] = Field([], description="断言信息")
