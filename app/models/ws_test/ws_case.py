# coding=utf-8
"""
File: ws_case.py
Author: bot
Created: 2023/11/20
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, TEXT, ForeignKey


class WsCaseModel(Base, BaseMixin):
    __tablename__ = "ws_case"

    case_id = Column(Integer, primary_key=True)
    ws_id = Column(Integer, ForeignKey("ws_code.ws_id"), nullable=False)
    case_desc = Column(TEXT, nullable=False)
    case_status = Column(Integer, nullable=False, comment="1: 正常 2: 废弃", index=True, default=1)

    def __init__(self, ws_id: int, case_desc: str, create_user: int, case_status: int = 1):
        self.ws_id = ws_id
        self.case_desc = case_desc
        self.case_status = case_status
        self.create_user = create_user
        self.update_user = create_user
