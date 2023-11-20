# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/11/20
Description:
"""
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class RequestAddWsCode(BaseModel):
    project_id: int
    code_value: int
    desc: str


class OutAfterNew(BaseModel):
    ws_id: int


class ResponseAddWsCode(CommonResponse):
    data: OutAfterNew = Field(..., description="添加WS_CODE后返回的ID")
