# coding=utf-8
"""
File: case_service.py
Author: bot
Created: 2023/10/26
Description:
"""
from typing import List

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_420_project import PD_NOT_EXISTS
from app.exceptions.exp_480_case import *
from app.handler.case.case_handler_new import CaseHandler
from app.handler.redis.api_redis_new import ApiRedis

from app.services.api_case_new.case.crud.case_crud import ApiCaseCrud
from app.services.api_case_new.case.schema.debug_form import RequestDebugForm
from app.services.api_case_new.case.schema.new import RequestApiCaseNew
from app.services.api_case_new.settings.asserts.asserts_service import AssertService
from app.services.api_case_new.settings.extract.extract_service import ExtractService
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
        await rds.init_case_keys()

        # 实例化SuffixServer
        s_server = SuffixService(rds, env_detail)
        # 执行环境前置
        await s_server.execute_env_prefix(env_detail.prefix_info, True)
        # 执行用例前置
        await s_server.execute_case_prefix(form.prefix_info, True)
        # 执行用例
        c_server = CaseHandler(form, env_detail, rds)
        response = await c_server.case_executor()
        # 执行用例后置
        await s_server.execute_case_prefix(form.suffix_info, True)
        # 执行用例断言
        c_assert_server = AssertService(rds)
        case_assert_result = [await c_assert_server.assert_result(response, x) for x in form.assert_info]

        # 执行用例提取

        c_extract_server = ExtractService(rds)
        await c_extract_server.extract(response, form.extract_info)
        # 执行环境断言
        env_assert_result = [
            await c_assert_server.assert_result(response, x, is_env=True) for x in env_detail.assert_info
        ]

        # 返回结果以及断言结果
        final_assert_result = c_assert_server.assert_response_result(env_assert_result, case_assert_result)
        response.final_result = final_assert_result
        return response

    @staticmethod
    async def run_case_by_id(trace_id: str, env_id: int, case_ids: List[int], operator: int):
        env_detail = await EnvService.get_env_detail(env_id)
        env_prefix_running_status = False
        env_suffix_running_status = False
        # 迭代获取测试用例详情
        # fetch_case_detail = await ApiCaseCrud.query_batch_case_detail(case_ids)

        async for c in ApiCaseCrud.query_batch_case_detail(case_ids):
            # TODO 获取详情时异常或执行时异常记录Fail用例
            # 初始化Redis
            rds = ApiRedis(trace_id=trace_id, env_id=env_id, case_id=c.case_id, user_id=operator)

            await rds.init_env_keys()
            await rds.init_case_keys()

            suffix_server = SuffixService(rds, env_detail)
            await suffix_server.execute_env_prefix(env_detail.prefix_info, True, env_prefix_running_status)
            env_prefix_running_status = True

            await suffix_server.execute_case_prefix(c.prefix_info, True)
            c_server = CaseHandler(c, env_detail, rds)
            response = await c_server.case_executor()
            # 执行用例后置
            await suffix_server.execute_case_prefix(c.suffix_info, True)
            # 执行用例断言
            c_assert_server = AssertService(rds)
            case_assert_result = [await c_assert_server.assert_result(response, x) for x in c.assert_info]
            # 执行用例提取

            c_extract_server = ExtractService(rds)
            await c_extract_server.extract(response, c.extract_info)
            # 执行环境断言
            env_assert_result = [
                await c_assert_server.assert_result(response, x, is_env=True) for x in env_detail.assert_info
            ]
            # 返回结果以及断言结果
            final_assert_result = c_assert_server.assert_response_result(env_assert_result, case_assert_result)
            response.final_result = final_assert_result
            return response
