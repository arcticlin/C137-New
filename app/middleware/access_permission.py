# coding=utf-8
"""
File: access_permission.py
Author: bot
Created: 2023/7/27
Description:
"""
from fastapi.security import APIKeyHeader
from base_config import Config
from fastapi import Depends
from app.exceptions.commom_exception import CustomException
from app.exceptions.auth_exp import *
from app.handler.token_handler import UserToken
from datetime import datetime


class Permission:
    oauth_scheme = APIKeyHeader(name="Authorization")

    def __init__(self, role: int = Config.U_MEMBER, refresh: bool = False):
        self.role = role
        self.refresh = refresh

    async def __call__(self, token: str = Depends(oauth_scheme)):
        if not token:
            raise CustomException(AUTH_WITHOUT_TOKEN)
        user_info = UserToken.parse_token(token)
        # 给user_info加token信息, 方便解析
        user_info["token"] = token
        # 刷新Token的机制, 当self.refresh为True, 跳过过期和身份认证
        if self.refresh:
            return user_info
        # 检查Redis中的Token信息
        # if await AuthRedis.get_user_info(user_id=user_info["user_id"]) is None:
        #     raise CustomException(TOKEN_IS_INVALID)
        # 超时Token校验
        if int(datetime.now().timestamp()) > user_info.get("exp"):
            raise CustomException(TOKEN_IS_EXPIRED)
        # Token权限校验
        if user_info.get("role", 0) < self.role:
            raise CustomException(AUTH_NOT_PERMISSION)

        return user_info
