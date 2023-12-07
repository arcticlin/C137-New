# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/11/21
Description:
"""
from typing import List

from pydantic import BaseModel, Field


class RequestAddWsPlan(BaseModel):
    ...


class RequestAddWsPlanCase(BaseModel):
    ws_id: int = Field(..., description="WS ID")
    case_list: List[int] = Field(..., description="用例列表")


class RequestNewWsPlan(BaseModel):
    plan_desc: str = Field(..., description="计划描述")
    suites: List[RequestAddWsPlanCase] = Field(..., description="套件列表")


class OutAddWsPlan(BaseModel):
    plan_id: int = Field(..., description="计划ID")


class RequestTestConnect(BaseModel):
    ws_url: str = Field(..., description="WS URL")


class RequestTestRunCase(BaseModel):
    case_id: int
