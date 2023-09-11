# coding=utf-8
"""
File: tags_relation.py
Author: bot
Created: 2023/9/11
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class TagsRelationModel(Base, BaseMixin):
    __tablename__ = "common_tags_relation"

    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("common_tags.tag_id"), comment="绑定标签ID", index=True)
    case_id = Column(Integer, nullable=True, comment="绑定用例ID")
    script_id = Column(Integer, nullable=True, comment="绑定脚本ID")

    def __init__(self, tag_id: int, create_user: int, case_id: int = None, script_id: int = None):
        self.create_user = create_user
        self.update_user = create_user
        self.tag_id = tag_id
        self.case_id = case_id
        self.script_id = script_id
