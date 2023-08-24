import json
from datetime import datetime

from app.crud.project.project_crud import ProjectCrud
from app.crud.project.project_directory_crud import PDirectoryCrud
from app.exceptions.commom_exception import CustomException
from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest, DeletePDirectoryRequest
from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest, AddProjectMemberRequest
from app.utils.new_logger import logger
from app.exceptions.project_exp import *
from app.utils.sql_checker import SqlChecker
from app.crud.project.project_member_crud import ProjectMCrud


class ProjectService:
    @staticmethod
    async def add_project(data: AddProjectRequest, creator: int):
        """创建项目"""
        logger.debug(f"{creator} => 创建项目")
        exists = await ProjectCrud.exists_project_name(data.project_name, creator)
        if exists:
            raise CustomException(PROJECT_NAME_EXISTS)
        project_id = await ProjectCrud.add_project(data, creator)
        return project_id

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        """删除项目"""
        logger.debug(f"{operator} => 删除项目: {project_id}")
        exists = await ProjectCrud.exists_project_id(project_id)
        has_permission = await ProjectCrud.user_has_permission(project_id, operator)
        if not exists:
            raise CustomException(PROJECT_NOT_EXISTS)
        if not has_permission:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.delete_project(project_id, operator)

    @staticmethod
    async def update_project(data: UpdateProjectRequest, operator: int):
        """更新项目"""
        logger.debug(f"{operator} => 更新项目: {data.project_id}")
        exists = await ProjectCrud.exists_project_id(data.project_id)
        has_permission = await ProjectCrud.user_has_permission(data.project_id, operator)
        name_exists = await ProjectCrud.exists_project_name(data.project_name, operator)
        if not exists:
            raise CustomException(PROJECT_NOT_EXISTS)
        if not has_permission:
            raise CustomException(PROJECT_NOT_CREATOR)
        if name_exists:
            raise CustomException(PROJECT_NAME_EXISTS)
        await ProjectCrud.update_project(data, operator)

    @staticmethod
    async def add_project_member(project_id: int, data: AddProjectMemberRequest, operator: int):
        logger.debug(f"{operator} => 添加项目: {project_id} 成员: {data.user_id}")
        operator_role = await ProjectCrud.member_role_in_project(project_id, operator)
        if not operator_role:
            raise CustomException(PROJECT_NOT_CREATOR)
        if operator_role == 1:
            raise CustomException(PROJECT_NOT_CREATOR)
        if await ProjectCrud.member_role_in_project(project_id, data.user_id):
            raise CustomException(PROJECT_MEMBER_EXISTS)
        await ProjectCrud.add_project_member(
            project_id=project_id, user_id=data.user_id, role=data.role, operator=operator
        )

    @staticmethod
    async def get_project_list(user_id: int):
        logger.debug(f"查询用户: {user_id} 项目列表")
        result = await ProjectCrud.get_project_list(user_id)
        print(result)
        temp = []
        for item in result:
            (
                project_id,
                project_name,
                create_user,
                create_time,
                update_time,
                public,
                project_avatar,
                case_count,
                member_count,
            ) = item
            temp.append(
                {
                    "project_id": project_id,
                    "project_name": project_name,
                    "create_user": create_user,
                    "created_at": create_time,
                    "updated_at": update_time,
                    "public": public,
                    "project_avatar": project_avatar,
                    "case_count": case_count,
                    "member_count": member_count,
                }
            )
        return temp

    @staticmethod
    async def get_project_detail(project_id: int):
        logger.debug(f"查询项目: {project_id}详情")
        project_info = await ProjectCrud.query_project(project_id)
        return project_info

    @staticmethod
    async def add_project_dir(data: AddPDirectoryRequest, creator: int):
        logger.debug(f"{creator} => 添加项目: {data.project_id} 目录")
        if await PDirectoryCrud.pd_name_exists(name=data.name, project_id=data.project_id):
            raise CustomException(PD_NAME_EXISTS)
        await PDirectoryCrud.add_project_dir(data, creator)

    @staticmethod
    async def delete_directory_new(directory_id: int, operator: int):
        exists = await PDirectoryCrud.pd_is_exists(directory_id)
        if not exists:
            raise CustomException(PD_NOT_EXISTS)
        check = await PDirectoryCrud.verify_permission_in_directory(directory_id, operator)
        if not check:
            raise CustomException(PD_NOT_ALLOW)
        await PDirectoryCrud.delete_dir(directory_id, operator)

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

    @staticmethod
    async def update_project_directory_name(dir_id: int, name: str, operator: int):
        check_directory = await PDirectoryCrud.pd_is_exists(dir_id)
        if not check_directory:
            raise CustomException(PD_NOT_EXISTS)
        check_name = await PDirectoryCrud.pd_name_exists(name=name, directory_id=dir_id)
        if check_name:
            raise CustomException(PD_NAME_EXISTS)
        await PDirectoryCrud.update_project_dir_name(dir_id, name, operator)

    @staticmethod
    async def get_project_members(project_id: int):
        logger.debug(f"查询项目: {project_id}详情")
        members = await ProjectMCrud.query_project_members(project_id)
        return members

    @staticmethod
    async def add_member(project_id: int, member_id: int, role: int, operator: int):
        logger.debug(f"添加项目: {project_id}成员, 成员: {member_id}")
        if not await ProjectCrud.user_has_permission(project_id, operator):
            raise CustomException(PROJECT_NOT_CREATOR)
        if await ProjectMCrud.exists_member(project_id, member_id):
            raise CustomException(PROJECT_MEMBER_EXISTS)
        if role == 3:
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW_ADD_CREATOR)
        await ProjectMCrud.add_member(project_id, member_id, operator, role)

    @staticmethod
    async def remove_member(project_id: int, member_id: int, operator: int):
        logger.debug(f"移除项目: {project_id}成员, 成员: {member_id}")
        if not await ProjectCrud.user_has_permission(project_id, operator):
            raise CustomException(PROJECT_NOT_CREATOR)
        if await ProjectMCrud.member_is_creator(project_id, member_id):
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW_REMOVE_CREATOR)
        if not await ProjectMCrud.exists_member(project_id, member_id):
            raise CustomException(PROJECT_MEMBER_NOT_EXISTS)
        await ProjectMCrud.remove_member(project_id, member_id, operator)

    @staticmethod
    async def update_member(project_id: int, member_id: int, member_role: int, operator: int):
        logger.debug(f"更新项目: {project_id}成员, 成员: {member_id}")
        if not await ProjectCrud.user_has_permission(project_id, operator):
            raise CustomException(PROJECT_NOT_CREATOR)
        if await ProjectMCrud.member_is_creator(project_id, member_id):
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW_UPDATE_CREATOR)
        if not await ProjectMCrud.exists_member(project_id, member_id):
            raise CustomException(PROJECT_MEMBER_NOT_EXISTS)
        if member_role == 3:
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW_TO_CREATOR)
        await ProjectMCrud.update_member(project_id, member_id, member_role, operator)

    @staticmethod
    async def member_exit(project_id: int, operator: int):
        logger.debug(f"退出项目: {project_id}成员, 成员: {operator}")
        if await ProjectMCrud.member_is_creator(project_id, operator):
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW_EXIT_CREATOR)
        if not await ProjectMCrud.exists_member(project_id, operator):
            raise CustomException(PROJECT_MEMBER_NOT_EXISTS)
        await ProjectMCrud.exit_member(project_id, operator)
