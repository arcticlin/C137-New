# coding=utf-8
"""
File: notify_model.py
Author: bot
Created: 2023/10/19
Description:
"""
from app.core.db_connector import BaseMixin, Base
from sqlalchemy import String, Column, INT, DATETIME, BOOLEAN, TEXT, TIMESTAMP
from sqlalchemy import Enum as SqlEnum
from app.enums.enum_user import UserRoleEnum


class NotifyModel(Base, BaseMixin):
    __tablename__ = "notify"

    id = Column(INT, primary_key=True, autoincrement=True)
    user_id = Column(INT, nullable=False, comment="用户id")
    message = Column(TEXT, nullable=False, comment="消息")
    read_at = Column(TIMESTAMP, nullable=True, comment="已读时间")

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
