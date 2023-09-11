# coding=utf-8
"""
File: api_case_schema_new.py
Author: bot
Created: 2023/9/11
Description:
"""


from pydantic import BaseModel, Field

from app.schemas.api_settings.assert_schema import SchemaCaseAssert
from app.schemas.api_settings.extract_schema import SchemaCaseExtract
from app.schemas.api_settings.suffix_schema import SchemaCaseSuffix


class SchemaCaseBaseInfo(BaseModel):
    name: str
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级: P0-P4")
    case_type: int = Field(1, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")
    directory_id: int = Field(None, title="目录id")
    # tag: list[str]


class SchemaCaseUrl(BaseModel):
    url: str
    method: str


class SchemaCaseBody(BaseModel):
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: str = Field(None, title="请求体数据")


class SchemaCaseParams(BaseModel):
    path_id: str = Field(None, title="id")
    key: str
    value: str
    types: int
    enable: bool
    comment: str = Field(None, title="备注")


class SchemaCaseHeaders(BaseModel):
    header_id: str = Field(None, title="id")
    key: str
    value: str
    value_type: int
    enable: bool
    comment: str = Field(None, title="备注")


class SchemaRequestAddCase(BaseModel):
    directory_id: int
    basic_info: SchemaCaseBaseInfo
    url_info: SchemaCaseUrl
    body_info: SchemaCaseBody
    query_info: list[SchemaCaseParams] = Field(..., title="请求参数")
    path_info: list[SchemaCaseParams] = Field(..., title="路径参数")
    header_info: list[SchemaCaseHeaders] = Field(..., title="请求头")
    prefix_info: list[SchemaCaseSuffix] = Field(..., title="前置处理")
    suffix_info: list[SchemaCaseSuffix] = Field(..., title="后置处理")
    assert_info: list[SchemaCaseAssert] = Field(..., title="断言")
    extract_info: list[SchemaCaseExtract] = Field(..., title="提取")


class SchemaRequestUpdateCase(BaseModel):
    case_id: int = Field(..., title="用例id")
    env_id: int = Field(None, title="环境id")
    basic_info: SchemaCaseBaseInfo = Field(None, title="基础信息")
    url_info: SchemaCaseUrl = Field(None, title="url信息")
    body_info: SchemaCaseBody = Field(None, title="请求体信息")
    query_info: list[SchemaCaseParams] = Field([], title="请求参数")
    path_info: list[SchemaCaseParams] = Field([], title="路径参数")
    header_info: list[SchemaCaseHeaders] = Field([], title="请求头")
    prefix_info: list[SchemaCaseSuffix] = Field([], title="前置处理")
    suffix_info: list[SchemaCaseSuffix] = Field([], title="后置处理")
    assert_info: list[SchemaCaseAssert] = Field([], title="断言")
    extract_info: list[SchemaCaseExtract] = Field([], title="提取")
