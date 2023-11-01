# coding=utf-8
"""
File: cache_redis.py
Author: bot
Created: 2023/10/8
Description:
"""
import functools
from typing import List, Union

from app.handler.redis.rds_client import RedisCli
from loguru import logger


class CacheRedis:
    rds = RedisCli()

    @staticmethod
    async def ping():
        await CacheRedis.rds.ping()

    @staticmethod
    def delete_keys(keys_list: List[str]):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                for key in keys_list:
                    await CacheRedis.rds.delete(key)
                return result

            return wrapper

        return decorator

    @staticmethod
    def user_cache(user_id: int = None):
        logger.debug("使用RedisUser缓存")

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if user_id is not None:
                    cache_key = f"ut:user_token_{user_id}"
                    cached_result = await CacheRedis.rds.get_key_value_as_json(cache_key)
                    if cached_result:
                        logger.debug(f"查询user_id: {user_id}的缓存信息并直接返回")
                        return cached_result
                result = await func(*args, **kwargs)
                uid = result.get("user_id")
                cache_key = f"ut:user_token_{uid}"
                logger.debug(f"设置user_id:{user_id}的缓存信息")
                await CacheRedis.rds.set_key_as_json(cache_key, result, expired=7200)
                return result

            return wrapper

        return decorator

    @staticmethod
    def cache(key: str, expired: int = 7200):
        logger.debug("使用Redis缓存")

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                cached_result = await CacheRedis.rds.get_key_value_as_json(key)
                if cached_result:
                    logger.debug(f"查询{key}的缓存信息并直接返回")
                    return cached_result
                result = await func(*args, **kwargs)
                logger.debug(f"设置{key}的缓存信息")
                await CacheRedis.rds.set_key_as_json(key, result, expired)
                return result

            return wrapper

        return decorator

    @staticmethod
    async def get_project_list_cache(user_id: int) -> Union[List, None]:
        result = await CacheRedis.rds.get_key_value_as_json(f"p:project_list_{user_id}")
        return result if result else None

    @staticmethod
    async def clear_project_list_cache(user_id: int) -> None:
        await CacheRedis.rds.delete(f"p:project_list_{user_id}")
