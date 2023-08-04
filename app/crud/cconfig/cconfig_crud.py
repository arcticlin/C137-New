# coding=utf-8
"""
File: cconfig_crud.py
Author: bot
Created: 2023/8/4
Description:
"""
from app.core.db_connector import async_session
from sqlalchemy import select, and_, text
from app.utils.new_logger import logger
from app.schemas.cconfig.sql_schema import *
from app.schemas.cconfig.redis_schema import *
from app.schemas.cconfig.script_schema import *
from app.models.common_config.redis_model import RedisModel
from app.models.common_config.sql_model import SqlModel
from app.models.common_config.script_model import ScriptModel
from app.handler.db_bulk import DatabaseBulk


class CommonConfigCrud:

    @staticmethod
    async def query_sql_id_exists(sql_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT sql_id FROM sql_model WHERE sql_id = :sql_id AND deleted_at = 0
                """
            )
            execute = await session.execute(smtm, {"sql_id": sql_id})
            return execute.first()

    @staticmethod
    async def query_sql_name_exists(sql_name: str):
        async with async_session() as session:
            smtm = text(
                """
                SELECT sql_id FROM sql_model WHERE name = :sql_name AND deleted_at = 0
                """
            )
            execute = await session.execute(smtm, {"sql_name": sql_name})
            return execute.first()

    @staticmethod
    async def query_redis_id_exists(redis_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT redis_id FROM redis_model WHERE redis_id = :redis_id AND deleted_at = 0
                """
            )
            execute = await session.execute(smtm, {"redis_id": redis_id})
            return execute.first()

    @staticmethod
    async def query_redis_name_exists(redis_name: str):
        async with async_session() as session:
            smtm = text(
                """
                SELECT redis_id FROM redis_model WHERE name = :redis_name AND deleted_at = 0
                """
            )
            execute = await session.execute(smtm, {"redis_name": redis_name})
            return execute.first()

    @staticmethod
    async def query_script_id_exists(script_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT script_id FROM script WHERE script_id = :script_id AND deleted_at = 0
                """
            )
            execute = await session.execute(smtm, {"script_id": script_id})
            return execute.first()

    @staticmethod
    async def query_script_name_exists_in_public(script_name: str):
        async with async_session() as session:
            smtm = text(
                """
                SELECT script_id FROM script WHERE name = :script_name AND deleted_at = 0 AND public = 1
                """
            )
            execute = await session.execute(smtm, {"script_name": script_name})
            return execute.first()

    @staticmethod
    async def query_script_name_exists_in_private(script_name: str, user_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT script_id FROM script WHERE name = :script_name AND deleted_at = 0 AND public = 0 AND create_user = :user_id
                """
            )
            execute = await session.execute(smtm, {"script_name": script_name, "user_id": user_id})
            return execute.first()

    @staticmethod
    async def add_sql_config(data: AddSqlRequest, create_user: int):
        async with async_session() as session:
            async with session.begin():
                sql_model = SqlModel(**data.dict(), create_user=create_user)
                session.add(sql_model)
                await session.flush()
                # return sql_model.sql_id

    @staticmethod
    async def update_sql_config(data: UpdateSqlRequest, sql_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0)))
                sql_model = smtm.scalars().first()
                DatabaseBulk.update_model(sql_model, data.dict(), operator)

    @staticmethod
    async def delete_sql_config(sql_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0)))
                sql_model = smtm.scalars().first()
                DatabaseBulk.delete_model(sql_model, operator)

    @staticmethod
    async def add_redis_config(data: AddRedisRequest, create_user: int):
        async with async_session() as session:
            async with session.begin():
                redis_model = RedisModel(**data.dict(), create_user=create_user)
                session.add(redis_model)
                await session.flush()
                return redis_model.redis_id

    @staticmethod
    async def update_redis_config(data: UpdateRedisRequest, redis_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0)))
                redis_model = smtm.scalars().first()
                DatabaseBulk.update_model(redis_model, data.dict(), operator)

    @staticmethod
    async def delete_redis_config(redis_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0)))
                redis_model = smtm.scalars().first()
                DatabaseBulk.delete_model(redis_model, operator)

    @staticmethod
    async def add_script_config(data: AddScriptRequest, create_user: int):
        async with async_session() as session:
            async with session.begin():
                scripts = ScriptModel(**data.dict(), create_user=create_user)
                session.add(scripts)
                await session.flush()

                return scripts.script_id

    @staticmethod
    async def update_script_config(data: UpdateScriptRequest, script_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0)))
                script_model = smtm.scalars().first()
                DatabaseBulk.update_model(script_model, data.dict(), operator)

    @staticmethod
    async def delete_script_config(script_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0)))
                script_model = smtm.scalars().first()
                DatabaseBulk.delete_model(script_model, operator)

    @staticmethod
    async def query_sql_list():
        async with async_session() as session:
            smtm = text(
                """
                   SELECT sql_id, name, host ,sql_type FROM sql_model WHERE deleted_at = 0
                """
            )
            execute = await session.execute(smtm)
            return execute.all()

    @staticmethod
    async def query_redis_list():
        async with async_session() as session:
            smtm = text(
                """
                   SELECT redis_id, name, host  FROM redis_model WHERE deleted_at = 0
                """
            )
            execute = await session.execute(smtm)
            return execute.all()

    @staticmethod
    async def query_script_list(page: int = 1, page_size: int = 20,user_id: int = 0):
        pass

    @staticmethod
    async def query_sql_detail(sql_id: int):
        async with async_session() as session:
            smtm = await session.execute(select(SqlModel).where(and_(SqlModel.sql_id == sql_id, SqlModel.deleted_at == 0)))
            return smtm.scalars().first()

    @staticmethod
    async def query_redis_detail(redis_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0)))
            return smtm.scalars().first()

    @staticmethod
    async def query_script_detail(script_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ScriptModel).where(and_(ScriptModel.script_id == script_id, ScriptModel.deleted_at == 0)))
            return smtm.scalars().first()

