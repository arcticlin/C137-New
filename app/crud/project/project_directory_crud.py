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
    async def pd_is_exists(directory_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT directory_id FROM `directory` WHERE directory_id=:directory_id AND deleted_at = 0;
            """
            )
            result = await session.execute(smtm, {"directory_id": directory_id})
            if result.first() is not None:
                return True
            else:
                return False

    @staticmethod
    async def pd_name_exists(name: str, project_id: int = None, directory_id: int = None):
        async with async_session() as session:
            if project_id is not None:
                smtm = text(
                    """
                        SELECT directory_id FROM directory WHERE project_id = :project_id AND deleted_at = 0 AND name = :name
                    """
                )
                result = await session.execute(smtm, {"project_id": project_id, "name": name})
            if directory_id is not None:
                smtm = text(
                    """
                        SELECT directory_id  FROM `directory` WHERE name=:name AND deleted_at = 0 AND project_id = (SELECT project_id FROM `directory` WHERE directory_id=:directory_id);
                    """
                )
                result = await session.execute(smtm, {"directory_id": directory_id, "name": name})
            if result.first() is not None:
                return True
            else:
                return False

    @staticmethod
    async def add_project_dir(data: AddPDirectoryRequest, creator: int):
        async with async_session() as session:
            async with session.begin():
                directory = PDirectoryModel(**data.dict(), create_user=creator)
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
    async def update_project_dir_name(directory_id: int, name: str, operator: int):
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

    @staticmethod
    async def get_case_list_in_directory(directory_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT case_id, name, method, priority, status, create_user, updated_at
                FROM api_case
                WHERE deleted_at = 0 AND directory_id = :directory_id
            """
            )
            execute = await session.execute(smtm, {"directory_id": directory_id})
            return execute.all()

    @staticmethod
    async def verify_permission_in_directory(directory_id: int, user_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT 1
                FROM directory AS d
                JOIN project_member AS pm
                ON d.project_id = pm.project_id AND pm.role > 1
                WHERE d.directory_id = :directory_id AND pm.user_id = :user_id AND d.deleted_at = 0
            """
            )
            execute = await session.execute(smtm, {"directory_id": directory_id, "user_id": user_id})
            return execute.first() is not None

    @staticmethod
    async def delete_dir(directory_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm_dir = text(
                    """
                    UPDATE directory AS d
                    SET deleted_at = :deleted_at
                    WHERE deleted_at = 0 AND d.directory_id IN (
                      WITH RECURSIVE DirectoryCTE AS (
                        SELECT directory_id
                        FROM directory
                        WHERE directory_id = :start_directory_id

                        UNION ALL
                    
                        SELECT d2.directory_id
                        FROM directory AS d2
                        JOIN DirectoryCTE cte ON d2.parent_id = cte.directory_id
                      )
                      SELECT directory_id
                      FROM DirectoryCTE
                    );
                """
                )

                smtm_case = text(
                    """
                UPDATE `api_case`
                SET deleted_at = :deleted_at
                WHERE deleted_at = 0 AND directory_id IN (
                  WITH RECURSIVE DirectoryCTE AS (
                    SELECT directory_id
                    FROM directory
                    WHERE directory_id = :start_directory_id
                
                    UNION ALL
                
                    SELECT d2.directory_id
                    FROM directory AS d2
                    JOIN DirectoryCTE cte ON d2.parent_id = cte.directory_id
                  )
                  SELECT directory_id
                  FROM DirectoryCTE
                ) ;
                
                """
                )

                await session.execute(
                    smtm_dir,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "update_user": operator,
                        "start_directory_id": directory_id,
                        "updated_at": datetime.now(),
                    },
                )

                await session.execute(
                    smtm_case,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "update_user": operator,
                        "start_directory_id": directory_id,
                        "updated_at": datetime.now(),
                    },
                )

                await session.flush()
