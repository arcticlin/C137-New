# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""
from pydantic import BaseModel, Field


class OutCaseSuffixInfo(BaseModel):
    suffix_id: int = Field(..., description="前/后置ID")
    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., description="前/后置名称")
    enable: bool = Field(..., description="是否启用")
    sort: int = Field(..., description="排序")
    execute_type: int = Field(..., description="执行类型,  1: 公共脚本 2: sql 3: redis 4: delay 5: python")
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


class DebugCaseSuffixInfo(BaseModel):
    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., description="前/后置名称")
    enable: bool = Field(..., description="是否启用")
    sort: int = Field(..., description="排序")
    execute_type: int = Field(..., description="执行类型, 1: 公共脚本 2: sql 3: redis 4: delay 5: python")
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
