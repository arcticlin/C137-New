# coding=utf-8
"""
File: project_directory_crud.py
Author: bot
Created: 2023/8/1
Description:
"""
from datetime import datetime

from sqlalchemy.orm import aliased

from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest, DeletePDirectoryRequest
from app.utils.logger import Log
from app.core.db_connector import async_session
from app.models.project.project_directory import PDirectoryModel
from sqlalchemy import func, select, and_, or_


class PDirectoryCrud:
    log = Log("PDirectoryCrud")

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
    async def delete_project_dir(project_id: int, data: DeletePDirectoryRequest, operator: int):
        async with async_session() as session:
            current_dir = await session.execute(
                select(PDirectoryModel).where(and_(PDirectoryModel.directory_id == data.directory_id))
            )
            current_dir_result = current_dir.scalars().first()
            current_dir_result.deleted_at = int(datetime.now().timestamp())

    @staticmethod
    async def get_descendant_ids(parent_id):
        async with async_session() as session:
            subquery = select(PDirectoryModel.directory_id).where(PDirectoryModel.parent_id == parent_id).alias()
            descendant_ids = subquery
            async for descendant_id in session.execute(descendant_ids):
                yield descendant_id[0]
                async for child_id in PDirectoryCrud.get_descendant_ids(session, descendant_id[0]):
                    yield child_id
