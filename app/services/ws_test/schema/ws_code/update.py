# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/11/20
Description:
"""

from pydantic import BaseModel, Field


class RequestUpdateWsCode(BaseModel):
    code_value: int = None
    desc: str = None
    status: int = None
