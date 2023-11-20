# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/11/20
Description:
"""

from pydantic import BaseModel, Field


class RequestUpdateWsCode(BaseModel):
    ws_id: int
    project_id: int
    code_value: int
    desc: str
    status: int
