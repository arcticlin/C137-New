# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel, Field


class OutWsCaseBasicInfo(BaseModel):
    case_id: int = Field(..., description="用例ID")
    ws_id: int = Field(..., description="WS_ID")
    case_desc: str = Field(..., description="用例描述")
    case_status: int = Field(..., description="用例状态")
    json_exp: str = Field(None, description="json格式的期望值")
    expected: str = Field(None, description="期望值")
    create_user: int
