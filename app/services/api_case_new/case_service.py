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
from app.handler.redis.api_redis_new import ApiRedis

from app.services.api_case_new.case.crud.case_crud import ApiCaseCrud
from app.services.api_case_new.case.schema.debug_form import RequestDebugForm
from app.services.api_case_new.case.schema.new import RequestApiCaseNew
from app.services.api_case_new.settings.suffix.suffix_service import SuffixService
from app.services.common_config.env_service import EnvService
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

    @staticmethod
    async def debug_temp_case(trace_id: str, form: RequestDebugForm, operator: int):
        rds = ApiRedis(trace_id=trace_id, env_id=form.env_id, user_id=operator)
        # 加载环境信息
        env_detail = await EnvService.get_env_detail(form.env_id)
        env_keys = await rds.get_common_env(form.env_id, operator)

        # 初始化环境Redis
        await rds.init_env_keys()

        # 实例化SuffixServer
        s_server = SuffixService(rds)
        # 执行环境前置
        await s_server.execute_env_prefix(env_detail.prefix_info, True)
