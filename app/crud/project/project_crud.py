# coding=utf-8
"""
File: project_crud.py
Author: bot
Created: 2023/7/28
Description:
"""
from datetime import datetime
from typing import List, Dict

from app.models.apicase.api_case import ApiCaseModel
from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest
from app.utils.new_logger import logger
from app.models.project.project import ProjectModel


from sqlalchemy import select, and_, or_, text

from app.core.db_connector import async_session

from app.enums.enum_project import ProjectRoleEnum
from app.models.project.project_member import ProjectMemberModel
from app.handler.db_bulk import DatabaseBulk
from app.models.project.project_directory import PDirectoryModel


class ProjectCrud:
    @staticmethod
    def another_build_directory_tree(data: List[Dict]):
        directory_map = {item["directory_id"]: item for item in data}
        root = []

        for item in data:
            parent_id = item.get("parent_id")
            if parent_id is None:
                root.append(item)
            else:
                parent = directory_map.get(parent_id)
                if parent is not None:
                    children = parent.setdefault("children", [])
                    children.append(item)
        return root

    @staticmethod
    async def query_project(project_id: int):
        async with async_session() as session:
            smtm = select(ProjectModel).where(and_(ProjectModel.project_id == project_id, ProjectModel.deleted_at == 0))
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
        logger.info(f"{creator}: 创建项目: {data.project_name}")
        async with async_session() as session:
            async with session.begin():
                project = ProjectModel(**data.dict(), create_user=creator)
                session.add(project)
                await session.flush()
                # 创建项目的同时添加进成员表中进行记录
                logger.info(f"{creator}: 创建添加用户: {creator}进项目")
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
        async with async_session() as session:
            async with session.begin():
                smtm_case = text(
                    """
                    UPDATE api_case c 
                    INNER JOIN directory d 
                    ON c.directory_id = d.directory_id 
                    SET c.deleted_at = :deleted_at, c.update_user = :operator 
                    WHERE d.project_id = :project_id AND c.deleted_at = 0
                """
                )
                smtm_dir = text(
                    """
                    UPDATE directory 
                    SET deleted_at = :deleted_at, update_user = :operator 
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                smtm_pm = text(
                    """
                    UPDATE project_member 
                    SET deleted_at = :deleted_at, update_user = :operator 
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                smtm_project = text(
                    """
                    UPDATE project 
                    SET deleted_at = :deleted_at, update_user = :operator 
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的用例")
                await session.execute(
                    smtm_case,
                    {"deleted_at": int(datetime.now().timestamp()), "operator": operator, "project_id": project_id},
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的目录")
                await session.execute(
                    smtm_dir,
                    {"deleted_at": int(datetime.now().timestamp()), "operator": operator, "project_id": project_id},
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的成员")
                await session.execute(
                    smtm_pm,
                    {"deleted_at": int(datetime.now().timestamp()), "operator": operator, "project_id": project_id},
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的项目")
                await session.execute(
                    smtm_project,
                    {"deleted_at": int(datetime.now().timestamp()), "operator": operator, "project_id": project_id},
                )
                await session.flush()

    @staticmethod
    async def update_project(data: UpdateProjectRequest, operator: int):
        logger.info(f"{operator}: 修改信息项目: {data.dict()}")
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(ProjectModel).where(
                        and_(
                            ProjectModel.project_id == data.project_id,
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
            # smtm = select(ProjectModel).join(
            #     ProjectMemberModel,
            #     and_(
            #         ProjectModel.project_id == ProjectMemberModel.project_id,
            #         ProjectMemberModel.user_id == user_id,
            #     ),
            # )
            smtm_case_count = text(
                """
                SELECT 
                    p.project_id, p.project_name, p.create_user, UNIX_TIMESTAMP(p.created_at), UNIX_TIMESTAMP(p.updated_at),p.public,p.project_avatar,IFNULL(COUNT(ac.case_id), 0) AS case_count, COUNT(pm.id) AS member_count
                FROM project p
                LEFT JOIN directory d on p.project_id = d.project_id AND d.deleted_at = 0
                LEFT JOIN api_case ac on d.directory_id = ac.directory_id AND ac.deleted_at = 0
                LEFT JOIN project_member pm on p.project_id = pm.project_id AND pm.deleted_at = 0
                WHERE p.deleted_at = 0 AND p.project_id IN (SELECT project_id FROM project_member WHERE user_id = :user_id AND deleted_at = 0)
                GROUP BY p.project_id, p.project_name
            """
            )
            smtm_case_count = await session.execute(smtm_case_count, {"user_id": user_id})
            result = smtm_case_count.all()
            # execute_member = await session.execute(smtm)
            # result = execute_member.scalars().all()
            return result

    @staticmethod
    async def member_role_in_project(user_id: int, project_id: int):
        async with async_session() as session:
            smtm = select(ProjectMemberModel).where(
                and_(
                    ProjectMemberModel.project_id == project_id,
                    ProjectMemberModel.user_id == user_id,
                    ProjectMemberModel.deleted_at == 0,
                )
            )
            result = await session.execute(smtm)
            user_role = result.scalars().first()
            if user_role is None:
                return None
            return user_role.role

    @staticmethod
    async def add_project_member(
        project_id: int, user_id: int, operator: int, role: ProjectRoleEnum = ProjectRoleEnum.MEMBER
    ):
        async with async_session() as session:
            async with session.begin():
                member = ProjectMemberModel(
                    project_id=project_id,
                    user_id=user_id,
                    create_user=operator,
                    role=role,
                )
                session.add(member)

    @staticmethod
    async def query_project_member(project_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ProjectMemberModel).where(
                    and_(
                        ProjectMemberModel.project_id == project_id,
                        ProjectMemberModel.deleted_at == 0,
                    )
                )
            )
            return smtm.scalars().all()

    @staticmethod
    async def n_get_project_directory_tree(project_id: int):
        async with async_session() as session:
            smtm = """
                SELECT d.directory_id, d.name, d.parent_id, (SELECT COUNT(case_id) FROM api_case AS ac WHERE ac.directory_id = d.directory_id AND ac.deleted_at = 0) AS has_case
                FROM directory AS d
                WHERE project_id = :project_id  AND deleted_at =0
            """
            execute = await session.execute(text(smtm), {"project_id": project_id})
            return execute.all()
