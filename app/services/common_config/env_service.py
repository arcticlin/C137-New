# coding=utf-8
"""
File: env_service.py
Author: bot
Created: 2023/10/23
Description:
"""
from app.handler.redis.rds_client import RedisCli
from app.handler.serializer.response_serializer import C137Response
from app.services.common_config.crud.envs.env_crud import EnvCrud


class EnvService:
    @staticmethod
    async def get_env_list(page: int, page_size: int, user_id: int):
        result, total = await EnvCrud.get_env_list(page, page_size, user_id)
        return result, total

    @staticmethod
    async def get_env_detail(env_id: int):
        result = await EnvCrud.get_env_detail(env_id)
        return result

    @staticmethod
    async def get_env_keys(env_id: int, user_id: int):
        return await RedisCli().get_key_value_as_json(f"api:e:e_{env_id}_{user_id}")