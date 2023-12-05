# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/21
Description:
"""
from typing import List

from pydantic import BaseModel, Field


class OutPlanBasicInfo(BaseModel):
    plan_id: int = Field(..., description="计划ID")
    plan_desc: str = Field(..., description="计划描述")
    plan_status: int = Field(..., description="计划状态")
    case_count: int = Field(0, description="用例数量")
    created_at: int = Field(..., description="创建时间")
    create_user: str = Field(..., description="创建人")


class RequestQueryPlanList(BaseModel):
    page: int = Field(1, description="页码")
    page_size: int = Field(10, description="条数")
    filter_user: List[int] = Field(None, description="筛选用户")
    filter_name: str = Field(None, description="筛选名称")
    filter_status: List[int] = Field(None, description="筛选状态")
    filter_project: List[int] = Field(None, description="筛选项目")
