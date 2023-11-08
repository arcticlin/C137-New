# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/10/23
Description:
"""


from pydantic import BaseModel, Field


class ResponseSuffixInfo(BaseModel):
    suffix_id: int = Field(..., description="前/后置id")
    suffix_type: int = Field(..., description="前/后置类型, 1: 前置, 2: 后置")
    name: str = Field(..., description="前/后置名称")
    enable: bool = Field(..., description="是否启用")
    description: str = Field(None, description="描述")
    execute_type: int = Field(..., description="执行类型,  1: 公共脚本 2: sql 3: redis 4: delay 5: python 6: 用例")
    run_each_case: int = Field(None, description="是否每个用例都运行")

    script_id: int = Field(None, description="脚本id")
    sql_id: int = Field(None, description="sql id")
    redis_id: int = Field(None, description="redis id")
    run_case_id: int = Field(None, description="执行用例id")

    run_delay: int = Field(None, description="延迟时间")
    run_command: str = Field(None, description="执行命令")
    run_out_name: str = Field(None, description="出参")
    fetch_one: bool = Field(None, description="是否只取一条数据")
