# coding=utf-8
"""
File: project_env.py
Author: bot
Created: 2023/8/4
Description:
"""
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey

from app.core.db_connector import Base, BaseMixin


class ProjectEnvModel(Base, BaseMixin):
    __tablename__ = "project_env"

    env_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    env_name = Column(String(16), nullable=False, comment="环境名称", index=True)

    env_url = Column(TEXT, nullable=False)
