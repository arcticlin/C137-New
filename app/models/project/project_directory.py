# coding=utf-8
"""
File: project_directory.py
Author: bot
Created: 2023/8/1
Description:
"""

from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String


class PDirectoryModel(Base, BaseMixin):
    __tablename__ = "directory"

    directory_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False)
    parent_id = Column(Integer, default=None)

    def __init__(self, name: str, project_id: int, create_user: int, parent_id: int = 0):
        self.create_user = create_user
        self.name = name
        self.parent_id = parent_id
        self.project_id = project_id
