# coding=utf-8
"""
File: assert_crud.py
Author: bot
Created: 2023/8/7
Description:
"""
from typing import List

from app.models.api_settings.assert_settings import AssertModel
from app.core.db_connector import async_session
from sqlalchemy import select, and_, text


class AssertCurd:
    @staticmethod
    async def query_assert_detail(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm = [AssertModel.deleted_at == 0]
            if env_id:
                smtm.append(AssertModel.env_id == env_id)
            if case_id:
                smtm.append(AssertModel.case_id == case_id)
            result = await session.execute(select(AssertModel).where(and_(*smtm)).order_by(AssertModel.created_at))
            return result.scalars().all()

    @staticmethod
    async def execute_assert_equal(assert_src: str, assert_value: str, is_equal: bool):
        pass

    @staticmethod
    async def execute_assert_ge(assert_src: str, assert_value: str, is_ge: bool):
        pass

    @staticmethod
    async def execute_assert_in_list(assert_src: str, assert_value: List, is_in: bool):
        pass

    @staticmethod
    async def execute_assert_contain(assert_src: str, assert_value: str, is_contain: bool):
        pass

    @staticmethod
    async def execute_assert_start_with(assert_src: str, assert_value: str, is_start_with: bool):
        pass

    @staticmethod
    async def execute_assert_re(assert_src: str, assert_exp: str):
        pass

    @staticmethod
    async def execute_assert_json_path(assert_src: str, assert_exp: str):
        pass
