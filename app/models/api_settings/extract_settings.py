# coding=utf-8
"""
File: extract_settings.py
Author: bot
Created: 2023/8/7
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class ExtractModel(Base, BaseMixin):
    __tablename__ = "common_extract"

    extract_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False, comment="提取变量名称")
    description = Column(String(64), comment="提取变量描述")
    enable = Column(BOOLEAN, nullable=False, comment="是否启用")

    case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="绑定用例ID")

    extract_from = Column(Integer, nullable=False, comment="提取来源, 1: res-header 2: res-body 3: res-cookie")
    extract_type = Column(Integer, nullable=False, comment="提取类型, 1: jsonpath 2: 正则")
    extract_exp = Column(TEXT, nullable=False, comment="提取表达式")
    extract_out_name = Column(String(16), nullable=False, comment="提取出参名")
    extract_index = Column(Integer, comment="提取顺序")

    def __init__(
        self,
        name: str,
        case_id: int,
        extract_from: int,
        extract_type: int,
        extract_exp: str,
        extract_out_name: str,
        description: str = None,
        extract_index: int = None,
        enable: bool = True,
    ):
        self.name = name
        self.enable = enable
        self.case_id = case_id
        self.extract_from = extract_from
        self.extract_type = extract_type
        self.extract_exp = extract_exp
        self.extract_out_name = extract_out_name
        self.description = description
        self.extract_index = extract_index
