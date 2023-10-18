# coding=utf-8
"""
File: admin.py
Author: bot
Created: 2023/10/9
Description:
"""
from fastapi import APIRouter, Depends

from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.core.basic_schema import CommonResponse
from app.services.auth.schema.admin import AdminBanRequest, AdminAssignNewRoleRequest, AdminGenerateCodeRequest, ResponseResetCode
from app.services.auth.auth_service import AuthService


admin = APIRouter()


@admin.post("/reset_code", summary="生成重置密码验证码", response_model=ResponseResetCode)
async def generate_reset_code(data: AdminGenerateCodeRequest, user_info=Depends(Permission(role=2))):
    reset_code = await AuthService.admin_generate_reset_code(data.account)
    return C137Response.success(data={"reset_code": reset_code})


@admin.put("/role", summary="更新用户身份", response_model=CommonResponse)
async def update_user_role(data: AdminAssignNewRoleRequest, user_info: dict = Depends(Permission(role=2))):
    await AuthService.admin_update_user_role(data, user_info["user_id"])
    return C137Response.success(message="操作成功")


@admin.put(
    "/ban",
    summary="禁用用户",
    response_model=CommonResponse
)
async def ban_user(data: AdminBanRequest, user_info: dict = Depends(Permission(role=2))):
    await AuthService.admin_ban_user(data)
    return C137Response.success(message="操作成功")