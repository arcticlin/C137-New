# coding=utf-8
"""
File: env_settings.py
Author: bot
Created: 2023/8/7
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class EnvModel(Base, BaseMixin):
    __tablename__ = "env"

    env_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False, comment="环境名称")
    domain = Column(String(128), nullable=False, comment="环境URL")

    def __init__(self, name: str, domain: str, create_user: int):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.domain = domain
