# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel, Field


class OutResultBasicInfo(BaseModel):
    result_id: int
    case_id: int
    result_desc: str
    result_status: int


class OutStaticPlanResult(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    plan_desc: str = Field(..., description="计划描述")
    case_total: int = Field(0, description="用例总数")
    case_pass: int = Field(0, description="用例通过数")
    case_fail: int = Field(0, description="用例失败数")
    case_ignore: int = Field(0, description="用例忽略数")
    case_not_run: int = Field(0, description="用例未执行数")


class RequestMarkCase(BaseModel):
    result_id: int = Field(..., description="结果ID")
    result_status: int = Field(..., description="结果状态")
    result_desc: str = Field(None, description="结果描述")
