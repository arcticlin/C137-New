# coding=utf-8
"""
File: api_case_schema.py
Author: bot
Created: 2023/8/2
Description:
"""

from pydantic import BaseModel, Field
from app.schemas.api_case.api_headers_schema import AddApiHeaderRequest
from app.schemas.api_case.api_path_schema import AddApiPathRequest
from typing import List, Union

from app.schemas.response_schema import CommonResponse


class AddApiCaseRequest(BaseModel):
    name: str = Field(..., title="用例名称")
    request_type: int = Field(..., title="请求协议类型, 1: http, 2: grpc")
    url: str = Field(..., title="请求url")
    method: str = Field(..., title="请求方法")
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: str = Field(None, title="请求体数据")
    path: List[AddApiPathRequest] = Field(None, title="请求路径参数")
    headers: List[AddApiHeaderRequest] = Field(None, title="请求头")
    directory_id: int = Field(..., title="目录id")
    tag: str = Field(None, title="标签")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级, P0-P4")
    case_type: int = Field(1, title="用例类型, 1. 正常用例 2. 前置用例 3. 数据构造")


class UpdateApiCaseRequest(BaseModel):
    name: str = Field(None, title="用例名称")
    url: str = Field(None, title="请求url")
    method: str = Field(None, title="请求方法")
    body_type: int = Field(None, title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: str = Field(None, title="请求体数据")
    status: int = Field(None, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field(None, title="用例优先级, P0-P4")
    case_type: int = Field(None, title="用例类型, 1. 正常用例 2. 前置用例 3. 数据构造")


class DeleteApiCaseRequest(BaseModel):
    case_id: int = Field(..., title="用例id")


class ApiCaseShow(BaseModel):
    name: str = Field(..., title="用例名称")
    request_type: int = Field(..., title="请求协议类型, 1: http, 2: grpc")
    url: str = Field(..., title="请求url")
    method: str = Field(..., title="请求方法")
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, bytes, None] = Field(None, title="请求体数据")
    path: List[AddApiPathRequest] = Field([], title="请求路径参数")
    query: List[AddApiPathRequest] = Field([], title="请求query参数")
    headers: List[AddApiHeaderRequest] = Field([], title="请求头")
    directory_id: int = Field(..., title="目录id")
    tag: str = Field(None, title="标签")
    status: int = Field(..., title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field(..., title="用例优先级, P0-P4")
    case_type: int = Field(..., title="用例类型, 1. 正常用例 2. 前置用例 3. 数据构造")


class ApiCaseInfoResponse(CommonResponse):
    data: ApiCaseShow
