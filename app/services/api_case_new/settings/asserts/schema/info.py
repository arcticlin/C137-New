# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""

from pydantic import BaseModel, Field


class OutAssertInfo(BaseModel):
    assert_id: int = Field(..., description="断言ID")
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


class DebugAssertInfo(BaseModel):
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