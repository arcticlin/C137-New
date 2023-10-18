import json
from typing import Union, Any
from redis import asyncio as aioredis
from redis.asyncio import Redis
from base_config import Config
from loguru import logger
import sys


class RedisCli(Redis):
    _instances = {}

    def __new__(cls, trace_id: str = None):
        # 实现单例
        if trace_id is None:
            instance = super(RedisCli, cls).__new__(cls)
            instance.__init__(trace_id)
            cls._instances["default"] = instance
            return cls._instances["default"]
        else:
            if trace_id not in cls._instances:
                instance = super(RedisCli, cls).__new__(cls)
                instance.__init__(trace_id)
                cls._instances[trace_id] = instance
        return cls._instances[trace_id]

    def __init__(self, trace_id: str = None):
        super(RedisCli, self).__init__(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PWD,
            db=Config.REDIS_DB,
            decode_responses=True,
        )
        self.trace_id = trace_id

    @classmethod
    async def destroy_instance(cls, trace_id):
        logger.debug(f"断开redis连接: {trace_id}")
        if cls._instances.__contains__(trace_id):
            cls._instances.pop(trace_id)

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

    async def get_key(self, key: str) -> Any:
        value = await self.get(key)
        return value

    async def get_key_value_as_json(self, key: str) -> dict:
        value = await self.get(key)
        try:
            return json.loads(value)
        except Exception as e:
            return {}

    async def set_key(self, key: str, value: Any, expired: int = None) -> None:
        await self.set(key, value, ex=expired)

    async def set_key_as_json(self, key: str, value: dict, expired: int = None) -> None:
        await self.set(key, json.dumps(value), ex=expired)
