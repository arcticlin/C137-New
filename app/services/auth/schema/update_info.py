# coding=utf-8
"""
File: update_info.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse


class UserUpdateRequest(BaseModel):
    nickname: str = Field(None, description="昵称", max_length=16)
    email: str = Field(None, description="邮箱")
    avatar: str = Field(None, description="头像")


class UserModifyPasswordRequest(BaseModel):
    old_password: str = Field(..., description="旧密码", max_length=16)
    new_password: str = Field(..., description="新密码", max_length=16)


class UserResetPasswordRequest(BaseModel):
    account: str = Field(..., description="用户id")
    reset_code: str = Field(..., description="重置密码token", min_length=6, max_length=6)
    new_password: str = Field(..., description="新密码", max_length=16)
