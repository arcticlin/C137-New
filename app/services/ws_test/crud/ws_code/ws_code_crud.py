# coding=utf-8
"""
File: ws_code_crud.py
Author: bot
Created: 2023/11/22
Description:
"""
from typing import List, Any, Sequence

from app.services.ws_test.schema.ws_code.new import RequestAddWsCode
from app.services.ws_test.schema.ws_code.update import RequestUpdateWsCode
from app.utils.new_logger import logger
from app.core.db_connector import async_session
from app.models.ws_test.ws_code import WsCodeModel

from sqlalchemy import select, text, and_, func
from app.handler.db_tool.db_bulk import DatabaseBulk


class WsCodeCrud:
    @staticmethod
    async def code_is_exists(project_id: int, code_value: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM ws_code
                    WHERE project_id = :project_id AND code_value = :code_value AND deleted_at = 0
                ) AS is_exists
            """
            )
            result = await session.execute(smtm, {"project_id": project_id, "code_value": code_value})
            return result.scalars().first()

    @staticmethod
    async def ws_id_is_exists(ws_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM ws_code
                    WHERE ws_id = :ws_id AND deleted_at = 0
                ) AS is_exists
            """
            )
            result = await session.execute(smtm, {"ws_id": ws_id})
            return result.scalars().first()

    @staticmethod
    async def query_code_list(project_id: int):
        async with async_session() as session:
            count = await session.execute(
                select(func.count(WsCodeModel.ws_id)).where(
                    and_(WsCodeModel.project_id == project_id, WsCodeModel.deleted_at == 0)
                )
            )
            smtm = await session.execute(
                select(WsCodeModel).where(and_(WsCodeModel.project_id == project_id, WsCodeModel.deleted_at == 0))
            )
            return smtm.scalars().all(), count.scalars().first()

    @staticmethod
    async def query_code_detail(ws_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(WsCodeModel).where(and_(WsCodeModel.ws_id == ws_id, WsCodeModel.deleted_at == 0))
            )
            return smtm.scalars().first()

    @staticmethod
    async def add_ws_code(form: RequestAddWsCode, create_user: int):
        async with async_session() as session:
            async with session.begin():
                ws_code = WsCodeModel(
                    project_id=form.project_id,
                    code_value=form.code_value,
                    desc=form.desc,
                    create_user=create_user,
                    status=2,
                )
                session.add(ws_code)
                await session.flush()
                session.expunge(ws_code)
                return ws_code.ws_id

    @staticmethod
    async def update_ws_code(ws_id: int, form: RequestUpdateWsCode, create_user: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(WsCodeModel).where(and_(WsCodeModel.ws_id == ws_id, WsCodeModel.deleted_at == 0))
                )
                data = {"code_value": form.code_value, "desc": form.desc, "status": form.status}

                DatabaseBulk.update_model(smtm.scalars().first(), data, create_user)

    @staticmethod
    async def delete_ws_code(ws_id: int, create_user: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(WsCodeModel).where(and_(WsCodeModel.ws_id == ws_id, WsCodeModel.deleted_at == 0))
                )
                DatabaseBulk.delete_model(smtm.scalars().first(), create_user)
