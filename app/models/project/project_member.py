# coding=utf-8
"""
File: projects_member.py
Author: bot
Created: 2023/7/28
Description:
"""
from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from app.enums.enum_project import ProjectRoleEnum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship


class ProjectMemberModel(Base, BaseMixin):
    __tablename__ = "project_member"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer,ForeignKey("project.project_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    role = Column(SqlEnum(ProjectRoleEnum), nullable=False, comment="角色")

    users = relationship("UserModel", backref="project_member")
    project_name = relationship("ProjectModel", backref="project_member")

    def __init__(
        self,
        project_id: int,
        user_id: int,
        create_user: int,
        role: ProjectRoleEnum = ProjectRoleEnum.MEMBER,
    ):
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.create_user = create_user
