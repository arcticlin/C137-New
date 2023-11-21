# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/11/21
Description:
"""

from typing import List
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse
from app.services.ws_test.schema.ws_plan.info import OutPlanBasicInfo
from app.services.ws_test.schema.ws_plan.new import OutAddWsPlan


class ResponsePlanAdd(CommonResponse):
    data: OutAddWsPlan = Field(..., description="计划ID")


class ResponsePlanList(CommonResponse):
    data: List[OutPlanBasicInfo] = Field(..., description="计划列表")
    total: int
