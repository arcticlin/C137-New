# coding=utf-8
"""
File: api_case_schema_new_new.py
Author: bot
Created: 2023/9/15
Description:
"""
import json
from typing import Union

from pydantic import BaseModel, Field, validator


class CaseBasicInfoNew(BaseModel):
    name: str = Field(..., title="用例名称")
    directory_id: int = Field(..., title="目录id")
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级: P0-P4")
    case_type: int = Field(1, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")


class CaseBasicInfoUpdate(BaseModel):
    name: str = Field(None, title="用例名称")
    directory_id: int = Field(None, title="目录id")
    request_type: int = Field(None, title="请求类型, 1: http, 2: grpc")
    status: int = Field(None, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field(None, title="用例优先级: P0-P4")
    case_type: int = Field(None, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")


class CaseUrlAdd(BaseModel):
    url: str = Field(..., title="请求地址")
    method: str = Field(..., title="请求方法")


class CaseUrlUpdate(BaseModel):
    url: str = Field(None, title="请求地址")
    method: str = Field(None, title="请求方法")


class CaseBodyAdd(BaseModel):
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")

    @validator("body", pre=True, always=True)
    def convert_to_str(cls, v, values):
        # 如果body_type为1并且body不为空，则尝试将body解析为JSON
        try:
            if isinstance(v, dict) or isinstance(v, list):
                return json.dumps(v)
        except json.JSONDecodeError:
            # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
            return str(v)


class CaseBodyUpdate(BaseModel):
    body_type: int = Field(None, title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")

    @validator("body", pre=True, always=True)
    def convert_to_str(cls, v, values):
        # 如果body_type为1并且body不为空，则尝试将body解析为JSON
        try:
            if isinstance(v, dict) or isinstance(v, list):
                return json.dumps(v)
        except json.JSONDecodeError:
            # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
            return str(v)


class CaseParamsAdd(BaseModel):
    key: str = Field(..., title="参数名")
    types: int = Field(..., title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(..., title="参数值")
    enable: bool = Field(True, title="是否启用")
    comment: str = Field(None, title="备注")


class CaseParamsUpdate(BaseModel):
    path_id: int = Field(..., title="path id")
    key: str = Field(None, title="参数名")
    types: int = Field(None, title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(None, title="参数值")
    enable: bool = Field(None, title="是否启用")
    comment: str = Field(None, title="备注")


class CaseHeaderAdd(BaseModel):
    key: str = Field(..., title="参数名")
    value_type: int = Field(..., title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(..., title="参数值")
    enable: bool = Field(True, title="是否启用")
    comment: str = Field(None, title="备注")


class CaseHeaderUpdate(BaseModel):
    header_id: int = Field(..., title="header id")
    key: str = Field(None, title="参数名")
    value_type: int = Field(None, title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(None, title="参数值")
    enable: bool = Field(None, title="是否启用")
    comment: str = Field(None, title="备注")
