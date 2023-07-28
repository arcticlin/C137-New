# coding=utf-8
"""
File: admin_schema.py
Author: bot
Created: 2023/7/28
Description:
"""
from pydantic import BaseModel, Field


class AdminResetCode(BaseModel):
    account: str = Field(..., description="账号")
