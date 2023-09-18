# coding=utf-8
"""
File: api_case_schema_new_new.py
Author: bot
Created: 2023/9/15
Description:
"""
import json
from typing import Union, Optional

from pydantic import BaseModel, Field, validator


class CaseBasicInfoAdd(BaseModel):
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
                return json.dumps(v, ensure_ascii=False)
        except json.JSONDecodeError:
            # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
            return str(v)


class CaseBodyUpdate(BaseModel):
    body_type: int = Field(None, title="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body: Union[str, dict, list] = Field(None, title="请求体数据")

    # @validator("body", pre=True, always=True)
    # def convert_to_str(cls, v, values):
    #     # 如果body_type为1并且body不为空，则尝试将body解析为JSON
    #     try:
    #         if isinstance(v, dict) or isinstance(v, list):
    #             return json.dumps(v, ensure_ascii=False)
    #     except json.JSONDecodeError:
    #         # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
    #         return str(v)


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


class CaseSuffixAdd(BaseModel):
    suffix_type: int = Field(..., title="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., title="前/后置名称")
    enable: Optional[bool] = Field(True, title="是否启用")
    sort: int = Field(..., title="排序")
    execute_type: int = Field(..., title="执行类型, 1: 用例, 2: 脚本, 3: sql, 4: redis, 5: 延迟, 6: 命令")
    case_id: Optional[int] = Field(None, description="用例id")
    env_id: Optional[int] = Field(None, description="环境id")
    run_each_case: Optional[bool] = Field(None, description="是否每个用例都运行")
    run_out_name: Optional[str] = Field(None, description="出参")
    description: Optional[str] = Field(None, description="描述")
    script_id: Optional[int] = Field(None, description="脚本id")
    sql_id: Optional[int] = Field(None, description="sql id")
    redis_id: Optional[int] = Field(None, description="redis id")
    run_case_id: Optional[int] = Field(None, description="执行用例id")
    run_delay: Optional[int] = Field(None, description="延迟时间")
    run_command: Optional[str] = Field(None, description="执行命令")
    fetch_one: Optional[int] = Field(None, description="是否只取一条数据")


class CaseSuffixUpdate(BaseModel):
    suffix_id: int = Field(..., description="前/后置ID")
    suffix_type: int = Field(None, title="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(None, title="前/后置名称")
    enable: Optional[bool] = Field(True, title="是否启用")
    sort: int = Field(None, title="排序")
    execute_type: int = Field(None, title="执行类型, 1: 用例, 2: 脚本, 3: sql, 4: redis, 5: 延迟, 6: 命令")
    case_id: Optional[int] = Field(None, description="用例id")
    env_id: Optional[int] = Field(None, description="环境id")
    run_each_case: Optional[bool] = Field(None, description="是否每个用例都运行")
    run_out_name: Optional[str] = Field(None, description="出参")
    description: Optional[str] = Field(None, description="描述")
    script_id: Optional[int] = Field(None, description="脚本id")
    sql_id: Optional[int] = Field(None, description="sql id")
    redis_id: Optional[int] = Field(None, description="redis id")
    run_case_id: Optional[int] = Field(None, description="执行用例id")
    run_delay: Optional[int] = Field(None, description="延迟时间")
    run_command: Optional[str] = Field(None, description="执行命令")
    fetch_one: Optional[int] = Field(None, description="是否只取一条数据")


class CaseAssertAdd(BaseModel):
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


class CaseAssertUpdate(BaseModel):
    assert_id: int = Field(..., description="断言id")
    name: str = Field(None, description="断言名称")
    enable: bool = Field(None, description="是否启用")
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")
    assert_from: int = Field(None, description="断言来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    assert_type: int = Field(
        None,
        description="断言类型 1: equal 2: n-equal 3:GE 4: LE 5:in-list 6: not-in-list 7: contain 8: not-contain 9: start-with 10: end-with 11: Re_Gex 12:Json-Path",
    )
    assert_exp: str = Field(None, description="断言表达式")
    assert_value: str = Field(None, description="断言值")


class CaseExtractAdd(BaseModel):
    extract_id: int = Field(..., description="提取id")
    name: str = Field(..., description="提取名称")
    description: str = Field(None, description="提取描述")
    enable: bool = Field(..., description="是否启用")
    case_id: int = Field(None, description="用例id")
    extract_from: int = Field(..., description="提取来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    extract_type: int = Field(..., description="提取类型 1: Json-Path 2: Re_Gex")
    extract_exp: str = Field(None, description="提取表达式")
    extract_out_name: str = Field(..., description="提取值")
    extract_index: int = Field(None, description="提取索引")


class CaseExtractUpdate(BaseModel):
    extract_id: int = Field(..., description="提取id")
    name: str = Field(None, description="提取名称")
    description: str = Field(None, description="提取描述")
    enable: bool = Field(None, description="是否启用")
    case_id: int = Field(None, description="用例id")
    extract_from: int = Field(None, description="提取来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    extract_type: int = Field(None, description="提取类型 1: Json-Path 2: Re_Gex")
    extract_exp: str = Field(None, description="提取表达式")
    extract_out_name: str = Field(None, description="提取值")
    extract_index: int = Field(None, description="提取索引")


class CaseFullAdd(BaseModel):
    directory_id: int = Field(..., title="环境目录")
    basic_info: CaseBasicInfoAdd = Field(..., title="基础信息")
    url_info: CaseUrlAdd = Field(..., title="url信息")
    body_info: CaseBodyAdd = Field(..., title="body信息")
    query_info: list[CaseParamsAdd] = Field([], title="请求参数")
    path_info: list[CaseParamsAdd] = Field([], title="请求参数")
    header_info: list[CaseHeaderAdd] = Field([], title="请求头")
    prefix_info: list[CaseSuffixAdd] = Field([], title="前置处理")
    suffix_info: list[CaseSuffixAdd] = Field([], title="后置处理")
    assert_info: list[CaseAssertAdd] = Field([], title="断言")
    extract_info: list[CaseExtractAdd] = Field([], title="提取")


class CaseFullUpdate(BaseModel):
    case_id: int = Field(..., title="用例id")
    directory_id: int = Field(None, title="环境目录")
    basic_info: CaseBasicInfoAdd = Field(None, title="基础信息")
    url_info: CaseUrlAdd = Field(None, title="url信息")
    body_info: CaseBodyUpdate = Field(None, title="body信息")
    query_info: list[CaseParamsAdd] = Field(None, title="请求参数")
    path_info: list[CaseParamsAdd] = Field(None, title="请求参数")
    header_info: list[CaseHeaderAdd] = Field(None, title="请求头")
    prefix_info: list[CaseSuffixAdd] = Field(None, title="前置处理")
    suffix_info: list[CaseSuffixAdd] = Field(None, title="后置处理")
    assert_info: list[CaseAssertAdd] = Field(None, title="断言")
    extract_info: list[CaseExtractAdd] = Field(None, title="提取")


class CaseFullOut(BaseModel):
    case_id: int = Field(..., title="用例id")
    directory_id: int = Field(..., title="环境目录")
    basic_info: CaseBasicInfoAdd = Field(..., title="基础信息")
    url_info: CaseUrlAdd = Field(..., title="url信息")
    body_info: CaseBodyAdd = Field(..., title="body信息")
    query_info: list[CaseParamsAdd] = Field([], title="请求参数")
    path_info: list[CaseParamsAdd] = Field([], title="请求参数")
    header_info: list[CaseHeaderAdd] = Field([], title="请求头")
    prefix_info: list[CaseSuffixAdd] = Field([], title="前置处理")
    suffix_info: list[CaseSuffixAdd] = Field([], title="后置处理")
    assert_info: list[CaseAssertAdd] = Field([], title="断言")
    extract_info: list[CaseExtractAdd] = Field([], title="提取")
