# coding=utf-8
"""
File: user_center.py
Author: bot
Created: 2023/7/31
Description:
"""
from fastapi import APIRouter
from app.services.users.uc_services import UserCenterServices
from app.handler.response_handler import C137Response
from app.schemas.auth.user import UserListResponse

uc = APIRouter()


@uc.get("/list", summary="用户列表", response_model=UserListResponse)
async def get_platform_user_list():
    user_list = await UserCenterServices.get_platform_user()
    return C137Response.success(data=user_list)
