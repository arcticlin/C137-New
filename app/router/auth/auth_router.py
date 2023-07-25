# coding=utf-8
"""
File: auth_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import APIRouter
from app.schemas.auth.user import UserRegisterRequest, UserRegisterResponse
from app.services.auth.auth_service import AuthService
from app.handler.response_handler import C137Response

auth = APIRouter()


@auth.post("/register", summary="注册账号", response_model=UserRegisterResponse)
async def register_user(register_form: UserRegisterRequest):
    """
    注册账号
    """
    register_info = await AuthService.register_user(register_form)
    return C137Response.success(data=register_info)
