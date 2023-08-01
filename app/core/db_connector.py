# coding=utf-8
"""
File: db_connector.py
Author: bot
Created: 2023/7/25
Description: 连接Sqlalchemy数据库
"""
from datetime import datetime

from sqlalchemy import Column, INT, BIGINT, func, event, TIMESTAMP

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base
from base_config import Config


async_engine: AsyncEngine = create_async_engine(Config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500, future=True)

async_session: async_sessionmaker = async_sessionmaker(bind=async_engine, class_=AsyncSession, autoflush=True)


Base = declarative_base()


# Mixin
class BaseMixin:
    create_user = Column(INT, comment="创建人", index=True)
    update_user = Column(INT, comment="更新人")
    created_at = Column(
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        comment="创建时间",
        index=True,
    )
    updated_at = Column(
        TIMESTAMP,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        comment="更新时间",
    )
    deleted_at = Column(BIGINT, default=0, comment="删除时间", index=True)

    @staticmethod
    def set_defaults(mapper, connection, target: "BaseMixin"):
        target.created_at = func.now()
        target.deleted_at = 0
        target.updated_at = func.now()

    @staticmethod
    def set_updated_at(mapper, connection, target: "BaseMixin"):
        target.updated_at = func.now()


# 事件绑定, before在更新数据时执行方法. FYI: 仅python层面的赋值, 并不会真正的更新数据库, 只有Commit后才会更新数据库.
# https://docs.sqlalchemy.org/en/14/orm/events.html
event.listen(BaseMixin, "before_insert", BaseMixin.set_defaults)
event.listen(BaseMixin, "before_update", BaseMixin.set_updated_at)
