# coding=utf-8
"""
File: script_crud.py
Author: bot
Created: 2023/10/25
Description:
"""

from app.core.db_connector import async_session
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.handler.db_tool.db_client import AsyncDbClient
from app.handler.script.script_handler import ScriptHandler
from app.services.common_config.schema.script.news import RequestScriptAdd, RequestScriptDebugByForm
from app.services.common_config.schema.script.update import RequestScriptUpdate
from app.models.common_config.script_model import ScriptModel


from sqlalchemy import select, and_, text


class ScriptCrud:
    @staticmethod
    async def query_script_id_exists(script_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM script WHERE script_id = :script_id AND deleted_at = 0) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"script_id": script_id})
            return execute.scalars().first()

    @staticmethod
    async def query_script_name_exists(script_name: str, creator: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM script WHERE name = :script_name AND deleted_at = 0 AND create_user=:creator) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"script_name": script_name, "creator": creator})
            return execute.scalars().first()

    @staticmethod
    async def operator_is_creator(script_id: int, operator: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM script WHERE script_id = :script_id AND deleted_at = 0 AND create_user =:operator) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"script_id": script_id, "operator": operator})
            return execute.scalars().first()

    @staticmethod
    async def create_script_config(form: RequestScriptAdd, creator: int):
        async with async_session() as session:
            async with session.begin():
                r = ScriptModel(**form.dict(), create_user=creator)
                session.add(r)
                await session.flush()
                session.expunge(r)
                return r.script_id

    @staticmethod
    async def update_script_config(script_id: int, form: RequestScriptUpdate, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.update_model(result, form.dict(), operator)
                await session.flush()

    @staticmethod
    async def delete_script_config(script_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.delete_model(result, operator)
                await session.flush()

    @staticmethod
    async def query_script_list(page: int, page_size: int, operator: int):
        offset = (page - 1) * page_size
        async with async_session() as session:
            smtm_total = text(
                """
                SELECT COUNT(*) as total FROM script WHERE deleted_at = 0 AND (public = 1 OR create_user = :operator)
                """
            )
            total = await session.execute(smtm_total, {"operator": operator})
            smtm_r = select(ScriptModel).where(and_(ScriptModel.deleted_at == 0)).limit(page_size).offset(offset)
            execute = await session.execute(smtm_r)

            return execute.scalars().all(), total.scalars().first()

    @staticmethod
    async def query_script_detail(script_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
            return result

    @staticmethod
    async def execute_by_form(form: RequestScriptDebugByForm):
        result = await ScriptHandler.python_executor(form.var_key, form.var_script)
        return result

    @staticmethod
    async def execute_by_id(script_id: int, trace_id: str = "default"):
        async with async_session() as session:
            smtm = await session.execute(
                select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
        s_config = ScriptCrud.convert_model_to_script_form(result)
        result = await ScriptHandler.python_executor(s_config.var_key, s_config.var_script, trace_id=trace_id)
        return result

    @staticmethod
    def convert_model_to_script_form(instance: ScriptModel):
        return RequestScriptDebugByForm(
            var_key=instance.var_key,
            var_script=instance.var_script,
        )
