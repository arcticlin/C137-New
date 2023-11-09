# coding=utf-8
"""
File: script_service.py
Author: bot
Created: 2023/10/24
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.services.auth.crud.auth_crud import UserCrud
from app.services.common_config.crud.script.script_crud import ScriptCrud
from app.services.common_config.schema.script.news import (
    RequestScriptAdd,
    RequestScriptDebugByForm,
)
from app.exceptions.exp_470_script import *
from app.services.common_config.schema.script.update import RequestScriptUpdate


class ScriptService:
    @staticmethod
    async def create_script_config(form: RequestScriptAdd, creator: int):
        check = await ScriptCrud.query_script_name_exists(form.name, creator)
        if check:
            raise CustomException(SCRIPT_NAME_EXISTS)
        script_id = await ScriptCrud.create_script_config(form, creator)
        return script_id

    @staticmethod
    async def update_script_config(script_id: int, form: RequestScriptUpdate, operator: int):
        check = await ScriptCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        if form.name:
            check = await ScriptCrud.query_script_name_exists(form.name, operator)
            if check:
                raise CustomException(SCRIPT_NAME_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await ScriptCrud.operator_is_creator(script_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_MODIFY_SCRIPT)
        await ScriptCrud.update_script_config(script_id, form, operator)

    @staticmethod
    async def delete_script_config(script_id: int, operator: int):
        check = await ScriptCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await ScriptCrud.operator_is_creator(script_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_DELETE_SCRIPT)
        await ScriptCrud.delete_script_config(script_id, operator)

    @staticmethod
    async def query_script_list(
        page: int,
        page_size: int,
        operator: int,
        filter_user: int = None,
        filter_public: int = None,
        filter_name: str = None,
    ):
        if filter_public == 0 and filter_user != operator:
            raise CustomException(NO_ALLOW_TO_QUERY_OTHER_PRIVATE)
        result, total = await ScriptCrud.query_script_list(
            page=page,
            page_size=page_size,
            operator=operator,
            filter_user=filter_user,
            filter_public=filter_public,
            filter_name=filter_name,
        )
        return result, total

    @staticmethod
    async def query_script_by_id(script_id: int):
        check = await ScriptCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await ScriptCrud.query_script_detail(script_id)
        return result

    @staticmethod
    async def debug_script_by_form(form: RequestScriptDebugByForm):
        result = await ScriptCrud.execute_by_form(form)
        return result

    @staticmethod
    async def debug_script_by_id(script_id: int, trace_id: str = "default"):
        check = await ScriptCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await ScriptCrud.execute_by_id(script_id, trace_id)
        return result
