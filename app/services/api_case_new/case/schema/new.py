# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/10/25
Description:
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from app.services.api_case_new.case_params.headers.schema.news import AddWithHeaderInfo
from app.services.api_case_new.case_params.query.schema.news import AddWithQueryInfo
from app.services.api_case_new.settings.asserts.schema.news import AddWithAssertInfo
from app.services.api_case_new.settings.extract.schema.new import AddWithExtractInfo
from app.services.api_case_new.settings.suffix.schema.news import AddWithSuffixInfo


class AddWithBasicInfo(BaseModel):
    name: str = Field(..., title="用例名称")
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级: P0-P4")
    case_type: int = Field(1, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")


class AddWithUrlInfo(BaseModel):
    url: str = Field(..., title="请求地址")
    method: str = Field(..., title="请求方法")


class AddWithBodyInfo(BaseModel):
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")


class RequestApiCaseNew(BaseModel):
    directory_id: int = Field(..., title="环境目录")
    basic_info: AddWithBasicInfo = Field(..., title="基础信息")
    url_info: AddWithUrlInfo = Field(..., title="请求地址信息")
    body_info: AddWithBodyInfo = Field(..., title="请求体信息")
    query_info: List[AddWithQueryInfo] = Field([], title="请求参数信息")
    path_info: List[AddWithQueryInfo] = Field([], title="路径参数信息")
    header_info: List[AddWithHeaderInfo] = Field([], title="请求头信息")
    prefix_info: List[AddWithSuffixInfo] = Field([], title="前置信息")
    suffix_info: List[AddWithSuffixInfo] = Field([], title="后置信息")
    assert_info: List[AddWithAssertInfo] = Field([], title="断言信息")
    extract_info: List[AddWithExtractInfo] = Field([], title="提取信息")


class OutApiCaseNew(BaseModel):
    case_id: int = Field(..., title="用例id")
