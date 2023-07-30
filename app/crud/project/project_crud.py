# coding=utf-8
"""
File: project_crud.py
Author: bot
Created: 2023/7/28
Description:
"""
from datetime import datetime

from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest
from app.utils.logger import Log
from app.models.project.project import ProjectModel
from app.models.project.project_member import ProjectMemberModel

from sqlalchemy import select, and_, or_

from app.core.db_connector import async_session
from app.handler.response_handler import C137Response
from sqlalchemy.orm import selectinload
from app.crud.project.project_member_crud import ProjectMCrud
from app.enums.enum_project import ProjectRoleEnum
from app.models.project.project_member import ProjectMemberModel
from app.handler.db_bulk import DatabaseBulk


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
            return result

    @staticmethod
    async def query_project_by_name(project_name: str):
        async with async_session() as session:
            smtm = select(ProjectModel).where(
                and_(
                    ProjectModel.project_name == project_name,
                    ProjectModel.deleted_at == 0,
                )
            )
            execute = await session.execute(smtm)
            result = execute.scalars().first()
            return result

    @staticmethod
    async def add_project(data: AddProjectRequest, creator: int):
        ProjectCrud.log.d_info(creator, f"创建项目: {data.project_name}")
        async with async_session() as session:
            async with session.begin():
                project = ProjectModel(**data.dict(), create_user=creator)
                session.add(project)
                await session.flush()
                # 创建项目的同时添加进成员表中进行记录
                ProjectCrud.log.d_info(creator, f"创建添加用户: {creator}进项目")
                add_member = ProjectMemberModel(
                    project_id=project.project_id,
                    role=ProjectRoleEnum.CREATOR,
                    user_id=creator,
                    create_user=creator,
                )
                session.add(add_member)
                await session.flush()
                session.expunge(add_member)

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        ProjectCrud.log.d_info(operator, f"删除项目: {project_id}")
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ProjectModel).where(
                        and_(
                            ProjectModel.project_id == project_id,
                            ProjectModel.deleted_at == 0,
                        )
                    )
                )
                result = smtm.scalars().first()
                result.deleted_at = int(datetime.now().timestamp())
                result.update_user = operator
                await session.flush()
                session.expunge(result)

    @staticmethod
    async def update_project(
        project_id: int, data: UpdateProjectRequest, operator: int
    ):
        ProjectCrud.log.d_info(operator, f"修改信息项目: {data.dict()}")
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ProjectModel).where(
                        and_(
                            ProjectModel.project_id == project_id,
                            ProjectModel.deleted_at == 0,
                        )
                    )
                )
                result = smtm.scalars().first()
                DatabaseBulk.update_model(result, data.dict(), operator)
                await session.flush()

    @staticmethod
    async def get_project_list(user_id: int):
        async with async_session() as session:
            # 我创建或我参与的项目
            smtm = select(ProjectModel).join(
                ProjectMemberModel,
                and_(
                    ProjectModel.project_id == ProjectMemberModel.project_id,
                    ProjectMemberModel.user_id == user_id,
                ),
            )

            execute_member = await session.execute(smtm)
            result = execute_member.scalars().all()
            return result
