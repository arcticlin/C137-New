# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""
import json
from typing import Union, List

from pydantic import BaseModel, Field, validator

from app.services.api_case_new.case_params.headers.schema.info import OutHeaderInfo
from app.services.api_case_new.case_params.query.schema.info import OutParamsInfo
from app.services.api_case_new.settings.asserts.schema.info import OutAssertInfo
from app.services.api_case_new.settings.extract.schema.info import OutExtractInfo
from app.services.api_case_new.settings.suffix.schema.info import OutCaseSuffixInfo


class OutCaseBasicInfo(BaseModel):
    name: str = Field(..., title="用例名称")
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级: P0-P4")
    case_type: int = Field(1, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")
    temp_domain: str = Field("", description="临时Domain, 用于跳过环境Domain")


class OutCaseUrlInfo(BaseModel):
    url: str = Field(..., title="请求地址")
    method: str = Field(..., title="请求方法")


class OutCaseBodyInfo(BaseModel):
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")

    # @validator("body", pre=True, always=True)
    # def convert_to_json(cls, v, values):
    #     # 如果body_type为1并且body不为空，则尝试将body解析为JSON
    #     if values.get("body_type") == 1 and v and isinstance(v, str):
    #         try:
    #             print(v)
    #             return json.loads(v)
    #         except json.JSONDecodeError:
    #             # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
    #             return v
    #             # raise ValueError("Invalid JSON format")


class OutCaseDetailInfo(BaseModel):
    case_id: int = Field(..., title="用例id")
    directory_id: int = Field(..., title="环境目录")
    basic_info: OutCaseBasicInfo = Field(..., title="基础信息")
    url_info: OutCaseUrlInfo = Field(..., title="请求地址信息")
    body_info: OutCaseBodyInfo = Field(..., title="请求体信息")
    query_info: List[OutParamsInfo] = Field([], title="请求参数信息")
    path_info: List[OutParamsInfo] = Field([], title="路径参数信息")
    header_info: List[OutHeaderInfo] = Field([], title="请求头信息")
    prefix_info: List[OutCaseSuffixInfo] = Field([], title="前置信息")
    suffix_info: List[OutCaseSuffixInfo] = Field([], title="后置信息")
    assert_info: List[OutAssertInfo] = Field([], title="断言信息")
    extract_info: List[OutExtractInfo] = Field([], title="提取信息")


class OutCaseSimpleInfo(BaseModel):
    case_id: int = Field(..., title="用例id")
    directory_id: int = Field(..., title="环境目录")
    name: str = Field(..., title="用例名称")
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    priority: str = Field("P1", title="用例优先级: P0-P4")
