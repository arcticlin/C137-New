# coding=utf-8
"""
File: login.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class UserLoginRequest(BaseModel):
    account: str = Field(..., description="账号", max_length=32)
    password: str = Field(..., description="密码", min_length=4, max_length=16)


class UserLoginOut(BaseModel):
    user_id: int = Field(..., description="用户id")
    account: str = Field(..., description="登录账号")
    nickname: str = Field(..., description="昵称")
    email: str = Field(None, description="邮箱")
    user_role: int = Field(None, description="用户权限, 1: 普通用户, 2: 管理员")
    department_id: int = Field(None, description="部门id")
    valid: bool = Field(None, description="账号可用状态")
    avatar: str = Field(None, description="头像")
    token: str = Field(..., description="token")
    expired_at: int = Field(..., description="过期时间")
    last_login: int = Field(None, description="记录最后一次登录时间")


class ResponseLogin(CommonResponse):
    data: UserLoginOut = Field(..., description="返回登录信息")
