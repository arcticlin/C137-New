# coding=utf-8
"""
File: ws_code_services.py
Author: bot
Created: 2023/11/22
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_420_project import PROJECT_NOT_EXISTS
from app.exceptions.exp_490_ws_test import *
from app.services.project.crud.project_curd import ProjectCrud
from app.services.ws_test.crud.ws_code.ws_code_crud import WsCodeCrud
from app.services.ws_test.schema.ws_code.new import RequestAddWsCode
from app.services.ws_test.schema.ws_code.update import RequestUpdateWsCode


class WsCodeService:
    @staticmethod
    async def add_code_in_project(form: RequestAddWsCode, create_user: int):
        # 检查项目是否存在
        check = await ProjectCrud.exists_project_id(form.project_id)
        if not check:
            raise CustomException(PROJECT_NOT_EXISTS)
        # 检查Code是否已存在
        code_check = await WsCodeCrud.code_is_exists(form.project_id, form.code_value)
        if code_check:
            raise CustomException(CODE_EXISTS_IN_PROJECT)
        ws_id = await WsCodeCrud.add_ws_code(form, create_user)
        return ws_id

    @staticmethod
    async def query_code_list(project_id: int):
        result = await WsCodeCrud.query_code_list(project_id)
        return result

    @staticmethod
    async def query_code_detail(ws_id: int):
        result = await WsCodeCrud.query_code_detail(ws_id)
        return result

    @staticmethod
    async def update_code_detail(ws_id: int, form: RequestUpdateWsCode, operator: int):
        check = await WsCodeCrud.ws_id_is_exists(ws_id)
        if not check:
            raise CustomException(CODE_NOT_EXISTS)
        await WsCodeCrud.update_ws_code(ws_id, form, operator)

    @staticmethod
    async def remove_code(ws_id: int, operator: int):
        check = await WsCodeCrud.ws_id_is_exists(ws_id)
        if not check:
            raise CustomException(CODE_NOT_EXISTS)
        await WsCodeCrud.delete_ws_code(ws_id, operator)
