# coding=utf-8
"""
File: api_redis_handle.py
Author: bot
Created: 2023/9/22
Description:
"""
import json
from typing import Union

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
            return instance.__init__(trace_id)
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

    async def get_kv(self, key: str) -> dict:
        """获取键值对"""
        value = await self.get(key)
        try:
            return json.loads(value)
        except Exception as e:
            return {}

    async def set_kv(self, key: str, obj: dict, expired: int = None):
        """设置键值对"""
        await self.set(key, json.dumps(obj), ex=expired)

    def get_env_rk(self, env_id: int):
        """返回env redis key, 格式为: api_{trace_id}:e:e_{env_id}"""
        return f"api:{self.trace_id}:e:e_{env_id}"

    def get_case_rk(self, case_id: int):
        """返回case redis key, 格式为: api_{trace_id}:c:c_{case_id}"""
        return f"api:{self.trace_id}:c:c_{case_id}"

    async def init_env_key(self, env_id: int):
        rk = self.get_env_rk(env_id)
        body = dict(var={}, log=dict(env_prefix=[], env_suffix=[]))
        await self.set_kv(rk, body, expired=7200)

    async def init_case_key(self, case_id: int):
        rk = self.get_case_rk(case_id)
        body = dict(var={}, log=dict())
        await self.set_kv(rk, body, expired=7200)

    async def set_env_var(self, env_id: int, value: dict):
        rk = self.get_env_rk(env_id)
        var = await self.get_kv(rk)
        var["var"].update(value)
        await self.set_kv(rk, var, expired=7200)

    async def set_env_log(self, env_id: int, value: dict):
        rk = self.get_env_rk(env_id)
        var = await self.get_kv(rk)
        var["log"].update(value)
        await self.set_kv(rk, var, expired=7200)

    async def set_case_var(self, case_id: int, value: dict):
        rk = self.get_case_rk(case_id)
        var = await self.get_kv(rk)
        var["var"].update(value)
        await self.set_kv(rk, var, expired=7200)

    async def set_case_log(self, case_id: int, value: dict):
        rk = self.get_case_rk(case_id)
        var = await self.get_kv(rk)
        var["log"].update(value)
        await self.set_kv(rk, var, expired=7200)

    async def get_var_value(
        self, var_key: str, env_id: int = None, case_id: Union[str, int] = None, is_env: bool = True
    ):
        if is_env:
            rk = self.get_env_rk(env_id)
        else:
            rk = self.get_case_rk(case_id)

        get_value_from_redis = await self.get_kv(rk)
        return get_value_from_redis.get("var", {}).get(var_key, None)
