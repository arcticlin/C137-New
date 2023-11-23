# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/11/21
Description:
"""

from pydantic import BaseModel, Field


class RequestUpdateWsCase(BaseModel):
    case_id: int
    case_desc: str
    case_status: int
    json_exp: str = Field(None, description="json格式的期望值")
    expected: str = Field(None, description="期望值")
