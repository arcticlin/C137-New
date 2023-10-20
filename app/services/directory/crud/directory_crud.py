# coding=utf-8
"""
File: directory_crud.py
Author: bot
Created: 2023/10/20
Description:
"""
from datetime import datetime
from typing import List, Dict

from sqlalchemy import text

from app.core.db_connector import async_session
from app.models.project.project_directory import PDirectoryModel
from app.services.directory.schema.dir_new import DirectoryNew


class DirectoryCrud:
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
    async def n_get_project_directory_tree(project_id: int):
        async with async_session() as session:
            smtm = """
                    SELECT d.directory_id, d.name, d.parent_id, (SELECT COUNT(case_id) FROM api_case AS ac WHERE ac.directory_id = d.directory_id AND ac.deleted_at = 0) AS has_case
                    FROM directory AS d
                    WHERE project_id = :project_id  AND deleted_at =0
                """
            execute = await session.execute(text(smtm), {"project_id": project_id})
            return execute.all()

    @staticmethod
    async def add_project_dir(data: DirectoryNew, creator: int) -> int:
        async with async_session() as session:
            async with session.begin():
                directory = PDirectoryModel(**data.dict(), create_user=creator)
                session.add(directory)
                await session.flush()
                session.expunge(directory)
                return directory.directory_id

    @staticmethod
    async def pd_name_exists(name: str, project_id: int = None, directory_id: int = None) -> bool:
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
    async def pd_is_exists(directory_id: int) -> bool:
        """检查项目是否存在"""
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
    async def verify_permission_in_directory(directory_id: int, user_id: int):
        """检查用户是否有权限操作目录"""
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
    async def get_case_list_in_directory(directory_id: int):
        """返回目录的用例列表"""
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
    async def update_project_dir_name(directory_id: int, name: str, operator: int):
        """更新目录名称"""
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
    async def check_directory_permission(project_id: int, directory_id: int):
        """
        检查目录以及权限, 当前用户是否有权限操作目录, 当项目成员权限大于1时, 有权限
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
                        ON d.project_id = pm.project_id
                        WHERE d.directory_id = :directory_id AND d.project_id = :project_id  AND d.deleted_at = 0 AND pm.deleted_at = 0 AND pm.role > 1
                    ) AS subquery
                    GROUP BY 
                        directory_id
                """
            )
            result = await session.execute(smtm, {"project_id": project_id, "directory_id": directory_id})
            return result.first()

    @staticmethod
    async def delete_dir(directory_id: int, operator: int) -> None:
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
