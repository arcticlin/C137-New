# coding=utf-8
"""
File: ws_case_services.py
Author: bot
Created: 2023/11/22
Description:
"""
from app.services.ws_test.schema.ws_case.new import RequestAddWsCase
from app.services.ws_test.schema.ws_case.update import RequestUpdateWsCase


class WsCaseService:
    @staticmethod
    async def query_case_list(ws_id: int):
        pass

    @staticmethod
    async def add_case_in_ws(form: RequestAddWsCase, create_user: int):
        pass

    @staticmethod
    async def update_case_detail(ws_id: int, form: RequestUpdateWsCase, operator: int):
        pass

    @staticmethod
    async def remove_case(ws_id: int, case_id: int, operator: int):
        pass
