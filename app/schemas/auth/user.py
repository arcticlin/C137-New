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


class UserModelBase(BaseModel):
    user_id: int = Field(..., description="用户id")
    account: str = Field(..., description="登录账号")
    nickname: str = Field(..., description="昵称")
    email: str = Field(None, description="邮箱")
    user_role: UserRoleEnum = Field(None, description="用户权限, 1: 普通用户, 2: 管理员")
    department_id: int = Field(None, description="部门id")
    valid: bool = Field(None, description="账号可用状态")
    avatar: str = Field(None, description="头像")
    last_login: int = Field(None, description="记录最后一次登录时间")


class UserRegisterRequest(BaseModel):
    account: str
    password: str


class UserLoginRequest(BaseModel):
    account: str
    password: str


class UserUpdateRequest(BaseModel):
    nickname: str = Field(None, description="昵称")
    email: str = Field(None, description="邮箱")
    avatar: str = Field(None, description="头像")


class UserModifyPasswordRequest(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码")


class UserResetPasswordRequest(BaseModel):
    account: str = Field(..., description="用户id")
    reset_code: str = Field(..., description="重置密码token", min_length=6, max_length=6)
    new_password: str = Field(..., description="新密码")


class UserUpdateRoleRequest(BaseModel):
    user_id: int = Field(..., description="用户id")
    user_role: UserRoleEnum = Field(..., description="用户权限")


class UserUpdateBanRequest(BaseModel):
    user_id: int = Field(..., description="用户id")
    valid: bool = Field(..., description="账号可用状态")


class UserLoginShow(UserModelBase):
    expired_at: int = Field(None, description="过期时间")
    token: str = Field(None, description="token")


class UserLoginResponse(CommonResponse):
    data: UserLoginShow


class UserDetailResponse(CommonResponse):
    data: UserModelBase
