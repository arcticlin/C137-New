# coding=utf-8
"""
File: sql_crud.py
Author: bot
Created: 2023/10/24
Description:
"""
from aiomysql import Connection
from pydantic import BaseModel

from app.core.db_connector import async_session
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.handler.db_tool.db_client import AsyncDbClient
from app.services.common_config.schema.sql.news import RequestSqlAdd, RequestSqlPingByForm
from app.services.common_config.schema.sql.update import RequestSqlUpdate
from app.models.common_config.sql_model import SqlModel


from sqlalchemy import select, and_, text


class SqlCrud:
    @staticmethod
    async def query_sql_id_exists(sql_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM sql_model WHERE sql_id = :sql_id AND deleted_at = 0) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"sql_id": sql_id})
            return execute.scalars().first()

    @staticmethod
    async def query_sql_name_exists(sql_name: str):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM sql_model WHERE name = :sql_name AND deleted_at = 0) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"sql_name": sql_name})
            return execute.scalars().first()

    @staticmethod
    async def operator_is_creator(sql_id: int, operator: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM sql_model WHERE sql_id = :sql_id AND deleted_at = 0 AND create_user =:operator) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"sql_id": sql_id, "operator": operator})
            return execute.scalars().first()

    @staticmethod
    async def create_sql_config(form: RequestSqlAdd, creator: int):
        async with async_session() as session:
            async with session.begin():
                r = SqlModel(**form.dict(), create_user=creator)
                session.add(r)
                await session.flush()
                session.expunge(r)
                return r.sql_id

    @staticmethod
    async def update_sql_config(sql_id: int, form: RequestSqlUpdate, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.update_model(result, form.dict(), operator)
                await session.flush()

    @staticmethod
    async def delete_sql_config(sql_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.delete_model(result, operator)
                await session.flush()

    @staticmethod
    async def query_sql_list(page: int, page_size: int):
        offset = (page - 1) * page_size
        async with async_session() as session:
            smtm_total = text(
                """
                SELECT COUNT(*) as total FROM sql_model WHERE deleted_at = 0;
                """
            )
            total = await session.execute(smtm_total)
            smtm_r = select(SqlModel).where(and_(SqlModel.deleted_at == 0)).limit(page_size).offset(offset)
            execute = await session.execute(smtm_r)

            return execute.scalars().all(), total.scalars().first()

    @staticmethod
    async def query_sql_detail(sql_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
            return result

    @staticmethod
    async def ping_by_form(form: RequestSqlPingByForm):
        await AsyncDbClient(form).ping()

    @staticmethod
    async def ping_by_id(sql_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
        s_config = SqlCrud.convert_model_to_sql_form(result)
        await AsyncDbClient(s_config).ping()

    @staticmethod
    async def execute_sql_command_by_form(form: RequestSqlPingByForm, command: str, fetch_one: bool):
        c = AsyncDbClient(form)
        async with c as connection:
            result = await c.execute_command_with_c(connection, command, fetch_one)
            return result

    @staticmethod
    def convert_model_to_sql_form(instance: SqlModel):
        return RequestSqlPingByForm(
            host=instance.host,
            port=instance.port,
            db_user=instance.db_user,
            db_password=instance.db_password,
            db_name=instance.db_name,
            sql_type=instance.sql_type,
        )
