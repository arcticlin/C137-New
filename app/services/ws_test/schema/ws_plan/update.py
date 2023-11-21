# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/11/21
Description:
"""

from typing import List
from pydantic import BaseModel, Field


class RequestUpdatePlan(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    plan_desc: str = Field(..., description="计划描述")
    plan_status: int = Field(..., description="计划状态")


class RequestRemovePlanCase(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    case_id: List[int] = Field(..., description="用例ID")


class RequestAddPlanCase(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    case_id: List[int] = Field(..., description="用例ID")
