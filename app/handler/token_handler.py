# coding=utf-8
"""
File: token_handler.py
Author: bot
Created: 2023/7/27
Description:
"""
import hashlib
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError
from app.exceptions.auth_exp import *
from app.exceptions.commom_exception import CustomException
from typing import Dict
from base_config import Config
from app.utils.new_logger import logger


class UserToken:
    @staticmethod
    def add_salt(password: str) -> str:
        # 密码加盐
        m = hashlib.md5()

        salty = f"{password}@{Config.TOKEN_SALT}".encode("utf-8")

        m.update(salty)

        return m.hexdigest()

    @staticmethod
    def encode_token(payload: dict) -> tuple[int, str]:
        """
        生成token, 并返回过期时间戳和token
        """
        expired = datetime.now() + timedelta(minutes=Config.EXPIRED_MIN)
        encode_payload = dict({"exp": expired}, **payload)
        return int(expired.timestamp()), jwt.encode(encode_payload, key=Config.TOKEN_KEY)

    @staticmethod
    def parse_token(token: str) -> Dict:
        try:
            return jwt.decode(token, key=Config.TOKEN_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise CustomException(TOKEN_IS_EXPIRED)
        except Exception as e:
            raise CustomException(TOKEN_IS_INVALID)

    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        token_info = UserToken.parse_token(token)
        return str(token_info["user_id"])