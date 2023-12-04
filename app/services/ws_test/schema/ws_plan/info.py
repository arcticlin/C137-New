# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/21
Description:
"""

from pydantic import BaseModel, Field


class OutPlanBasicInfo(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    plan_desc: str = Field(..., description="计划描述")
    plan_status: int = Field(..., description="计划状态")
    case_count: int = Field(..., description="用例数量")
    created_at: int = Field(..., description="创建时间")
    create_user: str = Field(..., description="创建人")


class RequestQueryPlanList(BaseModel):
    page: int = Field(1, description="")
