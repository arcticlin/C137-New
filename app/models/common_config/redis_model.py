# coding=utf-8
"""
File: redis_model.py
Author: bot
Created: 2023/8/4
Description:
"""

from sqlalchemy import Column, INT, String, BOOLEAN
from app.core.db_connector import Base, BaseMixin


class RedisModel(Base, BaseMixin):
    __tablename__ = "redis_model"

    redis_id = Column(INT, primary_key=True)
    name = Column(String(16), nullable=False, comment="Redis描述")

    host = Column(String(128), nullable=False, comment="Redis域名")
    port = Column(INT, nullable=False, default=6379, comment="Redis端口")

    db = Column(INT, default=0, comment="Redis DB")

    username = Column(String(64), comment="账号")
    password = Column(String(64), comment="密码")

    cluster = Column(BOOLEAN, nullable=False, default=False, comment="集群")

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        create_user: int,
        db: int = 0,
        username: str = None,
        password: str = None,
        cluster: bool = False,
    ):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.cluster = cluster
