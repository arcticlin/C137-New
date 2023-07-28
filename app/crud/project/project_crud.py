# coding=utf-8
"""
File: project_crud.py
Author: bot
Created: 2023/7/28
Description:
"""
from app.utils.logger import Log
from app.models.project.project import ProjectModel
from app.models.project.project_member import ProjectMemberModel

from sqlalchemy import select, and_
from app.core.db_connector import async_session
from app.handler.response_handler import C137Response
from sqlalchemy.orm import selectinload


class ProjectCrud:
    log = Log("ProjectCrud")

    @staticmethod
    async def query_project(project_id: int):
        async with async_session() as session:
            smtm = select(ProjectModel).where(
                and_(
                    ProjectModel.project_id == project_id, ProjectModel.deleted_at == 0
                )
            )
            execute = await session.execute(smtm)
            result = execute.scalars().first()
            print("非外键查询", result, C137Response.orm_to_dict(result))
