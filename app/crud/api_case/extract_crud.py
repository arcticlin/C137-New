# coding=utf-8
"""
File: extract_crud.py
Author: bot
Created: 2023/8/8
Description:
"""
from app.models.api_settings.extract_settings import ExtractModel
from sqlalchemy import select, and_, text
from app.core.db_connector import async_session


class ExtractCrud:
    @staticmethod
    async def query_extract_detail(extract_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ExtractModel).where(and_(ExtractModel.extract_id == extract_id, ExtractModel.deleted_at == 0))
            )
            return smtm.scalars().first()
