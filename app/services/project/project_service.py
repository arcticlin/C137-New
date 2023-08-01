from app.crud.project.project_crud import ProjectCrud
from app.crud.project.project_directory_crud import PDirectoryCrud
from app.enums.enum_project import ProjectRoleEnum
from app.exceptions.commom_exception import CustomException
from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest
from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest, AddProjectMemberRequest
from app.utils.logger import Log
from app.exceptions.project_exp import *


class ProjectService:
    log = Log("ProjectService")

    @staticmethod
    async def add_project(data: AddProjectRequest, creator: int):
        if await ProjectCrud.query_project_by_name(data.project_name):
            raise CustomException(PROJECT_NAME_EXISTS)
        await ProjectCrud.add_project(data, creator)

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        project = await ProjectCrud.query_project(project_id)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.delete_project(project_id, operator)

    @staticmethod
    async def update_project(project_id: int, data: UpdateProjectRequest, operator: int):
        project = await ProjectCrud.query_project(project_id)
        print("Here", project)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.update_project(project_id, data, operator)

    @staticmethod
    async def add_project_member(project_id: int, data: AddProjectMemberRequest, operator: int):
        operator_role = await ProjectCrud.member_role_in_project(project_id, operator)
        if not operator_role:
            raise CustomException(PROJECT_NOT_CREATOR)
        if operator_role == ProjectRoleEnum.MEMBER:
            raise CustomException(PROJECT_NOT_CREATOR)
        if await ProjectCrud.member_role_in_project(project_id, data.user_id):
            raise CustomException(PROJECT_MEMBER_EXISTS)
        await ProjectCrud.add_project_member(
            project_id=project_id, user_id=data.user_id, role=data.role, operator=operator
        )

    @staticmethod
    async def get_project_detail(project_id: int):
        project_info = await ProjectCrud.query_project(project_id)
        project_member = await ProjectCrud.query_project_member(project_id)
        orm_project_member = C137Response.orm_with_list(project_member, "id", "updated_at", "deleted_at", "project_id")
        return {
            "project_info": C137Response.orm_to_dict(project_info),
            "project_member": orm_project_member,
        }

    @staticmethod
    async def get_project_dir(project_id: int, directory_id: int = None):
        if directory_id is None or directory_id == 0:
            result = await ProjectCrud.get_project_dir_root(project_id)
        else:
            result = await PDirectoryCrud.get_project_dir_and_case(directory_id)
        tree = []
        for item in result:
            temp = C137Response.orm_to_dict(
                item, "create_user", "update_user", "created_at", "updated_at", "deleted_at", "project_id"
            )
            count = await PDirectoryCrud.query_dir_has_child(item.directory_id)
            temp.__setitem__("has_child", count != 0)
            tree.append(temp)
        return tree

    @staticmethod
    async def add_project_dir(project_id: int, data: AddPDirectoryRequest, creator: int):
        if await PDirectoryCrud.pd_name_exists(project_id, data.name):
            raise CustomException(PD_NAME_EXISTS)
        await PDirectoryCrud.add_project_dir(project_id, data, creator)

    @staticmethod
    async def delete_project_dir(directory_id: int, operator: int):
        pass
