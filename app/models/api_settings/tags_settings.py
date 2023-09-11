# coding=utf-8
"""
File: tags_settings.py
Author: bot
Created: 2023/9/11
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class TagsModel(Base, BaseMixin):
    __tablename__ = "common_tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(16), nullable=False, comment="标签名称")
    case_id = Column(Integer, nullable=True, comment="绑定用例ID")
    script_id = Column(Integer, nullable=True, comment="绑定脚本ID")

    def __init__(self, tag_name: str, create_user: int, case_id: int = None, script_id: int = None):
        self.create_user = create_user
        self.update_user = create_user
        self.tag_name = tag_name
        self.case_id = case_id
        self.script_id = script_id
