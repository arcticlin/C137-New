# coding=utf-8
"""
File: auth_service.py
Author: bot
Created: 2023/7/25
Description: Auth服务
"""
from app.handler.token_handler import UserToken
from app.utils.logger import Log
from app.schemas.auth.user import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
)
from app.crud.auth.auth_crud import AuthCrud
from app.handler.response_handler import C137Response
from app.exceptions.commom_exception import CustomException
from app.exceptions.auth_exp import *
from app.handler.response_handler import C137Response


class AuthService:
    @staticmethod
    async def set_token_in_redis():
        pass

    @staticmethod
    async def register_user(register_form: UserRegisterRequest):
        if await AuthCrud.get_user_by_account(register_form.account):
            raise CustomException(ACCOUNT_EXISTS)
        if await AuthCrud.get_user_by_nickname(register_form.nickname):
            raise CustomException(ACCOUNT_EXISTS)
        # 密码加盐
        if register_form.password:
            register_form.password = UserToken.add_salt(register_form.password)
        # 初始化用户昵称
        if "@" in register_form.account and not register_form.nickname:
            register_form.nickname = register_form.account.split("@")[0]
        await AuthCrud.register_user(register_form)
        return True

    @staticmethod
    async def login_user(form: UserLoginRequest):
        # 检查已注册
        user = await AuthCrud.get_user_by_account(form.account)
        if not user:
            raise CustomException(ACCOUNT_NOT_EXISTS)
        # 检查密码
        if user.password != UserToken.add_salt(form.password):
            raise CustomException(PASSWORD_INCORRECT)
        # 检查账户状态
        if user.valid == 0:
            raise CustomException(ACCOUNT_IS_BANNED)
        # 生成token
        user_orm = C137Response.orm_to_dict(
            user,
            "password",
            "valid",
        )
        expired_time, token = UserToken.encode_token(user_orm)
        user_orm["expired_at"] = expired_time
        user_orm["token"] = token

        return user_orm
