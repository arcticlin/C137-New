# coding=utf-8
"""
File: new_project_service.py
Author: bot
Created: 2023/10/18
Description:
"""

from app.exceptions.custom_exception import CustomException
from app.services.project.crud.pm_crud import ProjectMCrud
from app.services.project.crud.project_curd import ProjectCrud
from app.exceptions.project_exp_420 import *
from loguru import logger

from app.services.project.schema.project_member import ProjectAddMemberRequest
from app.services.project.schema.project_new import ProjectNewRequest
from app.services.project.schema.project_update import ProjectUpdateRequest
from app.services.ws.ws_service import WsService


class ProjectService:
    @staticmethod
    async def add_project(data: ProjectNewRequest, operator: int) -> int:
        """创建项目"""
        project_id = await ProjectCrud.add_project(data, operator)
        # 通知更新
        await WsService.ws_notify_update_project_list([operator])
        return project_id

    @staticmethod
    async def delete_project(project_id: int, operator: int) -> None:
        """删除项目"""
        logger.debug(f"{operator} => 删除项目: {project_id}")
        exists = await ProjectCrud.exists_project_id(project_id)
        has_permission = await ProjectCrud.user_has_permission(project_id, operator)
        if not exists:
            raise CustomException(PROJECT_NOT_EXISTS)
        if not has_permission:
            raise CustomException(PROJECT_NOT_CREATOR)
        # 通知更新
        pm_list = await ProjectMCrud.query_pm_with_id(project_id)
        await ProjectCrud.delete_project(project_id, operator)
        await WsService.ws_notify_update_project_list(pm_list)
        await WsService.ws_notify_message(pm_list, f"项目: {project_id}已被解散")

    @staticmethod
    async def update_project(project_id: int, data: ProjectUpdateRequest, operator: int) -> None:
        """更新项目"""
        logger.debug(f"{operator} => 更新项目: {project_id}")
        exists = await ProjectCrud.exists_project_id(project_id)
        has_permission = await ProjectCrud.user_has_permission(project_id, operator)
        name_exists = await ProjectCrud.exists_project_name(data.project_name, operator)
        if not exists:
            raise CustomException(PROJECT_NOT_EXISTS)
        if not has_permission:
            raise CustomException(PROJECT_NOT_CREATOR)
        if name_exists:
            raise CustomException(PROJECT_NAME_EXISTS)
        # 通知更新
        pm_list = await ProjectMCrud.query_pm_with_id(project_id)
        await ProjectCrud.update_project(project_id, data, operator)
        await WsService.ws_notify_update_project_list(pm_list)

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
                today_case,
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
                    "total_case": case_count,
                    "new_case_today": today_case,
                    "members": member_count,
                }
            )
        return temp

    @staticmethod
    async def get_project_detail(project_id: int, user_id: int):
        logger.debug(f"查询项目: {project_id}详情")
        if not await ProjectMCrud.exists_member(project_id, user_id):
            raise CustomException(PROJECT_MEMBER_NOT_ALLOW)
        project_info = await ProjectCrud.query_project(project_id)
        return project_info

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
        await WsService.ws_notify_update_project_list([member_id])
        await WsService.ws_notify_message([member_id], f"你被添加到项目: {project_id}")

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
        await WsService.ws_notify_update_project_list([member_id])
        await WsService.ws_notify_message([member_id], f"你被移除项目: {project_id}")

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
        # 通知更新
        pm_list = await ProjectMCrud.query_pm_with_id(project_id)
        await WsService.ws_notify_update_project_list(pm_list)
