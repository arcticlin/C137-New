# coding=utf-8
"""
File: ws_case_crud.py
Author: bot
Created: 2023/11/22
Description:
"""
from typing import List, Any, Sequence

from app.services.ws_test.schema.ws_case.new import RequestAddWsCase
from app.services.ws_test.schema.ws_case.update import RequestUpdateWsCase
from app.utils.new_logger import logger
from app.core.db_connector import async_session
from app.models.ws_test.ws_case import WsCaseModel

from sqlalchemy import select, text, and_
from app.handler.db_tool.db_bulk import DatabaseBulk


class WsCaseCrud:
    @staticmethod
    async def query_case_list(ws_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(WsCaseModel).where(and_(WsCaseModel.ws_id == ws_id, WsCaseModel.deleted_at == 0))
            )
            return smtm.scalars().all()

    @staticmethod
    async def add_case(form: RequestAddWsCase, create_user: int):
        async with async_session() as session:
            async with session.begin():
                case = WsCaseModel(
                    ws_id=form.ws_id,
                    case_desc=form.case_desc,
                    case_status=1,
                    create_user=create_user,
                )
                session.add(case)
                await session.flush()
                session.expunge(case)
                return case.case_id

    @staticmethod
    async def update_case(ws_id: int, form: RequestUpdateWsCase):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(WsCaseModel).where(
                        and_(
                            WsCaseModel.ws_id == ws_id, WsCaseModel.case_id == form.case_id, WsCaseModel.deleted_at == 0
                        )
                    )
                )
                data = {"case_desc": form.case_desc, "case_status": form.case_status}
                DatabaseBulk.update_model(smtm.scalars().first(), data)

    @staticmethod
    async def remove_case(ws_id: int, case_id: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(WsCaseModel).where(
                        and_(WsCaseModel.ws_id == ws_id, WsCaseModel.case_id == case_id, WsCaseModel.deleted_at == 0)
                    )
                )
                DatabaseBulk.delete_model(smtm.scalars().first())

    @staticmethod
    async def query_case_as_dict(case_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(WsCaseModel).where(and_(WsCaseModel.case_id == case_id, WsCaseModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
            ws_id = result.ws_id
            smtm_code = await session.execute(
                text("""select code_value from ws_code where ws_id = :ws_id and deleted_at = 0"""), {"ws_id": ws_id}
            )
            code = smtm_code.scalars().all()
            return {
                "case_id": result.case_id,
                "ws_code": code,
                "json_exp": result.json_exp,
                "expected": result.expected,
            }
