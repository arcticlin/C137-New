# coding=utf-8
"""
File: directory_service.py
Author: bot
Created: 2023/10/20
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.services.directory.crud.directory_crud import DirectoryCrud
from app.services.directory.schema.dir_new import DirectoryNew
from app.exceptions.project_exp_420 import *
from loguru import logger


class DirectoryService:
    @staticmethod
    async def get_project_directory_tree(project_id: int):
        result = await DirectoryCrud.n_get_project_directory_tree(project_id)
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

        return DirectoryCrud.another_build_directory_tree(temp_data)

    @staticmethod
    async def add_project_dir(data: DirectoryNew, creator: int):
        # 检查目录名是否重复
        exists = await DirectoryCrud.pd_name_exists(data.name, project_id=data.project_id)
        if exists:
            raise CustomException(PD_NAME_EXISTS)
        return await DirectoryCrud.add_project_dir(data, creator)

    @staticmethod
    async def delete_directory_new(directory_id: int, operator: int):
        exists = await DirectoryCrud.pd_is_exists(directory_id)
        if not exists:
            raise CustomException(PD_NOT_EXISTS)
        check = await DirectoryCrud.verify_permission_in_directory(directory_id, operator)
        if not check:
            raise CustomException(PD_NOT_ALLOW)
        await DirectoryCrud.delete_dir(directory_id, operator)

    @staticmethod
    async def update_project_dir_name(project_id: int, directory_id: int, name: str, operator: int):
        logger.debug(f"{operator} => 更新项目: {project_id} 目录信息")
        check = await DirectoryCrud.check_directory_permission(project_id, directory_id)
        if check is None:
            raise CustomException(PD_NOT_EXISTS)
        check_d, check_u = check
        if operator not in DatabaseBulk.serializer_comma_string(check_u):
            raise CustomException(PD_NOT_ALLOW)
        await DirectoryCrud.update_project_dir_name(directory_id, name, operator)

    @staticmethod
    async def get_case_list_in_directory(directory_id: int):
        result = await DirectoryCrud.get_case_list_in_directory(directory_id)
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
