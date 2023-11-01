import json
from typing import Union, Any
from redis import asyncio as aioredis
from redis.asyncio import Redis

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_450_rds import REDIS_CONNECT_FAIL
from app.services.common_config.schema.redis.news import RequestRedisPingByForm
from base_config import Config
from loguru import logger
import sys


class RedisCli(Redis):
    _instances = {}

    # def __new__(cls, trace_id: str = None, form: RequestRedisPingByForm = None, **kwargs):
    #     # 实现单例
    #     if trace_id is None:
    #         instance = super(RedisCli, cls).__new__(cls)
    #         if form:
    #             instance.__init__(trace_id, form)
    #         else:
    #             instance.__init__(trace_id)
    #         cls._instances["default"] = instance
    #         return cls._instances["default"]
    #     else:
    #         if trace_id not in cls._instances and kwargs.get("case_id", False) and :
    #             instance = super(RedisCli, cls).__new__(cls)
    #             instance.__init__(trace_id)
    #             cls._instances[trace_id] = instance
    #     return cls._instances[trace_id]

    def __init__(self, trace_id: str = None, form: RequestRedisPingByForm = None):
        if form is not None:
            super(RedisCli, self).__init__(
                host=form.host,
                port=form.port,
                password=form.password,
                db=form.db,
                decode_responses=True,
            )
        else:
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
            raise CustomException(REDIS_CONNECT_FAIL, "连接超时")

        except aioredis.AuthenticationError:
            logger.error("验证失败")
            raise CustomException(REDIS_CONNECT_FAIL, "验证失败")
        except Exception as e:
            logger.error(f"Redis连接异常: {e}")
            raise CustomException(REDIS_CONNECT_FAIL, f"{e}")

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

    async def execute_rds_command(self, command: str) -> Union[str, int]:
        """
        执行自定义的 Redis 命令
        :param command: Redis 命令字符串
        :return: Redis 命令执行结果
        """
        try:
            result = await self.execute_command(command)
            return result
        except Exception as e:
            logger.error(f"Redis 命令执行异常: {e}")
            raise CustomException(REDIS_CONNECT_FAIL, f"Redis 命令执行异常: {e}")

    async def get_common_env(self, env_id: int, user_id: int):
        return await self.get_key_value_as_json(f"api:e:e_{env_id}_{user_id}")
