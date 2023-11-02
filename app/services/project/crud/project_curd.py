# coding=utf-8
"""
File: project_crud.py
Author: bot
Created: 2023/7/28
Description:
"""
from datetime import datetime
from typing import List, Dict
from loguru import logger
from app.models.project.project import ProjectModel
from sqlalchemy import select, and_, or_, text
from app.core.db_connector import async_session
from app.models.project.project_member import ProjectMemberModel
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.services.project.schema.project_new import ProjectNewRequest
from app.services.project.schema.project_update import ProjectUpdateRequest


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
    async def exists_project_name(name: str, creator: int):
        async with async_session() as session:
            """
            查询项目是否存在:
                1. 当项目为公开时, 任何用户无法创建同名项目
                2. 当项目为私密时, 不同用户可以创建同名项目
                3. 当创建人为同一人时, 不可以创建同名项目
            """
            smtm = """
                SELECT EXISTS(
                    SELECT 1 
                    FROM project 
                    WHERE project_name=:name AND deleted_at = 0 AND (public = true OR create_user= :create_user)
                    ) AS is_exists;
            """
            result = await session.execute(text(smtm), {"name": name, "create_user": creator})
            return result.scalars().first()

    @staticmethod
    async def exists_project_id(project_id: int):
        """
        查询项目是否存在
        """
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS(
                    SELECT 1
                    FROM project
                    WHERE project_id=:project_id AND deleted_at = 0
                )
            """
            )
            result = await session.execute(smtm, {"project_id": project_id})
            return result.scalars().first()

    @staticmethod
    async def user_has_permission(project_id: int, operator: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT
                  CASE
                    WHEN 
                      (p.create_user =:user_id) 
                      OR 
                      (pm.user_id = :user_id AND pm.role > 1 AND pm.deleted_at = 0)
                    THEN 1 ELSE 0
                  END AS has_permission
                FROM project p
                LEFT JOIN
                  project_member pm ON p.project_id = pm.project_id AND pm.user_id=:user_id
                WHERE p.project_id = :project_id AND p.deleted_at = 0
            """
            )
            result = await session.execute(smtm, {"project_id": project_id, "user_id": operator})
            return result.scalars().first()

    @staticmethod
    async def user_in():
        pass

    @staticmethod
    async def query_project(project_id: int):
        async with async_session() as session:
            smtm = select(ProjectModel).where(and_(ProjectModel.project_id == project_id, ProjectModel.deleted_at == 0))
            execute = await session.execute(smtm)
            result = execute.scalars().first()
            return result

    @staticmethod
    async def add_project(data: ProjectNewRequest, creator: int):
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
                    role=3,
                    user_id=creator,
                    create_user=creator,
                )
                session.add(add_member)
                await session.flush()
                session.expunge(add_member)
                return project.project_id

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        """
        删除项目: 删除项目和目录和成员和用例
        """
        async with async_session() as session:
            async with session.begin():
                smtm_case = text(
                    """
                    UPDATE api_case c 
                    INNER JOIN directory d 
                    ON c.directory_id = d.directory_id 
                    SET c.deleted_at = :deleted_at, c.update_user = :operator, c.updated_at = :updated_at
                    WHERE d.project_id = :project_id AND c.deleted_at = 0
                """
                )
                smtm_dir = text(
                    """
                    UPDATE directory 
                    SET deleted_at = :deleted_at, update_user = :operator ,updated_at = :updated_at
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                smtm_pm = text(
                    """
                    UPDATE project_member 
                    SET deleted_at = :deleted_at, update_user = :operator , updated_at = :updated_at
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                smtm_project = text(
                    """
                    UPDATE project 
                    SET deleted_at = :deleted_at, update_user = :operator , updated_at = :updated_at
                    WHERE project_id = :project_id AND deleted_at = 0
                """
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的用例")
                await session.execute(
                    smtm_case,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "operator": operator,
                        "project_id": project_id,
                        "updated_at": datetime.now(),
                    },
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的目录")
                await session.execute(
                    smtm_dir,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "operator": operator,
                        "project_id": project_id,
                        "updated_at": datetime.now(),
                    },
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的成员")
                await session.execute(
                    smtm_pm,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "operator": operator,
                        "project_id": project_id,
                        "updated_at": datetime.now(),
                    },
                )
                logger.debug(f"{operator}: 删除项目: {project_id} 关联的项目")
                await session.execute(
                    smtm_project,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "operator": operator,
                        "project_id": project_id,
                        "updated_at": datetime.now(),
                    },
                )
                await session.flush()

    @staticmethod
    async def update_project(project_id: int, data: ProjectUpdateRequest, operator: int):
        logger.info(f"{operator}: 修改信息项目: {data.dict()}")
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
            """
            查询用户可查看的项目列表(我创建, 我参与, 公开的项目)并统计项目下的用例数和成员数
            """
            smtm_case_count = text(
                """
                SELECT 
                    p.project_id, p.project_name, p.create_user, UNIX_TIMESTAMP(p.created_at), UNIX_TIMESTAMP(p.updated_at),p.public,p.project_avatar,IFNULL(COUNT(DISTINCT ac.case_id), 0) AS total_case,IFNULL(COUNT(DISTINCT acd.case_id), 0) AS today_case,COUNT(DISTINCT pm.id) AS members
                FROM 
                    project p
                LEFT JOIN 
                    directory d on p.project_id = d.project_id AND d.deleted_at = 0
                LEFT JOIN 
                    api_case ac on d.directory_id = ac.directory_id AND ac.deleted_at = 0
                LEFT JOIN 
                    api_case acd on d.directory_id = acd.directory_id AND acd.deleted_at = 0 AND DATE(acd.created_at) = CURDATE()
                LEFT JOIN 
                    project_member pm on p.project_id = pm.project_id AND pm.deleted_at = 0
                WHERE 
                p.deleted_at = 0 
                AND p.project_id IN 
                    (
                        SELECT project_id FROM project_member WHERE user_id = :user_id AND deleted_at = 0
                    )
                GROUP BY p.project_id
            """
            )
            smtm_case_count = await session.execute(smtm_case_count, {"user_id": user_id})
            result = smtm_case_count.all()
            print(result)
            # execute_member = await session.execute(smtm)
            # result = execute_member.scalars().all()
            return result

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
