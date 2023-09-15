# coding=utf-8
"""
File: api_case_schemas.py
Author: bot
Created: 2023/9/15
Description:
"""
import json
from typing import Union

from pydantic import BaseModel, Field, validator
from loguru import logger


class Orm2CaseBaseInfo(BaseModel):
    name: str = Field(..., title="用例名称")
    request_type: int = Field(1, title="请求类型, 1: http, 2: grpc")
    status: int = Field(1, title="用例状态, 1: debug, 2: close, 3: normal")
    priority: str = Field("P1", title="用例优先级: P0-P4")
    case_type: int = Field(1, title="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")
    directory_id: int = Field(None, title="目录id")
    # tag: list[str]


class Orm2CaseUrl(BaseModel):
    url: str
    method: str


class Orm2CaseBody(BaseModel):
    body_type: int = Field(..., title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")

    @validator("body", pre=True, always=True)
    def convert_to_json(cls, v, values):
        # 如果body_type为1并且body不为空，则尝试将body解析为JSON
        if values.get("body_type") == 1 and v:
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
                return v
                # raise ValueError("Invalid JSON format")


class Orm2CaseParams(BaseModel):
    path_id: str = Field(None, title="id")
    key: str = Field(..., title="参数名")
    types: int = Field(..., title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(None, title="参数值")
    enable: bool = Field(..., title="是否启用")
    comment: str = Field(None, title="备注")


class Orm2CaseHeader(BaseModel):
    header_id: str = Field(None, title="id")
    key: str
    value_type: int
    value: str
    enable: bool
    comment: str = Field(None, title="备注")

    @validator("value", pre=True, always=True)
    def convert_to_json(cls, v, values):
        # 参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON
        try:
            vt = values.get("value_type")
            if vt == 1 and v:
                return v
            elif vt == 2 and v:
                return int(v)
            elif vt == 3 and v:
                if v.upper() == "TRUE":
                    return True
                elif v.upper == "FALSE":
                    return False
                elif v == "1":
                    return True
                else:
                    return False
            else:
                return json.loads(v)
        except json.JSONDecodeError:
            # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
            logger.error(f"无法转换 value: {v}为{values.get('value_type')}类型")
            return v


class Orm2CaseSuffix(BaseModel):
    suffix_id: int = Field(None, description="前/后置ID")
    suffix_type: int
    name: str
    enable: bool
    sort: int
    execute_type: int
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")
    run_each_case: bool = Field(None, description="是否每个用例都运行")
    run_out_name: str = Field(None, description="出参")
    description: str = Field(None, description="描述")
    script_id: int = Field(None, description="脚本id")
    sql_id: int = Field(None, description="sql id")
    redis_id: int = Field(None, description="redis id")
    run_case_id: int = Field(None, description="执行用例id")
    run_delay: int = Field(None, description="延迟时间")
    run_command: str = Field(None, description="执行命令")
    fetch_one: bool = Field(None, description="是否只取一条数据")


class Orm2CaseAssert(BaseModel):
    assert_id: int = Field(None, description="断言id")
    name: str = Field(..., description="断言名称")
    enable: bool = Field(..., description="是否启用")
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")
    assert_from: int = Field(..., description="断言来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    assert_type: int = Field(
        ...,
        description="断言类型 1: equal 2: n-equal 3:GE 4: LE 5:in-list 6: not-in-list 7: contain 8: not-contain 9: start-with 10: end-with 11: Re_Gex 12:Json-Path",
    )
    assert_exp: str = Field(None, description="断言表达式")
    assert_value: str = Field(..., description="断言值")


class Orm2CaseExtract(BaseModel):
    extract_id: int = Field(None, description="提取id")
    name: str = Field(..., description="提取名称")
    description: str = Field(None, description="提取描述")
    enable: bool = Field(..., description="是否启用")
    case_id: int = Field(None, description="用例id")
    extract_from: int = Field(..., description="提取来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    extract_type: int = Field(..., description="提取类型 1: Json-Path 2: Re_Gex")
    extract_exp: str = Field(None, description="提取表达式")
    extract_out_name: str = Field(..., description="提取值")
    extract_index: int = Field(None, description="提取索引")


class OrmFullCase(BaseModel):
    case_id: int = Field(None)
    env_id: int = Field(None, title="环境id")
    directory_id: int = Field(None, title="环境目录")
    basic_info: Orm2CaseBaseInfo = Field(None, title="基础信息")
    url_info: Orm2CaseUrl = Field(None, title="url信息")
    body_info: Orm2CaseBody = Field(None, title="body信息")
    query_info: list[Orm2CaseParams] = Field([], title="请求参数")
    path_info: list[Orm2CaseParams] = Field([], title="请求参数")
    header_info: list[Orm2CaseHeader] = Field([], title="请求头")
    prefix_info: list[Orm2CaseSuffix] = Field([], title="前置处理")
    suffix_info: list[Orm2CaseSuffix] = Field([], title="后置处理")
    assert_info: list[Orm2CaseAssert] = Field([], title="断言")
    extract_info: list[Orm2CaseExtract] = Field([], title="提取")
