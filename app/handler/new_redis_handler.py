# coding=utf-8
"""
File: new_redis_handler.py
Author: bot
Created: 2023/9/14
Description:
"""
import json
import sys
from typing import Union

from redis import asyncio as aioredis
from redis.asyncio import Redis

from app.utils.new_logger import logger
from base_config import Config


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PWD,
            db=Config.REDIS_DB,
            decode_responses=True,
        )

    async def init_redis_connect(self):
        """初始化连接"""
        try:
            await self.ping()
        except aioredis.TimeoutError:
            logger.error("连接超时")
            sys.exit()
        except aioredis.AuthenticationError:
            logger.error("验证失败")
            sys.exit()
        except Exception as e:
            logger.error(f"Redis连接异常: {e}")
            sys.exit()

    async def set_kv(self, key: str, obj: dict, expired: int = None):
        """设置键值对"""
        await self.set(key, json.dumps(obj), ex=expired)

    async def get_kv(self, key: str):
        """获取键值对"""
        value = await self.get(key)
        try:
            return json.loads(value)
        except Exception as e:
            return {}

    async def set_env_var(self, env_id: int, user_id: int, value: dict):
        """
        设置环境变量,存储格式: env_var_{env_id}_{user_id}, 保存3天
        """
        await self.set_kv(f"e:e_{env_id}_{user_id}", value, expired=600 * 60 * 24 * 3)

    async def get_env_var(self, env_id: int, user_id: int):
        """
        获取环境变量
        """
        return await self.get_kv(f"e:e_{env_id}_{user_id}")

    async def set_case_log(self, user_id: int, value: dict, case_id: int = None):
        """
        设置用例变量,存储格式: c:c_{case_id}_{user_id}, 保存3天
        """
        if case_id is None:
            case_id = "temp"
        await self.set_kv(f"c:c_{case_id}_{user_id}", value, expired=600 * 60 * 24 * 3)

    async def get_case_log(self, user_id: int, case_id: int = None):
        """
        获取用例变量
        """
        if case_id is None:
            case_id = "temp"
        return await self.get_kv(f"c:c_{case_id}_{user_id}")

    # async def init_case_log_body(self, user_id: int, case_id: int = None):
    #     """初始化每次执行用例的数据"""
    #     body = dict(
    #         env_prefix=[],
    #         case_prefix=[],
    #         var_replace=[],
    #         case_suffix=[],
    #         env_suffix=[],
    #         env_assert=[],
    #         case_assert=[],
    #         extract=[],
    #     )
    #     await self.set_case_var(user_id, body, case_id)


redis_client = RedisCli()
