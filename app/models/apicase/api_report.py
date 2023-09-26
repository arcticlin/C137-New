# coding=utf-8
"""
File: api_report.py
Author: bot
Created: 2023/9/26
Description:
"""


from sqlalchemy import Column, Integer, TEXT, String
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiReport(Base, BaseMixin):
    __tablename__ = "api_report"

    id = Column(Integer, primary_key=True)
    report_id = Column(String, nullable=False, index=True, comment="执行时产生的trace_id")

    total = Column(Integer, nullable=False, comment="总用例数")
    success = Column(Integer, nullable=False, comment="成功")
    failed = Column(Integer, nullable=False, comment="失败")
    xfail = Column(Integer, nullable=False, comment="注定失败")
    skip = Column(Integer, nullable=False, comment="跳过")
