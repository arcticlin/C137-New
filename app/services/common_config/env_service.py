# coding=utf-8
"""
File: env_service.py
Author: bot
Created: 2023/10/23
Description:
"""
from app.handler.serializer.response_serializer import C137Response
from app.services.common_config.crud.envs.env_crud import EnvCrud


class EnvService:
    @staticmethod
    async def get_env_list(page: int, page_size: int, user_id: int):
        result, total = await EnvCrud.get_env_list(page, page_size, user_id)
        return result, total

    @staticmethod
    async def get_env_detail(env_id: int):
        env_info, query_info, header_info, suffix_info, assert_info = await EnvCrud.get_env_detail(env_id)
        result = {
            "env_id": env_info.env_id,
            "name": env_info.name,
            "domain": env_info.domain,
            "query_info": C137Response.orm_with_list(query_info),
            "headers_info": C137Response.orm_with_list(header_info),
            "suffix_info": C137Response.orm_with_list(suffix_info),
            "assert_info": C137Response.orm_with_list(assert_info),
        }
        return result
