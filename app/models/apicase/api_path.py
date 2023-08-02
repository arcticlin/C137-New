# coding=utf-8
"""
File: api_path.py
Author: bot
Created: 2023/8/2
Description:
"""
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, TEXT

from app.core.db_connector import Base, BaseMixin


class ApiPathModel(Base, BaseMixin):
    __tablename__ = "api_path"

    path_id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(32), nullable=False, comment="参数名称")
    value = Column(TEXT, nullable=False, comment="参数值")
    types = Column(Integer, nullable=False, comment="类型, 1: Path, 2: Query", index=True)
    enable = Column(BOOLEAN, default=True, comment="是否启用")
    comment = Column(String(32), comment="备注")
    case_id = Column(Integer, ForeignKey("api_case.case_id"), index=True)

    def __init__(self, key: str, value: str, types: int, enable: bool, case_id: int, comment: str = None):
        self.key = key
        self.value = value
        self.types = types
        self.enable = enable
        self.case_id = case_id
        self.comment = comment
