# coding=utf-8
"""
File: redis_handler.py
Author: bot
Created: 2023/7/25
Description:
"""
import json
import sys

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
            return None

    async def set_kv_load(self, key: str, obj: dict, expired: int = None):
        """设置键值对"""
        result = await self.get_kv(key)
        if isinstance(result, dict):
            result.update(obj)
        else:
            result = obj
        await self.set_kv(key, result, expired)


redis_client = RedisCli()
