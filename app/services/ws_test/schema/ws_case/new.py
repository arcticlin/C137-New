# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel

from app.core.basic_schema import CommonResponse


class RequestAddWsCase(BaseModel):
    ws_id: int
    case_desc: str


class OutAddWsCase(BaseModel):
    case_id: int
