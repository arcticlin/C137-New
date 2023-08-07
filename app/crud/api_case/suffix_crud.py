# coding=utf-8
"""
File: suffix_crud.py
Author: bot
Created: 2023/8/7
Description:
"""

from app.models.api_settings.suffix_settings import SuffixModel
from app.core.db_connector import async_session
from sqlalchemy import text, select, and_, or_
from app.exceptions.commom_exception import CustomException


class SuffixCrud:
    @staticmethod
    async def get_prefix(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_or = [SuffixModel.deleted_at == 0, SuffixModel.suffix_type == 1]
            if env_id:
                smtm_or.append(SuffixModel.env_id == env_id)
            if case_id:
                smtm_or.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel).where(and_(*smtm_or)).order_by(SuffixModel.sort))

            return smtm.scalars().all()

    @staticmethod
    async def get_suffix(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_or = [SuffixModel.deleted_at == 0, SuffixModel.suffix_type == 2]
            if env_id:
                smtm_or.append(SuffixModel.env_id == env_id)
            if case_id:
                smtm_or.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel).where(and_(*smtm_or)).order_by(SuffixModel.sort))

            return smtm.scalars().all()

    @staticmethod
    async def execute_script(script_id: int):
        pass

    @staticmethod
    async def execute_sql(sql_id: int, command: str, out_name: str):
        pass

    @staticmethod
    async def execute_redis(redis_id: int, command: str, out_name: str):
        pass

    @staticmethod
    async def execute_delay(delay: int):
        pass

    @staticmethod
    async def execute_case(case_id: int):
        pass
