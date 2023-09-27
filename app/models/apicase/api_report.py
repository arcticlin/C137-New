# coding=utf-8
"""
File: api_report_crud.py
Author: bot
Created: 2023/9/26
Description:
"""


from sqlalchemy import Column, Integer, TEXT, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiReportModel(Base, BaseMixin):
    __tablename__ = "api_report"

    id = Column(Integer, primary_key=True)
    report_id = Column(String(64), nullable=False, comment="报告ID", index=True)
    total = Column(Integer, nullable=False, comment="总用例数")
    success = Column(Integer, nullable=False, comment="成功")
    failed = Column(Integer, nullable=False, comment="失败")
    xfail = Column(Integer, nullable=False, comment="注定失败")
    skip = Column(Integer, nullable=False, comment="跳过")
    duration = Column(Numeric(precision=5, scale=1))

    def __init__(self, report_id: str, total: int, success: int, failed: int, xfail: int, skip: int, duration: float):
        self.report_id = report_id
        self.total = total
        self.success = success
        self.failed = failed
        self.xfail = xfail
        self.skip = skip
        self.duration = duration
