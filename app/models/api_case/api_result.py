# coding=utf-8
"""
File: api_result.py
Author: bot
Created: 2023/9/27
Description:
"""
import json
from typing import Union

from sqlalchemy import Column, Integer, TEXT, String, ForeignKey, JSON, BOOLEAN, FLOAT
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiCaseResultModel(Base, BaseMixin):
    __tablename__ = "api_result"

    id = Column(Integer, primary_key=True)

    case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="绑定用例ID", index=True)
    report_id = Column(String(64), ForeignKey("api_report.report_id"), comment="绑定报告ID", index=True)

    result = Column(TEXT, comment="用例结果")
    run_log = Column(TEXT, comment="执行日志")
    elapsed = Column(FLOAT, comment="用例耗时")
    assert_result = Column(TEXT)

    def __init__(
        self,
        case_id: int,
        report_id: str,
        result: Union[dict, str],
        run_log: Union[dict, str],
        elapsed: float = None,
        assert_result: bool = None,
    ):
        self.case_id = case_id
        self.report_id = report_id
        self.result = json.dumps(result, ensure_ascii=False) if isinstance(result, dict) else result
        self.run_log = json.dumps(run_log, ensure_ascii=False) if isinstance(run_log, dict) else run_log
        self.assert_result = assert_result
        self.elapsed = elapsed
