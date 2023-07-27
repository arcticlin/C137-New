# coding=utf-8
"""
File: user.py
Author: bot
Created: 2023/7/25
Description:
"""

from pydantic import BaseModel, Field
from app.enums.enum_user import UserRoleEnum
from app.schemas.response_schema import CommonResponse
from typing import Optional


class UserRegisterRequest(BaseModel):
    account: str
    password: str
    nickname: str = Field(None, description="昵称")
    email: str = Field(None, description="邮箱")
    user_role: UserRoleEnum = Field(None, description="用户权限, 1: 普通用户, 2: 管理员")
    department_id: int = Field(None, description="部门id")
    avatar: str = Field(None, description="头像")


class UserRegisterShow(BaseModel):
    user_id: int = Field(..., description="用户id", alias="id")
    account: str = Field(..., description="登录账号")
    nickname: str = Field(..., description="昵称")


class UserLoginRequest(BaseModel):
    account: str
    password: str


class UserLoginShow(BaseModel):
    user_id: int = Field(..., description="用户id")
    account: str = Field(..., description="登录账号")
    nickname: str = Field(..., description="昵称")
    email: str = Field(None, description="邮箱")
    user_role: UserRoleEnum = Field(..., description="用户权限, 1: 普通用户, 2: 管理员")
    department_id: int = Field(None, description="部门id")
    avatar: str = Field(None, description="头像")
    last_login: int = Field(None, description="最后登录时间")
    expired_at: int = Field(None, description="过期时间")
    token: str = Field(None, description="token")


class UserRegisterResponse(CommonResponse):
    data: Optional[UserRegisterShow] = None


class UserLoginResponse(CommonResponse):
    data: UserLoginShow
