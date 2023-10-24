# coding=utf-8
"""
File: sql_crud.py
Author: bot
Created: 2023/10/24
Description:
"""
from app.core.db_connector import async_session
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.services.common_config.schema.redis.news import RequestRedisAdd, RequestRedisPingByForm
from app.services.common_config.schema.redis.update import RequestRedisUpdate
from app.models.common_config.redis_model import RedisModel
from app.handler.redis.rds_client import RedisCli

from sqlalchemy import select, and_, text


class RedisCrud:
    @staticmethod
    async def query_redis_id_exists(redis_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM redis_model WHERE redis_id = :redis_id AND deleted_at = 0) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"redis_id": redis_id})
            return execute.scalars().first()

    @staticmethod
    async def query_redis_name_exists(redis_name: str):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM redis_model WHERE name = :redis_name AND deleted_at = 0) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"redis_name": redis_name})
            return execute.scalars().first()

    @staticmethod
    async def operator_is_creator(redis_id: int, operator: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM redis_model WHERE redis_id = :redis_id AND deleted_at = 0 AND create_user =:operator) AS is_exists;
                """
            )
            execute = await session.execute(smtm, {"redis_id": redis_id, "operator": operator})
            return execute.scalars().first()

    @staticmethod
    async def create_redis_config(form: RequestRedisAdd, creator: int):
        async with async_session() as session:
            async with session.begin():
                r = RedisModel(**form.dict(), create_user=creator)
                session.add(r)
                await session.flush()
                session.expunge(r)
                return r.redis_id

    @staticmethod
    async def update_redis_config(redis_id: int, form: RequestRedisUpdate, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.update_model(result, form.dict(), operator)
                await session.flush()

    @staticmethod
    async def delete_redis_config(redis_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                DatabaseBulk.delete_model(result, operator)
                await session.flush()

    @staticmethod
    async def query_redis_list(page: int, page_size: int):
        offset = (page - 1) * page_size
        async with async_session() as session:
            smtm_total = text(
                """
                SELECT COUNT(*) as total FROM redis_model WHERE deleted_at = 0;
                """
            )
            total = await session.execute(smtm_total)
            smtm_r = select(RedisModel).where(and_(RedisModel.deleted_at == 0)).limit(page_size).offset(offset)
            execute = await session.execute(smtm_r)

            return execute.scalars().all(), total.scalars().first()

    @staticmethod
    async def query_redis_detail(redis_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
            return result

    @staticmethod
    async def ping_by_form(form: RequestRedisPingByForm):
        rds = RedisCli(form=form)
        await rds.init_redis_connect()

    @staticmethod
    async def ping_by_id(redis_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(RedisModel).where(and_(RedisModel.redis_id == redis_id, RedisModel.deleted_at == 0))
            )
            result = smtm.scalars().first()
        r_config = RequestRedisPingByForm(
            host=result.host,
            port=result.port,
            password=result.password,
            db=result.db,
        )
        rds = RedisCli(form=r_config)
        await rds.init_redis_connect()

    @staticmethod
    async def execute_rds_command(instance: RedisCli, command: str):
        return await instance.execute_rds_command(command)
