# coding=utf-8
"""
File: api_result.py
Author: bot
Created: 2023/9/27
Description:
"""
import json

from sqlalchemy import Column, Integer, TEXT, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiCaseResultModel(Base, BaseMixin):
    __tablename__ = "api_result"

    id = Column(Integer, primary_key=True)

    case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="绑定用例ID", index=True)
    report_id = Column(String(64), ForeignKey("api_report.report_id"), comment="绑定报告ID", index=True)

    result = Column(TEXT, comment="用例结果")

    def __init__(self, case_id: int, report_id: str, result: dict):
        self.case_id = case_id
        self.report_id = report_id
        self.result = json.dumps(result) if isinstance(result, dict) else result
