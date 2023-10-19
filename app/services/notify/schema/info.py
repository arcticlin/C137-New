# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/19
Description:
"""

from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse


class NotifyInfo(BaseModel):
    """消息通知Schema"""

    user_id: int = Field(..., title="用户id")
    message: str = Field(..., title="消息")
