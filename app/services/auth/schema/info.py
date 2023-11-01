# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/18
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class UserListOut(BaseModel):
    user_id: int = Field(..., description="用户id")
    nickname: str = Field(..., description="昵称")
    email: str = Field(None, description="邮箱")
    user_role: int = Field(..., description="用户权限, 1: 普通用户, 2: 管理员")
    department_id: int = Field(None, description="部门id")
    avatar: str = Field(None, description="头像")
    last_login: int = Field(None, description="上一次登录时间")


class ResponseUserList(CommonResponse):
    data: List[UserListOut] = Field([], description="返回用户列表信息")


class ResponseUserInfo(CommonResponse):
    data: UserListOut = Field(..., description="返回用户信息")
