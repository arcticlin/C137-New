# coding=utf-8
"""
File: news.py
Author: bot
Created: 2023/10/23
Description:
"""
from typing import List

from pydantic import BaseModel, Field


from app.services.api_case.case_params.headers.schema.news import RequestTempHeaderNew, AddWithHeaderInfo
from app.services.api_case.case_params.query.schema.news import AddWithQueryInfo
from app.services.api_case.settings.asserts.schema.news import AddWithAssertInfo
from app.services.api_case.settings.suffix.schema.news import AddWithSuffixInfo


class RequestEnvNew(BaseModel):
    name: str = Field(..., description="环境名称")
    domain: str = Field(..., description="环境URL")
    headers_info: List[AddWithHeaderInfo] = Field([], description="请求头信息")
    query_info: List[AddWithQueryInfo] = Field([], description="查询信息")
    suffix_info: List[AddWithSuffixInfo] = Field([], description="后缀信息")
    assert_info: List[AddWithAssertInfo] = Field([], description="断言信息")
