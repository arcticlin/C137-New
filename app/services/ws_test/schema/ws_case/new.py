# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class RequestAddWsCase(BaseModel):
    ws_id: int = Field(None, description="ws_id")
    case_desc: str
    json_exp: str = Field(None, description="json格式的期望值")
    expected: str = Field(None, description="期望值")


class OutAddWsCase(BaseModel):
    case_id: int
