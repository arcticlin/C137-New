# coding=utf-8
"""
File: sql_model.py
Author: bot
Created: 2023/8/4
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import (
    Column,
    INT,
    String,
)


class SqlModel(Base, BaseMixin):
    __tablename__ = "sql_model"

    sql_id = Column(INT, primary_key=True)
    name = Column(String(16), nullable=False, comment="数据库描述")

    host = Column(String(128), nullable=False, comment="数据库域名")
    port = Column(INT, nullable=False, comment="数据库端口")

    db_user = Column(String(64), nullable=False, comment="账号")
    db_password = Column(String(64), comment="密码")
    db_name = Column(String(32), nullable=False, comment="库名")
    sql_type = Column(INT, nullable=False, default=1, comment="数据库类型, 1: Mysql  2: POSTGRESQL 3: MONGODB")

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        db_user: str,
        db_password: str,
        db_name: str,
        create_user: int,
        sql_type: int = None,
    ):
        self.create_user = create_user
        self.update_user = create_user

        self.name = name
        self.host = host
        self.port = port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.sql_type = sql_type
