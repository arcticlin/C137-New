# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/21
Description:
"""
from pydantic import BaseModel, Field


class OutWsCaseBasicInfo(BaseModel):
    case_id: int
    ws_id: int
    case_desc: str
    case_status: int
    create_user: int
