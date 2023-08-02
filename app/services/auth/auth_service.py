# coding=utf-8
"""
File: auth_service.py
Author: bot
Created: 2023/7/25
Description: Auth服务
"""
import json, string, secrets

from app.handler.token_handler import UserToken
from app.schemas.admin.admin_schema import AdminResetCode
from app.utils.new_logger import logger
from app.schemas.auth.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserUpdateRequest,
    UserModifyPasswordRequest,
    UserResetPasswordRequest,
    UserUpdateRoleRequest,
    UserUpdateBanRequest,
)
from app.crud.auth.auth_crud import AuthCrud
from app.handler.response_handler import C137Response
from app.exceptions.commom_exception import CustomException
from app.exceptions.auth_exp import *
from app.handler.response_handler import C137Response
from app.handler.redis_handler import redis_client


class AuthService:
    @staticmethod
    async def set_token_in_redis(user_id: int, user_token: str, user_token_expired: int):
        user_token_info = {"token": user_token, "expired": user_token_expired}
        await redis_client.set(f"ut:user_token_{user_id}", json.dumps(user_token_info), ex=3600 * 24 * 3)

    @staticmethod
    async def get_token_in_redis(user_id: int):
        user_token_info = await redis_client.get(f"ut:user_token_{user_id}")
        try:
            json_user_token_info = json.loads(user_token_info)
            return json_user_token_info
        except Exception as e:
            return user_token_info

    @staticmethod
    async def get_user_info_by_id(user_id: int):
        user_info = await AuthCrud.get_user_by_id(user_id)
        return user_info

    @staticmethod
    async def register_user(register_form: UserRegisterRequest):
        if await AuthCrud.get_user_by_account(register_form.account):
            raise CustomException(ACCOUNT_EXISTS)
        # 密码加盐
        if register_form.password:
            register_form.password = UserToken.add_salt(register_form.password)

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
        # 记录最后登录时间
        await AuthCrud.record_last_login_time(user.user_id)
        # 记录Redis
        await AuthService.set_token_in_redis(user_orm["user_id"], token, expired_time)
        return user_orm

    @staticmethod
    async def user_logout(user_id: int):
        await redis_client.delete(f"ut:user_token_{user_id}")
        return True

    @staticmethod
    async def update_user_info(user_id: int, data: UserUpdateRequest):
        if await AuthCrud.get_user_by_nickname(data.nickname):
            raise CustomException(NICKNAME_EXISTS)
        await AuthCrud.update_user_info(user_id, data.dict())

    @staticmethod
    async def update_user_password(user_id: int, data: UserModifyPasswordRequest):
        user = await AuthCrud.get_user_by_id(user_id)
        if UserToken.add_salt(data.old_password) != user.password:
            raise CustomException(PASSWORD_INCORRECT)
        await AuthCrud.update_user_password(user_id, data.new_password)
        return True

    @staticmethod
    async def refresh_token(user_id: int, old_token: str):
        user_in_redis = await AuthService.get_token_in_redis(user_id)
        if user_in_redis is None:
            raise CustomException(TOKEN_IS_INVALID)
        if user_in_redis["token"] != old_token:
            raise CustomException(TOKEN_IS_INVALID)
        user_info = await AuthCrud.get_user_by_id(user_id)
        user_orm = C137Response.orm_to_dict(
            user_info,
            "password",
            "valid",
        )
        expired_time, token = UserToken.encode_token(user_orm)
        user_orm["expired_at"] = expired_time
        user_orm["token"] = token
        # 记录最后登录时间
        await AuthCrud.record_last_login_time(user_info.user_id)
        # 记录Redis
        await AuthService.set_token_in_redis(user_orm["user_id"], token, expired_time)
        return user_orm

    @staticmethod
    async def admin_generate_reset_code(account: str):
        await AuthCrud.get_user_by_account(account)
        characters = string.ascii_letters + string.digits
        reset_code = "".join(secrets.choice(characters) for _ in range(6))
        await redis_client.set(f"ut:reset_code_{account}", reset_code, ex=60 * 5)
        return reset_code

    @staticmethod
    async def reset_password(data: UserResetPasswordRequest):
        reset_code = await redis_client.get(f"ut:reset_code_{data.account}")
        if reset_code != data.reset_code:
            raise CustomException(RESET_CODE_INCORRECT)
        await AuthCrud.reset_user_password(data.account, data.new_password)
        await redis_client.delete(f"ut:reset_code_{data.account}")
        return True

    @staticmethod
    async def admin_update_user_role(data: UserUpdateRoleRequest):
        await AuthCrud.update_user_role(data.user_id, data.user_role)
        return True

    @staticmethod
    async def admin_ban_user(data: UserUpdateBanRequest):
        await AuthCrud.update_user_ban(data.user_id, data.valid)
        return True
