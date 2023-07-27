# coding=utf-8
"""
File: redis_handler.py
Author: bot
Created: 2023/7/25
Description:
"""
import sys

from redis import asyncio as aioredis
from redis.asyncio import Redis

from app.utils.logger import Log
from base_config import Config


class RedisCli(Redis):
    log = Log("Redis")

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
            RedisCli.log.error("连接超时")
            sys.exit()
        except aioredis.AuthenticationError:
            RedisCli.log.error("验证失败")
            sys.exit()
        except Exception as e:
            RedisCli.log.error(f"Redis连接异常: {e}")
            sys.exit()


redis_client = RedisCli()
