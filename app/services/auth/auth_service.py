# coding=utf-8
"""
File: auth_service.py
Author: bot
Created: 2023/7/25
Description: Auth服务
"""
from app.utils.logger import Log
from app.schemas.auth.user import UserRegisterRequest, UserRegisterResponse
from app.crud.auth.auth_crud import AuthCrud
from app.handler.response_handler import C137Response


class AuthService:
    @staticmethod
    async def register_user(register_form: UserRegisterRequest):
        if await AuthCrud.get_user_by_account(register_form.account):
            raise Exception("账号已存在")
        if await AuthCrud.get_user_by_nickname(register_form.nickname):
            raise Exception("昵称已存在")
        user = await AuthCrud.register_user(register_form)
        result = C137Response.orm_to_dict(user)
        return result
