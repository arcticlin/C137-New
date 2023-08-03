# coding=utf-8
"""
File: project_directory_crud.py
Author: bot
Created: 2023/8/1
Description:
"""
from datetime import datetime


from app.schemas.project.pd_schema import AddPDirectoryRequest

from app.core.db_connector import async_session
from app.models.project.project_directory import PDirectoryModel
from sqlalchemy import func, select, and_, or_, text
from app.utils.new_logger import logger


class PDirectoryCrud:
    @staticmethod
    async def query_dir_has_child(directory_id: int) -> int:
        async with async_session() as session:
            count_ = await session.execute(
                select(func.count(PDirectoryModel.directory_id)).where(
                    and_(PDirectoryModel.parent_id == directory_id, PDirectoryModel.deleted_at == 0)
                )
            )
            count = count_.scalars().first()
            return count

    @staticmethod
    async def get_project_dir_and_case(directory_id: int):
        async with async_session() as session:
            # 根目录
            smtm = select(PDirectoryModel).where(
                and_(
                    PDirectoryModel.parent_id == directory_id,
                    PDirectoryModel.deleted_at == 0,
                ),
            )
            execute = await session.execute(smtm)
            result = execute.scalars().all()

            return result

    @staticmethod
    async def pd_name_exists(project_id: int, name: str):
        async with async_session() as session:
            smtm = await session.execute(
                select(func.count(PDirectoryModel.directory_id)).where(
                    and_(
                        PDirectoryModel.project_id == project_id,
                        PDirectoryModel.deleted_at == 0,
                        PDirectoryModel.name == name,
                    )
                )
            )
            result = smtm.scalars().first()
            if result > 0:
                return True
            return False

    @staticmethod
    async def add_project_dir(project_id: int, data: AddPDirectoryRequest, creator: int):
        async with async_session() as session:
            async with session.begin():
                directory = PDirectoryModel(**data.dict(), create_user=creator, project_id=project_id)
                session.add(directory)
                await session.flush()
                return directory.directory_id

    @staticmethod
    async def check_directory_permission(project_id: int, directory_id: int):
        """
        检查目录以及权限
        返回 directory_id, user_id: [1, 2]
        """
        async with async_session() as session:
            smtm = text(
                """
                    SELECT directory_id, GROUP_CONCAT(user_id) AS user_ids
                    FROM (
                        SELECT d.directory_id, pm.user_id
                        FROM directory AS d
                        JOIN project_member AS pm
                        ON d.project_id = pm.project_id AND pm.role > 1
                        WHERE d.directory_id = :directory_id AND d.project_id = :project_id  AND d.deleted_at = 0
                    ) AS subquery
                    GROUP BY 
                        directory_id
                """
            )
            result = await session.execute(smtm, {"project_id": project_id, "directory_id": directory_id})
            return result.first()

    @staticmethod
    async def delete_project_dir(directory_id: int, operator: int):
        async with async_session() as session:
            smtm = text(
                """
                UPDATE 
                    directory 
                SET 
                    deleted_at = :deleted_at, update_user = :update_user, updated_at = :updated_at WHERE directory_id = :directory_id
            """
            )
            await session.execute(
                smtm,
                {
                    "deleted_at": int(datetime.now().timestamp()),
                    "update_user": operator,
                    "directory_id": directory_id,
                    "updated_at": datetime.now(),
                },
            )
            await session.commit()

    @staticmethod
    async def update_project_dir_name(directory_id: int, name: str, operator: int):
        logger.info("11")
        logger.debug("22")
        async with async_session() as session:
            smtm = text(
                """
                UPDATE directory SET name = :name, update_user = :update_user, updated_at = :updated_at WHERE directory_id = :directory_id
                """
            )
            await session.execute(
                smtm,
                {"name": name, "update_user": operator, "directory_id": directory_id, "updated_at": datetime.now()},
            )
            await session.commit()

    @staticmethod
    async def query_project_directory_root(project_id: int):
        """查询项目根目录并返回是否has_child"""
        async with async_session() as session:
            smtm = text(
                """
            SELECT d.directory_id, d.name, (SELECT
                    CASE
                        WHEN EXISTS(SELECT 1 FROM directory AS sd WHERE sd.parent_id = d.directory_id AND sd.deleted_at = 0)
                        OR EXISTS(SELECT 1 FROM api_case AS ac WHERE ac.directory_id = d.directory_id AND ac.deleted_at = 0)
                        THEN 1
                        ELSE 0
                    END)  AS has_child
            FROM directory AS d
            WHERE project_id = :project_id AND deleted_at = 0 AND (parent_id IS NULL OR parent_id = 0)
            """
            )
            execute = await session.execute(smtm, {"project_id": project_id})
            result = execute.all()
            return result

    @staticmethod
    async def query_directory_children(directory_id: int):
        async with async_session() as session:
            smtm_d = text(
                """
                    SELECT d.directory_id, d.name, d.parent_id, (SELECT
                    CASE
                        WHEN EXISTS(SELECT 1 FROM directory AS sd WHERE sd.parent_id = d.directory_id AND sd.deleted_at = 0)
                        OR EXISTS(SELECT 1 FROM api_case AS ac WHERE ac.directory_id = d.directory_id AND ac.deleted_at = 0)
                        THEN 1
                        ELSE 0
                    END)  AS has_child
                    FROM directory AS d
                    WHERE parent_id = :directory_id AND deleted_at = 0
                """
            )
            smtm_c = text(
                """
                    SELECT c.case_id, c.name, c.method, c.directory_id
                    FROM api_case AS c
                    WHERE directory_id = :directory_id AND deleted_at = 0
                """
            )
            execute_d = await session.execute(smtm_d, {"directory_id": directory_id})
            execute_c = await session.execute(smtm_c, {"directory_id": directory_id})

            return execute_d.all(), execute_c.all()

    @staticmethod
    async def check_directory_has_child(directory_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT
                    CASE
                        WHEN EXISTS(SELECT 1 FROM directory AS sd WHERE sd.parent_id = :directory_id AND sd.deleted_at = 0)
                        OR EXISTS(SELECT 1 FROM api_case AS ac WHERE ac.directory_id = :directory_id AND ac.deleted_at = 0)
                        THEN 1
                        ELSE 0
                    END AS has_child
            """
            )
            execute = await session.execute(smtm, {"directory_id": directory_id})
            return execute.scalars().first()
