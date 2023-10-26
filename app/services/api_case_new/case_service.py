# coding=utf-8
"""
File: case_service.py
Author: bot
Created: 2023/10/26
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_420_project import PD_NOT_EXISTS
from app.exceptions.exp_480_case import *
from app.services.api_case_new.case.crud.case_crud import ApiCaseCrud
from app.services.api_case_new.case.schema.new import RequestApiCaseNew
from app.services.directory.crud.directory_crud import DirectoryCrud


class CaseService:
    @staticmethod
    async def add_api_case(form: RequestApiCaseNew, creator: int):
        exists = await DirectoryCrud.pd_is_exists(form.directory_id)
        if not exists:
            raise CustomException(PD_NOT_EXISTS)
        check = await ApiCaseCrud.query_name_exists_in_directory(
            name=form.basic_info.name,
            method=form.url_info.method.upper(),
            directory_id=form.directory_id,
        )
        if check:
            raise CustomException(CASE_EXISTS)
        case_id = await ApiCaseCrud.add_case(form, creator)
        return case_id

    @staticmethod
    async def delete_api_case(case_id: int, operator: int):
        exists = await ApiCaseCrud.query_case_exists_by_id(case_id)
        if not exists:
            raise CustomException(CASE_NOT_EXISTS)
        await ApiCaseCrud.delete_case(case_id, operator)

    @staticmethod
    async def query_case_detail(case_id: int, operator: int):
        exists = await ApiCaseCrud.query_case_exists_by_id(case_id)
        if not exists:
            raise CustomException(CASE_NOT_EXISTS)

        return await ApiCaseCrud.query_case_detail(case_id)