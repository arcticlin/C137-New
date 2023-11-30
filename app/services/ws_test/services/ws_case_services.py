# coding=utf-8
"""
File: ws_case_services.py
Author: bot
Created: 2023/11/22
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_490_ws_test import CASE_NOT_EXISTS
from app.services.ws_test.crud.ws_case.ws_case_crud import WsCaseCrud
from app.services.ws_test.schema.ws_case.new import RequestAddWsCase
from app.services.ws_test.schema.ws_case.update import RequestUpdateWsCase


class WsCaseService:
    @staticmethod
    async def query_case_list(ws_id: int):
        result = await WsCaseCrud.query_case_list(ws_id)
        return result

    @staticmethod
    async def query_case_detail(ws_id: int, case_id: int):
        if not await WsCaseCrud.query_case_exists(ws_id, case_id):
            raise CustomException(CASE_NOT_EXISTS)
        result = await WsCaseCrud.query_case_detail(case_id)
        return result

    @staticmethod
    async def add_case_in_ws(form: RequestAddWsCase, create_user: int):
        case_id = await WsCaseCrud.add_case(form, create_user)
        return case_id

    @staticmethod
    async def update_case_detail(ws_id: int, form: RequestUpdateWsCase, operator: int):
        await WsCaseCrud.update_case(ws_id, form, operator)

    @staticmethod
    async def remove_case(ws_id: int, case_id: int, operator: int):
        await WsCaseCrud.remove_case(ws_id, case_id, operator)
