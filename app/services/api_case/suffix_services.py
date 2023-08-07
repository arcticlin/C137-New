# coding=utf-8
"""
File: suffix_services.py
Author: bot
Created: 2023/8/7
Description:
"""
from app.crud.api_case.suffix_crud import SuffixCrud
from app.handler.response_handler import C137Response
import asyncio


class SuffixServices:
    @staticmethod
    async def get_env_suffix(env_id: int):
        prefix = await SuffixCrud.get_prefix(env_id)
        suffix = await SuffixCrud.get_suffix(env_id)
        print(C137Response.orm_with_list(prefix))
        print(C137Response.orm_with_list(suffix))

    @staticmethod
    async def get_case_suffix(case_id: int):
        prefix = await SuffixCrud.get_prefix(case_id=case_id)
        suffix = await SuffixCrud.get_suffix(case_id=case_id)
        print(C137Response.orm_with_list(prefix))
        print(C137Response.orm_with_list(suffix))

    @staticmethod
    async def execute_delay(delay: int):
        await asyncio.sleep(delay)

