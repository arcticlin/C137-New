# coding=utf-8
"""
File: suffix_crud.py
Author: bot
Created: 2023/8/7
Description:
"""
from typing import List, Any, Sequence

from app.models.api_settings.suffix_settings import SuffixModel
from app.core.db_connector import async_session
from sqlalchemy import text, select, and_, or_, Row, RowMapping
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
    async def query_suffix_name_exists(suffix_type: int, name: str, env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_list = [SuffixModel.suffix_type == suffix_type, SuffixModel.name == name, SuffixModel.deleted_at == 0]
            if env_id:
                smtm_list.append(SuffixModel.env_id == env_id)
            else:
                smtm_list.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel.suffix_id).where(and_(*smtm_list)))
            return smtm.scalar().first()

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

    @staticmethod
    async def add_suffix(create_user: int, **kwargs):
        async with async_session() as session:
            async with session.begin():
                suffix = SuffixModel(**kwargs, create_user=create_user)
                session.add(suffix)
                await session.flush()
                session.expunge(suffix)
