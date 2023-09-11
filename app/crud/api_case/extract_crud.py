# coding=utf-8
"""
File: extract_crud.py
Author: bot
Created: 2023/8/8
Description:
"""
from app.handler.db_bulk import DatabaseBulk
from app.models.api_settings.extract_settings import ExtractModel
from sqlalchemy import select, and_, text
from app.core.db_connector import async_session
from app.schemas.api_settings.extract_schema import SchemaCaseExtract


class ExtractCrud:
    @staticmethod
    async def query_extract_detail(extract_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ExtractModel).where(and_(ExtractModel.extract_id == extract_id, ExtractModel.deleted_at == 0))
            )
            return smtm.scalars().first()

    @staticmethod
    async def query_case_extract(case_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ExtractModel).where(and_(ExtractModel.case_id == case_id, ExtractModel.deleted_at == 0))
            )
            return smtm.scalars().all()

    @staticmethod
    async def add_extract_form(form: list[SchemaCaseExtract], creator: int, case_id: int = None, env_id: int = None):
        async with async_session() as session:
            async with session.begin():
                await DatabaseBulk.bulk_add_data(
                    session,
                    ExtractModel,
                    form,
                    create_user=creator,
                    case_id=case_id,
                    env_id=env_id,
                    update_user=creator,
                )
                await session.flush()

    @staticmethod
    async def add_extract_form_with_session(
        session, form: list[SchemaCaseExtract], creator: int, case_id: int = None, env_id: int = None
    ):
        await DatabaseBulk.bulk_add_data(
            session,
            ExtractModel,
            form,
            create_user=creator,
            case_id=case_id,
            env_id=env_id,
            update_user=creator,
        )
        await session.flush()
