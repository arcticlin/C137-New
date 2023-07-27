# coding=utf-8
"""
File: auth_router.py
Author: bot
Created: 2023/7/26
Description:
"""
from fastapi import APIRouter
from app.schemas.auth.user import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
)
from app.schemas.response_schema import CommonResponse
from app.services.auth.auth_service import AuthService
from app.handler.response_handler import C137Response

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
async def logout_user():
    pass


@auth.get("/user_info/{user_id}", summary="获取用户信息")
async def get_user_info(user_id: int):
    pass


@auth.post("/update_user_info", summary="更新用户信息")
async def update_user_info():
    pass


@auth.post("/update_password", summary="更新用户密码")
async def update_password():
    pass


@auth.post("/reset_password", summary="重置用户密码")
async def reset_password():
    pass


@auth.post("/refresh_token", summary="刷新token")
async def refresh_token():
    pass


@auth.put("/update_user_role", summary="更新用户权限")
async def update_user_role():
    pass


@auth.put("/ban_user", summary="禁用用户")
async def ban_user():
    pass
