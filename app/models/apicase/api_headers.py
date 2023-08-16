# coding=utf-8
"""
File: api_headers.py
Author: bot
Created: 2023/8/2
Description:
"""
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, TEXT

from app.core.db_connector import Base, BaseMixin


class ApiHeadersModel(Base, BaseMixin):
    __tablename__ = "api_headers"

    header_id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(32), nullable=False, comment="参数名称")
    value = Column(TEXT, nullable=False, comment="参数值")
    value_type = Column(Integer, nullable=False, comment="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    enable = Column(BOOLEAN, default=True, comment="是否启用")
    comment = Column(String(32), comment="备注")
    case_id = Column(Integer, ForeignKey("api_case.case_id"), index=True)
    env_id = Column(Integer, ForeignKey("env.env_id"), index=True)

    def __init__(
        self,
        key: str,
        value: str,
        value_type: int,
        enable: bool,
        case_id: int = None,
        env_id: int = None,
        comment: str = None,
    ):
        self.keys = key
        self.value = value
        self.value_type = value_type
        self.enable = enable
        self.case_id = case_id
        self.comment = comment
        self.env_id = env_id
