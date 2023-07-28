# coding=utf-8
"""
File: auth_router.py
Author: bot
Created: 2023/7/26
Description:
"""
from fastapi import APIRouter, Query, Header, Depends
from app.schemas.auth.user import *

from app.schemas.response_schema import CommonResponse
from app.services.auth.auth_service import AuthService
from app.handler.response_handler import C137Response
from app.middleware.access_permission import Permission

auth = APIRouter()


@auth.post(
    "/register",
    summary="注册账号",
    response_model=CommonResponse,
    response_model_exclude_none=True,
)
async def register_user(register_form: UserRegisterRequest):
    """
    注册账号
    """
    await AuthService.register_user(register_form)
    return C137Response.success(message="注册成功")


@auth.post(
    "/login",
    summary="登录账号",
    response_model=UserLoginResponse,
    response_model_exclude_none=True,
)
async def login_user(form: UserLoginRequest):
    user_info = await AuthService.login_user(form)
    return C137Response.success(data=user_info)


@auth.post("/logout", summary="登出账号")
async def logout_user(user_info: dict = Depends(Permission())):
    await AuthService.user_logout(user_info["user_id"])
    return C137Response.success(message="登出成功")


@auth.get("/user_info/{user_id}", summary="获取用户信息", response_model=UserDetailResponse)
async def get_user_info(user_id: int, user_info: dict = Depends(Permission())):
    user_info = await AuthService.get_user_info_by_id(user_id)
    return C137Response.success(data=user_info)


@auth.post("/update_user_info", summary="更新用户信息", response_model=CommonResponse)
async def update_user_info(data: UserUpdateRequest, user_info: dict = Depends(Permission())):
    await AuthService.update_user_info(user_info["user_id"], data)
    return C137Response.success(message="操作成功")


@auth.post("/update_password", summary="更新用户密码")
async def update_password(data: UserModifyPasswordRequest, user_info: dict = Depends(Permission())):
    await AuthService.update_user_password(user_info["user_id"], data)
    return C137Response.success(message="操作成功")


@auth.post("/reset_password", summary="重置用户密码")
async def reset_password(data: UserResetPasswordRequest):
    await AuthService.reset_password(data)
    return C137Response.success(message="操作成功")


@auth.post("/refresh_token", summary="刷新token", response_model=UserLoginResponse)
async def refresh_token(user_info: dict = Depends(Permission(refresh=True))):
    new_token = await AuthService.refresh_token(user_info["user_id"], user_info["token"])
    return C137Response.success(message="操作成功", data=new_token)
