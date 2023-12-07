# coding=utf-8
"""
File: ws_result.py
Author: bot
Created: 2023/11/20
Description:
"""
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, TEXT, ForeignKey


class WsResultModel(Base, BaseMixin):
    __tablename__ = "ws_result"
    result_id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("ws_plan.plan_id"), nullable=False)
    ws_id = Column(Integer, ForeignKey("ws_code.ws_id"), nullable=False)
    case_id = Column(Integer, ForeignKey("ws_case.case_id"), nullable=False)
    result_desc = Column(TEXT(collation="utf8mb4_bin"), nullable=False, comment="Markdown格式的描述")
    result_status = Column(Integer, nullable=False, comment="1: 通过 2: 失败 3: 忽略 4: 未执行")

    # # 关联WsCase表，用relationship建立关系
    # case = relationship("WsCaseModel", backref="ws_result", lazy="dynamic")

    def __init__(self, plan_id: int, ws_id: int, case_id: int, result_desc: str, create_user: int, status: int = 4):
        self.plan_id = plan_id
        self.ws_id = ws_id
        self.case_id = case_id
        self.result_desc = result_desc
        self.result_status = status
        self.create_user = create_user
        self.update_user = create_user
