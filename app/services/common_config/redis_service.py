# coding=utf-8
"""
File: redis_service.py
Author: bot
Created: 2023/10/24
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.services.auth.crud.auth_crud import UserCrud
from app.services.common_config.crud.redis.redis_crud import RedisCrud
from app.services.common_config.schema.redis.news import RequestRedisAdd, RequestRedisPingByForm
from app.exceptions.rds_c_exp_450 import *
from app.services.common_config.schema.redis.update import RequestRedisUpdate


class RedisService:
    @staticmethod
    async def create_redis_config(form: RequestRedisAdd, creator: int):
        check = await RedisCrud.query_redis_name_exists(form.name)
        if check:
            raise CustomException(REDIS_NAME_EXISTS)
        redis_id = await RedisCrud.create_redis_config(form, creator)
        return redis_id

    @staticmethod
    async def update_redis_config(redis_id: int, form: RequestRedisUpdate, operator: int):
        check = await RedisCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        if form.name:
            check = await RedisCrud.query_redis_name_exists(form.name)
            if check:
                raise CustomException(REDIS_NAME_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await RedisCrud.operator_is_creator(redis_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_MODIFY_REDIS)
        await RedisCrud.update_redis_config(redis_id, form, operator)

    @staticmethod
    async def delete_redis_config(redis_id: int, operator: int):
        check = await RedisCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await RedisCrud.operator_is_creator(redis_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_DELETE_REDIS)
        await RedisCrud.delete_redis_config(redis_id, operator)

    @staticmethod
    async def query_redis_list(page: int, page_size: int):
        result, total = await RedisCrud.query_redis_list(page, page_size)
        return result, total

    @staticmethod
    async def query_redis_by_id(redis_id: int):
        check = await RedisCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        result = await RedisCrud.query_redis_detail(redis_id)
        return result

    @staticmethod
    async def ping_redis_by_form(form: RequestRedisPingByForm):
        await RedisCrud.ping_by_form(form)

    @staticmethod
    async def ping_redis_by_id(redis_id: int):
        check = await RedisCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        await RedisCrud.ping_by_id(redis_id)
