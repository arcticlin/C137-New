from app.utils.new_logger import logger
from app.core.db_connector import async_session
from app.models.project.project_member import ProjectMemberModel

from sqlalchemy import select, text, and_
from app.handler.db_bulk import DatabaseBulk


class ProjectMCrud:
    @staticmethod
    async def exists_member(project_id: int, user_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM project_member
                    WHERE project_id = :project_id AND user_id = :user_id AND deleted_at = 0
                ) AS is_exists
            """
            )
            result = await session.execute(smtm, {"project_id": project_id, "user_id": user_id})
            return result.scalars().first()

    @staticmethod
    async def member_is_creator(project_id: int, user_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS(
                    SELECT 1
                    FROM project p
                    LEFT JOIN project_member pm on p.project_id = pm.project_id AND pm.user_id= :user_id
                    WHERE p.project_id = :project_id AND p.deleted_at = 0 AND (p.create_user = :user_id OR pm.role=3)
                ) as is_creator
                
                """
            )
            result = await session.execute(smtm, {"project_id": project_id, "user_id": user_id})
            return result.scalars().first()

    @staticmethod
    async def query_project_members(project_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ProjectMemberModel).where(
                    and_(ProjectMemberModel.project_id == project_id, ProjectMemberModel.deleted_at == 0)
                )
            )
            return smtm.scalars().all()

    @staticmethod
    async def add_member(project_id: int, user_id: int, operator: int, role: int = 1):
        logger.info(f"{operator}: 添加项目成员", user_id)
        async with async_session() as session:
            async with session.begin():
                m = ProjectMemberModel(project_id=project_id, role=role, user_id=user_id, create_user=operator)
                session.add(m)
                await session.flush()
                session.expunge(m)

    @staticmethod
    async def remove_member(project_id: int, member_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                member_info = await session.execute(
                    select(ProjectMemberModel).where(
                        and_(
                            ProjectMemberModel.project_id == project_id,
                            ProjectMemberModel.user_id == member_id,
                            ProjectMemberModel.deleted_at == 0,
                        )
                    )
                )
                DatabaseBulk.delete_model(member_info.scalar_one(), operator)
                await session.flush()

    @staticmethod
    async def update_member(project_id: int, member_id: int, member_role: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                member_info = await session.execute(
                    select(ProjectMemberModel).where(
                        and_(
                            ProjectMemberModel.project_id == project_id,
                            ProjectMemberModel.user_id == member_id,
                            ProjectMemberModel.deleted_at == 0,
                        )
                    )
                )
                DatabaseBulk.update_model(member_info.scalar_one(), {"role": member_role}, operator)
                await session.flush()

    @staticmethod
    async def exit_member(project_id: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                member_info = await session.execute(
                    select(ProjectMemberModel).where(
                        and_(
                            ProjectMemberModel.project_id == project_id,
                            ProjectMemberModel.user_id == operator,
                            ProjectMemberModel.deleted_at == 0,
                        )
                    )
                )
                DatabaseBulk.delete_model(member_info.scalar_one(), operator)
                await session.flush()
