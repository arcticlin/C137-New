# coding=utf-8
"""
File: admin.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse


class AdminAssignNewRoleRequest(BaseModel):
    user_id: int = Field(..., description="用户id")
    user_role: int = Field(..., description="用户权限")


class AdminBanRequest(BaseModel):
    user_id: int = Field(..., description="用户id")
    valid: bool = Field(..., description="账号可用状态")


class AdminGenerateCodeRequest(BaseModel):
    account: str = Field(..., description="需要生成重置码的账号")


class OutResetCode(BaseModel):
    reset_code: str = Field(..., description="重置码")


class ResponseResetCode(CommonResponse):
    data: OutResetCode
