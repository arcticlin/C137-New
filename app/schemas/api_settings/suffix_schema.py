# coding=utf-8
"""
File: suffix_schema.py
Author: bot
Created: 2023/8/14
Description:
"""
from pydantic import BaseModel, Field, root_validator


class SuffixSimpleShow(BaseModel):
    suffix_id: int = Field(..., description="前/后置ID")
    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., description="前/后置名称")
    enable: bool = Field(..., description="是否启用")
    sort: int = Field(..., description="排序")
    execute_type: int = Field(..., description="执行类型, 1: python 2: sql 3: redis 4: delay 5: global-script")
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")
    run_each_case: bool = Field(..., description="是否每个用例都运行")
    run_out_name: str = Field(None, description="出参")
    description: str = Field(None, description="描述")


class AddSuffixSchema(BaseModel):
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")

    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., description="前/后置名称")
    enable: bool = Field(..., description="是否启用")
    description: str = Field(None, description="描述")
    execute_type: int = Field(..., description="执行类型, 1: python 2: sql 3: redis 4: delay 5: global-script")
    run_each_case: int = Field(None, description="是否每个用例都运行")

    script_id: int = Field(None, description="脚本id")
    sql_id: int = Field(None, description="sql id")
    redis_id: int = Field(None, description="redis id")
    run_case_id: int = Field(None, description="执行用例id")

    run_delay: int = Field(None, description="延迟时间")
    run_command: str = Field(None, description="执行命令")
    run_out_name: str = Field(None, description="出参")
    fetch_one: bool = Field(None, description="是否只取一条数据")

    @root_validator(pre=True)
    def check_ids(cls, values):
        case_id = values.get("case_id")
        env_id = values.get("env_id")
        if case_id is None and env_id is None:
            raise ValueError("At least one of 'case_id' or 'env_id' must be provided")
        return values


class DeleteSuffixSchema(BaseModel):
    suffix_id: int = Field(..., description="前/后置ID")
    case_id: int = Field(None, description="用例id")
    env_id: int = Field(None, description="环境id")
    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")


class EnableSuffixSchema(BaseModel):
    suffix_id: int = Field(..., description="前/后置ID")
    enable: bool = Field(..., description="是否启用")


class SchemaCaseSuffix(BaseModel):
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
