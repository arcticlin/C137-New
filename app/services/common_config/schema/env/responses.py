# coding=utf-8
"""
File: responses.py
Author: bot
Created: 2023/10/23
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse

from app.services.api_case.case_params.headers.schema.info import OutHeaderInfo
from app.services.api_case.case_params.query.schema.info import OutParamsInfo
from app.services.api_case.settings.asserts.schema.info import OutAssertInfo
from app.services.api_case.settings.suffix.schema.info import OutCaseSuffixInfo


class EnvListOut(BaseModel):
    env_id: int = Field(..., description="环境id")
    name: str = Field(..., description="环境名称")
    domain: str = Field(..., description="环境URL")


class EnvDetailOut(BaseModel):
    env_id: int = Field(..., description="环境id")
    name: str = Field(..., description="环境名称")
    domain: str = Field(..., description="环境URL")
    headers_info: List[OutHeaderInfo] = Field([], description="请求头信息")
    query_info: List[OutParamsInfo] = Field([], description="查询信息")
    prefix_info: List[OutCaseSuffixInfo] = Field([], description="前缀信息")
    suffix_info: List[OutCaseSuffixInfo] = Field([], description="后缀信息")
    assert_info: List[OutAssertInfo] = Field([], description="断言信息")


class EnvAddOut(BaseModel):
    env_id: int


class ResponseEnvList(CommonResponse):
    data: List[EnvListOut] = Field(..., description="环境列表")


class ResponseEnvDetail(CommonResponse):
    data: EnvDetailOut = Field(..., description="环境详情")


class ResponseEnvAdd(CommonResponse):
    data: EnvAddOut = Field(..., description="环境新增")
