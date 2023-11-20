# coding=utf-8
"""
File: ws_plan.py
Author: bot
Created: 2023/11/20
Description:
"""
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, TEXT, ForeignKey


class WsPlan(Base, BaseMixin):
    __tablename__ = "ws_plan"
    plan_id = Column(Integer, primary_key=True)
    ws_id = Column(Integer, ForeignKey("ws.ws_id"), nullable=False)
    plan_desc = Column(TEXT, nullable=False)
    plan_status = Column(Integer, nullable=False, comment="1: 进行中 2: 已完成 3: 已废弃")

    # 关联WsCase表，用relationship建立关系
    cases = relationship("WsCase", backref="ws_plan", lazy="dynamic")
