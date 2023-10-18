from fastapi.security import APIKeyHeader
from base_config import Config
from fastapi import Depends
from app.exceptions.custom_exception import CustomException
from app.exceptions.auth_exp_410 import *
from app.handler.auth.token_handler import UserToken
from datetime import datetime
from app.handler.redis.rds_client import RedisCli


class Permission:
    oauth_scheme = APIKeyHeader(name="Authorization")

    def __init__(self, role: int = Config.U_MEMBER, refresh: bool = False):
        self.role = role
        self.refresh = refresh
        self.rds = RedisCli()

    async def __call__(self, token: str = Depends(oauth_scheme)):
        if not token:
            raise CustomException(AUTH_WITHOUT_TOKEN)
        user_info = UserToken.parse_token(token)

        # 给user_info加token信息, 方便解析
        user_info["token"] = token

        # 刷新Token的机制, 当self.refresh为True, 跳过过期和身份认证
        if self.refresh:
            return user_info

        # 强验证Token, 当不存在Redis里就无法通过Token验证
        if Config.TOKEN_STRONG_VERIFY:
            redis_token = await self.rds.get_key_value_as_json(f"ut:user_token_{user_info['user_id']}")

            if redis_token is None or redis_token == {}:
                raise CustomException(TOKEN_IS_INVALID)
            if token != redis_token["token"]:
                await self.rds.delete(f"ut:user_token_{user_info['user_id']}")
                raise CustomException(TOKEN_IS_INVALID)

        # 超时Token校验
        if int(datetime.now().timestamp()) > user_info.get("exp"):
            raise CustomException(TOKEN_IS_EXPIRED)
        # Token权限校验
        if user_info.get("user_role", 0) < self.role:
            raise CustomException(AUTH_NOT_PERMISSION)

        return user_info
