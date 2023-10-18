# coding=utf-8
"""
File: register.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class UserRegisterRequest(BaseModel):
    account: str = Field(..., description="账号", max_length=32)
    password: str = Field(..., description="密码", min_length=4, max_length=16)


class UserRegisterOut(BaseModel):
    user_id: int = Field(..., description="用户id")


class ResponseRegister(CommonResponse):
    data: UserRegisterOut = Field(..., description="返回用户ID")
