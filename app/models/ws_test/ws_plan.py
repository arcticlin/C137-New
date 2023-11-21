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


class WsPlanModel(Base, BaseMixin):
    __tablename__ = "ws_plan"
    plan_id = Column(Integer, primary_key=True)
    plan_desc = Column(TEXT, nullable=False)
    plan_status = Column(Integer, nullable=False, comment="1: 进行中 2: 已完成 3: 已废弃 4: 待开始")

    # 关联WsCase表，用relationship建立关系
    cases = relationship("WsCaseModel", backref="ws_plan", lazy="dynamic")

    def __init__(self, plan_desc: str, create_user: int, status: int = 4):
        self.plan_desc = plan_desc
        self.plan_status = status
        self.create_user = create_user
        self.update_user = create_user
