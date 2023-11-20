# coding=utf-8
"""
File: ws_code.py
Author: bot
Created: 2023/11/20
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey


class WsCode(Base, BaseMixin):
    __tablename__ = "ws_code"

    ws_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    code_value = Column(Integer, nullable=False)
    desc = Column(String(32), nullable=False)
    status = Column(Integer, nullable=False, comment="1: 正常 2: 调试 3: 废弃")

    def __init__(self, ws_id: int, project_id: int, code_value: int, desc: str, create_user: int, status: int = 2):
        self.ws_id = ws_id
        self.project_id = project_id
        self.code_value = code_value
        self.desc = desc
        self.status = status
        self.create_user = create_user
        self.update_user = create_user
