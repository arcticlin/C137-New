# coding=utf-8
"""
File: api_path_crud.py
Author: bot
Created: 2023/8/14
Description:
"""
from app.handler.db_bulk import DatabaseBulk
from app.models.apicase.api_path import ApiPathModel
from app.core.db_connector import async_session
from sqlalchemy import select, and_

from app.schemas.api_case.api_case_schema_new import SchemaCaseParams


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

    @staticmethod
    async def add_params_form_with_session(
        session, form: list[SchemaCaseParams], creator: int, case_id: int = None, env_id: int = None
    ):
        await DatabaseBulk.bulk_add_data(
            session,
            ApiPathModel,
            form,
            create_user=creator,
            case_id=case_id,
            env_id=env_id,
            update_user=creator,
        )
        await session.flush()

    @staticmethod
    async def add_params_form(form: list[SchemaCaseParams], creator: int, case_id: int = None, env_id: int = None):
        async with async_session() as session:
            async with session.begin():
                await DatabaseBulk.bulk_add_data(
                    session,
                    ApiPathModel,
                    form,
                    create_user=creator,
                    case_id=case_id,
                    env_id=env_id,
                    update_user=creator,
                )
                await session.flush()
