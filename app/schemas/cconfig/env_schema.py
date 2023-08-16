# coding=utf-8
"""
File: env_schema.py
Author: bot
Created: 2023/8/11
Description:
"""
from pydantic import BaseModel, Field
from app.schemas.response_schema import CommonResponse
from app.schemas.api_case.api_path_schema import ApiPathShow, AddApiPathRequest
from app.schemas.api_case.api_headers_schema import ApiHeaderShow, AddApiHeaderRequest
from app.schemas.api_settings.assert_schema import AssertShow
from app.schemas.api_settings.suffix_schema import SuffixSimpleShow


class EnvInfoAddRequest(BaseModel):
    name: str = Field(..., description="环境名称")
    url: str = Field(..., description="环境URL")


class EnvAddRequest(BaseModel):
    env_info: EnvInfoAddRequest = Field(..., description="环境信息")
    query_info: list[AddApiPathRequest] = Field([], description="查询信息")
    headers_info: list[AddApiHeaderRequest] = Field([], description="请求头信息")


class EnvUpdateRequest(BaseModel):
    name: str = Field(None, description="环境名称")
    url: str = Field(None, description="环境URL")


class EnvListShow(BaseModel):
    env_id: int = Field(..., description="环境ID")
    name: str = Field(..., description="环境名称")
    url: str = Field(..., description="环境URL")
    create_user: int = Field(..., description="创建人")


class EnvDetailShow(BaseModel):
    env_info: EnvListShow = Field(..., description="环境信息")
    prefix_info: list[SuffixSimpleShow] = Field([], description="前缀信息")
    suffix_info: list[SuffixSimpleShow] = Field([], description="后缀信息")
    query_info: list[ApiPathShow] = Field([], description="查询信息")
    headers_info: list[ApiHeaderShow] = Field([], description="请求头信息")
    assert_info: list[AssertShow] = Field([], description="断言信息")


class EnvListResponse(CommonResponse):
    data: list[EnvListShow] = Field(..., description="环境列表")
    total: int = Field(..., description="总数")


class EnvDetailResponse(CommonResponse):
    data: EnvDetailShow = Field(..., description="环境详情")
