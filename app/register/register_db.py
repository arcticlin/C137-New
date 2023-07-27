# coding=utf-8
"""
File: register_db.py
Author: bot
Created: 2023/7/25
Description:
"""
from sqlalchemy import create_engine, DDL
from base_config import Config
from app.core.db_connector import async_engine, Base
from fastapi import FastAPI
from app.handler.redis_handler import redis_client

# Model
from app.models.model_collect import *


def create_databases():
    """
    启动时创建数据库, 使用的是同步的方法
    :return:
    """
    engine = create_engine(Config.SQLALCHEMY_URI)
    create_db_stmt = DDL(
        f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DBNAME} default character set utf8mb4 collate utf8mb4_unicode_ci"
    )
    with engine.connect() as conn:
        conn.execute(create_db_stmt)
        engine.dispose()


async def create_tables():
    # 创建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    # 删除所有表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def register_db(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        create_databases()
        if Config.MYSQL_DROP_BEFORE_START:
            await drop_tables()
        await create_tables()
        if Config.REDIS_ON:
            await redis_client.init_redis_connect()
