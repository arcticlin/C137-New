import json
from datetime import datetime

from app.crud.project.project_crud import ProjectCrud
from app.crud.project.project_directory_crud import PDirectoryCrud
from app.enums.enum_project import ProjectRoleEnum
from app.exceptions.commom_exception import CustomException
from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest
from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest, AddProjectMemberRequest
from app.utils.new_logger import logger
from app.exceptions.project_exp import *
from app.utils.sql_checker import SqlChecker


class ProjectService:
    @staticmethod
    async def add_project(data: AddProjectRequest, creator: int):
        logger.debug(f"{creator} => 创建项目")
        if await ProjectCrud.query_project_by_name(data.project_name):
            raise CustomException(PROJECT_NAME_EXISTS)
        await ProjectCrud.add_project(data, creator)

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        logger.debug(f"{operator} => 删除项目: {project_id}")
        project = await ProjectCrud.query_project(project_id)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.delete_project(project_id, operator)

    @staticmethod
    async def update_project(project_id: int, data: UpdateProjectRequest, operator: int):
        logger.debug(f"{operator} => 更新项目: {project_id}")
        project = await ProjectCrud.query_project(project_id)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.update_project(project_id, data, operator)

    @staticmethod
    async def add_project_member(project_id: int, data: AddProjectMemberRequest, operator: int):
        logger.debug(f"{operator} => 添加项目: {project_id} 成员: {data.user_id}")
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
        logger.debug(f"查询项目: {project_id}详情")
        project_info = await ProjectCrud.query_project(project_id)
        project_member = await ProjectCrud.query_project_member(project_id)
        orm_project_member = C137Response.orm_with_list(project_member, "id", "updated_at", "deleted_at", "project_id")
        return {
            "project_info": C137Response.orm_to_dict(project_info),
            "project_member": orm_project_member,
        }

    @staticmethod
    async def add_project_dir(project_id: int, data: AddPDirectoryRequest, creator: int):
        logger.debug(f"{creator} => 添加项目: {project_id} 目录")
        if await PDirectoryCrud.pd_name_exists(project_id, data.name):
            raise CustomException(PD_NAME_EXISTS)
        await PDirectoryCrud.add_project_dir(project_id, data, creator)

    @staticmethod
    async def delete_project_dir(project_id: int, directory_id: int, operator: int):
        logger.debug(f"{operator} => 删除项目: {project_id} 目录")
        check = await PDirectoryCrud.check_directory_permission(project_id, directory_id)
        if check is None:
            raise CustomException(PD_NOT_EXISTS)
        check_d, check_u = check
        if not SqlChecker().check_permission(operator, check_u):
            raise CustomException(PD_NOT_ALLOW)
        await PDirectoryCrud.delete_project_dir(directory_id, operator)

    @staticmethod
    async def update_project_dir_name(project_id: int, directory_id: int, name: str, operator: int):
        logger.debug(f"{operator} => 更新项目: {project_id} 目录信息")
        check = await PDirectoryCrud.check_directory_permission(project_id, directory_id)
        if check is None:
            raise CustomException(PD_NOT_EXISTS)
        check_d, check_u = check
        if not SqlChecker().check_permission(operator, check_u):
            raise CustomException(PD_NOT_ALLOW)
        await PDirectoryCrud.update_project_dir_name(directory_id, name, operator)

    @staticmethod
    async def get_project_root_dir(project_id: int):
        logger.debug(f"查询项目: {project_id} 根目录")
        result = await PDirectoryCrud.query_project_directory_root(project_id)
        temp_result = []
        if result is None:
            return []
        for item in result:
            directory_id, name, has_child = item
            temp_result.append(
                {
                    "directory_id": directory_id,
                    "name": name,
                    "has_child": has_child,
                }
            )
        return temp_result

    @staticmethod
    async def get_directory_children(directory_id: int):
        logger.debug(f"查询目录: {directory_id} 子目录和用例")
        list_dir, list_case = await PDirectoryCrud.query_directory_children(directory_id)
        temp_result = []
        if list_dir is None:
            list_dir = []
        if list_case is None:
            list_case = []
        for item in list_dir:
            t_directory_id, t_name, t_parent_id, t_has_child = item
            temp_result.append(
                {"directory_id": t_directory_id, "name": t_name, "parent_id": t_parent_id, "has_child": t_has_child}
            )

        for item in list_case:
            case_id, name, method, directory_id = item
            temp_result.append({"case_id": case_id, "name": name, "method": method, "parent_id": directory_id})

        return temp_result

    @staticmethod
    async def get_project_directory_tree(project_id: int):
        result = await ProjectCrud.n_get_project_directory_tree(project_id)
        temp_data = []
        for x in result:
            directory_id, name, parent_id, has_case = x
            temp_data.append(
                {
                    "directory_id": directory_id,
                    "name": name,
                    "parent_id": parent_id,
                    "has_case": has_case,
                }
            )

        return ProjectCrud.another_build_directory_tree(temp_data)

    @staticmethod
    async def get_case_list_in_directory(directory_id: int):
        result = await PDirectoryCrud.get_case_list_in_directory(directory_id)
        temp_data = []
        for x in result:
            case_id, name, method, priority, status, create_user, updated_at = x
            temp_data.append(
                {
                    "case_id": case_id,
                    "name": name,
                    "method": method,
                    "priority": priority,
                    "status": status,
                    "create_user": create_user,
                    "updated_at": int(updated_at.timestamp()),
                }
            )
        return temp_data
