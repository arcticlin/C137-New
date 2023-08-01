from app.utils.logger import Log
from app.core.db_connector import async_session
from app.models.project.project_member import ProjectMemberModel
from app.enums.enum_project import ProjectRoleEnum


class ProjectMCrud:

    log = Log("ProjectMCrud")

    @staticmethod
    async def add_member(project_id: int, role: int, user_id: int, operator: int):
        ProjectMCrud.log.d_info(operator, "添加项目成员", user_id)
        async with async_session() as session:
            async with session.begin():
                m = ProjectMemberModel(
                    project_id=project_id,
                    role=ProjectRoleEnum(role),
                    user_id=user_id,
                    create_user=operator
                )
                session.add(m)
                await session.flush()
                session.expunge(m)