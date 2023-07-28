# coding=utf-8
"""
File: admin.py
Author: bot
Created: 2023/7/28
Description:
"""

from fastapi import APIRouter, Depends
from app.middleware.access_permission import Permission
from app.schemas.admin.admin_schema import AdminResetCode
from app.schemas.auth.user import UserUpdateRoleRequest, UserUpdateBanRequest
from app.schemas.response_schema import CommonResponse
from app.services.auth.auth_service import AuthService
from app.handler.response_handler import C137Response

admin = APIRouter()


@admin.post("/reset_code", summary="生成重置密码验证码", response_model=CommonResponse)
async def generate_reset_code(data: AdminResetCode, user_info=Depends(Permission(role=2))):
    reset_code = await AuthService.admin_generate_reset_code(data.account)
    return C137Response.success(data={"reset_code": reset_code})


@admin.put("/update_user_role", summary="更新用户身份")
async def update_user_role(data: UserUpdateRoleRequest, user_info: dict = Depends(Permission(role=2))):
    await AuthService.admin_update_user_role(data)
    return C137Response.success(message="操作成功")


@admin.put(
    "/ban_user",
    summary="禁用用户",
)
async def ban_user(data: UserUpdateBanRequest, user_info: dict = Depends(Permission(role=2))):
    await AuthService.admin_ban_user(data)
    return C137Response.success(message="操作成功")
