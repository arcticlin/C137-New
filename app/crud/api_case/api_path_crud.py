# coding=utf-8
"""
File: api_path_crud.py
Author: bot
Created: 2023/8/14
Description:
"""
from app.models.apicase.api_path import ApiPathModel
from app.core.db_connector import async_session
from sqlalchemy import select, and_


class ApiPathCrud:
    @staticmethod
    async def query_path_detail_by_env_case(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm = [ApiPathModel.deleted_at == 0]
            if env_id is not None:
                smtm.append(ApiPathModel.env_id == env_id)
            if case_id is not None:
                smtm.append(ApiPathModel.case_id == case_id)
            smtm_p = await session.execute(select(ApiPathModel).where(and_(*smtm)))
            return smtm_p.scalars().all()
