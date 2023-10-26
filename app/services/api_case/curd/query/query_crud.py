# coding=utf-8
"""
File: query_crud.py
Author: bot
Created: 2023/10/23
Description:
"""
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.models.api_case.api_path import ApiPathModel
from app.core.db_connector import async_session
from sqlalchemy import select, and_

from app.services.api_case.schema.query.news import RequestTempQueryNew


class ApiPathCrud:
    @staticmethod
    async def add_params_form_with_session(
        session, form: list[RequestTempQueryNew], creator: int, case_id: int = None, env_id: int = None
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
