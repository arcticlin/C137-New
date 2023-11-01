# coding=utf-8
"""
File: user.py
Author: bot
Created: 2023/10/18
Description:
"""
from fastapi import APIRouter, Depends

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.auth.auth_service import AuthService
from app.services.auth.crud.auth_crud import UserCrud
from app.services.auth.schema.info import ResponseUserList, ResponseUserInfo
from app.services.auth.schema.update_info import UserUpdateRequest, UserModifyPasswordRequest


user = APIRouter()


@user.get("/list", summary="获取用户列表", response_model=ResponseUserList)
async def get_user_list():
    user_list = await AuthService.get_user_list()
    return C137Response.success(data=user_list)


@user.get("/{user_id}/info", summary="获取用户信息", response_model=ResponseUserInfo)
async def get_user_info(user_id: int, user_info: dict = Depends(Permission())):
    user_info = await UserCrud.get_user_by_id(user_id)
    return C137Response.success(data=user_info)


@user.put("/update/info", summary="更新用户信息", response_model=CommonResponse)
async def update_user_info(data: UserUpdateRequest, user_info: dict = Depends(Permission())):
    await AuthService.update_user_info(user_info["user_id"], data)
    return C137Response.success(message="操作成功")


@user.put("/update/password", summary="更新用户密码")
async def update_password(data: UserModifyPasswordRequest, user_info: dict = Depends(Permission())):
    await AuthService.modify_password(data, user_info["user_id"])
    return C137Response.success(message="操作成功")
