# coding=utf-8
"""
File: api_case_services.py
Author: bot
Created: 2023/8/2
Description:
"""
import time
from typing import List

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.crud.api_case.assert_crud import AssertCurd
from app.crud.api_case.extract_crud import ExtractCrud
from app.crud.api_case.suffix_crud import SuffixCrud
from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_480_case import *
from app.handler.redis.api_redis import ApiRedis


from app.handler.serializer.response_serializer import C137Response
from app.schemas.api_case.api_case_schema_new_new import CaseFullAdd, CaseFullUpdate
from app.schemas.api_case.api_case_schemas import (
    OrmFullCase,
    Orm2CaseBaseInfo,
    Orm2CaseUrl,
    Orm2CaseBody,
    Orm2CaseParams,
    Orm2CaseHeader,
    Orm2CaseSuffix,
    Orm2CaseAssert,
    Orm2CaseExtract,
)

from app.services.api_case.assert_service import AssertService
from app.services.api_case.extract_service import ExtractService
from app.handler.case.case_handler import CaseHandler
from app.services.api_case.new_suffix_service import SuffixService
from app.crud.api_case.api_report_crud import ApiResultCrud, ApiReportCrud


class ApiCaseServices:
    @staticmethod
    async def delete_case(case_id: int, operator: int):
        check = await ApiCaseCrud.get_case_dependencies(case_id)
        if check is None:
            raise CustomException(CASE_NOT_EXISTS)
        case_id, path_id, headers_id = check
        if path_id:
            path_id = [path_id] if "," not in path_id else path_id.split(",")
        if headers_id:
            headers_id = [headers_id] if "," not in headers_id else headers_id.split(",")
        await ApiCaseCrud.delete_api_case(case_id=case_id, operator=operator, path_id=path_id, headers_id=headers_id)

    @staticmethod
    async def query_case_details(case_id: int) -> OrmFullCase:
        temp = OrmFullCase()
        case_detail, case_path, case_header = await ApiCaseCrud.query_case_detail(case_id)
        prefix_info, suffix_info = await SuffixCrud.get_prefix(case_id=case_id), await SuffixCrud.get_suffix(
            case_id=case_id
        )
        assert_info = await AssertCurd.query_assert_detail(case_id=case_id)
        extract_info = await ExtractCrud.query_case_extract(case_id=case_id)

        if case_detail is None:
            raise CustomException(CASE_NOT_EXISTS)
        temp.case_id = case_id
        temp.directory_id = case_detail.directory_id
        # temp.basic_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBaseInfo).dict()
        # temp.url_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseUrl).dict()
        # temp.body_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBody).dict()
        # temp.query_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams).dict() for x in case_path if x.types == 1]
        # temp.path_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams).dict() for x in case_path if x.types == 2]
        # temp.header_info = [C137Response.orm_to_pydantic(x, Orm2CaseHeader).dict() for x in case_header]
        # temp.prefix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix).dict() for x in prefix_info]
        # temp.suffix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix).dict() for x in suffix_info]
        # temp.assert_info = [C137Response.orm_to_pydantic(x, Orm2CaseAssert).dict() for x in assert_info]
        # temp.extract_info = [C137Response.orm_to_pydantic(x, Orm2CaseExtract).dict() for x in extract_info]
        temp.basic_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBaseInfo)
        temp.url_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseUrl)
        temp.body_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBody)
        temp.query_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams) for x in case_path if x.types == 2]
        temp.path_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams) for x in case_path if x.types == 1]
        temp.header_info = [C137Response.orm_to_pydantic(x, Orm2CaseHeader) for x in case_header]
        temp.prefix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix) for x in prefix_info]
        temp.suffix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix) for x in suffix_info]
        temp.assert_info = [C137Response.orm_to_pydantic(x, Orm2CaseAssert) for x in assert_info]
        temp.extract_info = [C137Response.orm_to_pydantic(x, Orm2CaseExtract) for x in extract_info]
        return temp

    @staticmethod
    def diff_form(update_form: dict, src_form: dict):
        diff_ = {}
        for key, value in update_form.items():
            if value == src_form[key]:
                continue
            else:
                diff_[key] = value
        return diff_

    @staticmethod
    # async def temp_request(data: OrmFullCase, operator: int):
    #     case = CaseHandler(env_id=data.env_id, case_id=data.case_id, user_id=operator)
    #     await redis_client.init_case_log_body(operator, data.case_id)
    #     suffix = NewSuffixServices(data.env_id, operator, None)
    #
    #     # 获取环境信息
    #     env_url = await ApiCaseCrud.query_env_info(data.env_id)
    #     # 执行环境前置
    #     await suffix.execute_env_prefix(is_prefix=True)
    #     # 执行用例前置
    #     await suffix.execute_case_prefix(is_prefix=True, temp_prefix=data.prefix_info)
    #
    #     # 执行用例信息(替换变量)
    #     response = await case.case_executor(env_url, data)
    #
    #     response["trace_id"] = f"c:c_temp_{operator}"
    #
    #     # 执行用例后置
    #     await suffix.execute_case_prefix(is_prefix=False, temp_prefix=data.suffix_info)
    #     # 实例化断言模块
    #     asserts = AssertService(env_id=data.env_id, user_id=operator, async_response=response, case_id=data.case_id)
    #     # 执行环境断言
    #     env_result = await asserts.assert_from_env()
    #     # 执行用例断言
    #     case_result = await asserts.assert_from_case(data=data.assert_info)
    #     _flag = asserts.assert_response_result(env_result, case_result)
    #     if len(env_result) == 0 and len(case_result) == 0:
    #         if response["status_code"] != 200:
    #             _flag = [False]
    #         if response["json_format"]:
    #             if response["response"].__contains__("code"):
    #                 if response["response"]["code"] != 0:
    #                     _flag = [False]
    #     response["assert_result"] = {
    #         "env_assert": env_result,
    #         "case_assert": case_result,
    #         "final_result": False not in _flag,
    #     }
    #     # 执行提取参数
    #     extract = ExtractService(env_id=data.env_id, user_id=operator, async_response=response, case_id=data.case_id)
    #     extract_result = await extract.extract(extract_data=data.extract_info)
    #     response["extract_result"] = extract_result
    #     response["log"] = await redis_client.get_case_log(operator, data.case_id)
    #     return response

    @staticmethod
    async def case_request(case_id: int, operator: int):
        pass

    @staticmethod
    async def add_case(form: CaseFullAdd, creator: int):
        repeat = await ApiCaseCrud.check_case_exists(form.directory_id, form.basic_info.name, form.url_info.method)
        if repeat:
            raise CustomException(CASE_EXISTS)
        case_id = await ApiCaseCrud.add_case_form(form, creator)
        return case_id

    @staticmethod
    async def update_case(form: CaseFullUpdate, operator: int):
        source_case = await ApiCaseServices.query_case_details(form.case_id)
        diff_ = ApiCaseServices.diff_form(form.dict(), source_case.dict())
        print(diff_)

    @staticmethod
    async def run_single_case(trace_id: str, env_id: int, case_id: int):
        rds = ApiRedis(trace_id)
        await rds.init_env_key(env_id)
        # 1. 检查环境获取是否存在异常
        env_url = await ApiCaseCrud.query_env_info(env_id)

        # 2. 检查用例获取是否存在异常
        case_info = await ApiCaseServices.query_case_details(case_id)
        # 3. 初始化Redis连接 + Case模块 + Suffix模块 + Assert模块

        suffix = SuffixService(env_id, trace_id, case_id, is_temp=False)
        case = CaseHandler(env_id=env_id, case_id=case_id, trace_id=trace_id)

        # 4. 初始化环境Redis, e:e_{env_id}_{trace_id} = {var: {}, log: {}}

        # 5. 初始化用例Redis, c:c_{case_id}_{trace_id} = {var: {}, log: {}}
        await rds.init_case_key(case_id)
        # 6. 初始化前后置模块
        # 5. 执行环境前置,并将日志和提取的参数存入环境Redis
        await suffix.execute_env_prefix(is_prefix=True)
        # 6. 执行用例前置,并将日志和提取的参数存入用例Redis
        await suffix.execute_case_prefix(is_prefix=True)
        # 7. 执行用例,并将日志和提取的参数存入用例Redis
        response = await case.case_executor(env_url, case_info)
        # 8. 执行用例后置,并将日志和提取的参数存入用例Redis
        await suffix.execute_case_prefix(is_prefix=False)
        # 9. 执行环境后置,并将日志和提取的参数存入环境Redis
        await suffix.execute_env_prefix(is_prefix=False)
        # 10. 执行断言,并将断言结果存入用例Redis
        assert_ = AssertService(env_id=env_id, trace_id=trace_id, case_id=case_id, async_response=response)
        extract_ = ExtractService(env_id=env_id, trace_id=trace_id, case_id=case_id, async_response=response)
        await assert_.assert_from_case(case_info.assert_info)
        await assert_.assert_from_env()
        # 11. 执行提取参数,并将提取结果存入用例Redis
        await extract_.extract(case_info.extract_info)
        # return response
        print(response)
        return {}

    @staticmethod
    async def run_case_suite(trace_id: str, env_id: int, case_id: List[int]):
        rds = ApiRedis(trace_id)
        await rds.init_env_key(env_id)
        # 1. 检查环境获取是否存在异常
        env_url = await ApiCaseCrud.query_env_info(env_id)
        total = len(case_id)
        report_id = await ApiReportCrud.init_api_report(trace_id, total)
        count_result = {"success": 0, "failed": 0, "xfail": 0, "skip": 0, "duration": 0}
        start_time = time.time()
        for e_id in case_id:
            response = {}
            try:
                # 2. 检查用例获取是否存在异常
                case_info = await ApiCaseServices.query_case_details(e_id)
                # 3. 初始化Redis连接 + Case模块 + Suffix模块 + Assert模块

                suffix = SuffixService(env_id, trace_id, e_id, is_temp=False)
                case = CaseHandler(env_id=env_id, case_id=e_id, trace_id=trace_id)

                # 4. 初始化环境Redis, e:e_{env_id}_{trace_id} = {var: {}, log: {}}

                # 5. 初始化用例Redis, c:c_{case_id}_{trace_id} = {var: {}, log: {}}
                await rds.init_case_key(e_id)
                # 6. 初始化前后置模块
                # 5. 执行环境前置,并将日志和提取的参数存入环境Redis
                await suffix.execute_env_prefix(is_prefix=True)
                # 6. 执行用例前置,并将日志和提取的参数存入用例Redis
                await suffix.execute_case_prefix(is_prefix=True)
                # 7. 执行用例,并将日志和提取的参数存入用例Redis
                response = await case.case_executor(env_url, case_info)
                # 8. 执行用例后置,并将日志和提取的参数存入用例Redis
                await suffix.execute_case_prefix(is_prefix=False)
                # 9. 执行环境后置,并将日志和提取的参数存入环境Redis
                await suffix.execute_env_prefix(is_prefix=False)
                # 10. 执行断言,并将断言结果存入用例Redis
                assert_ = AssertService(env_id=env_id, trace_id=trace_id, case_id=e_id, async_response=response)
                extract_ = ExtractService(env_id=env_id, trace_id=trace_id, case_id=e_id, async_response=response)
                case_result = await assert_.assert_from_case(case_info.assert_info)
                env_result = await assert_.assert_from_env()
                # 11. 执行提取参数,并将提取结果存入用例Redis
                _flag = assert_.assert_response_result(env_result, case_result)
                extract_result = await extract_.extract(case_info.extract_info)
                response["extract_result"] = extract_result
                response["assert_result"] = {
                    "env_assert": env_result,
                    "case_assert": case_result,
                    "final_result": False not in _flag,
                }
                if False not in _flag:
                    count_result["success"] += 1
                else:
                    count_result["failed"] += 1
            except Exception as e:
                count_result["failed"] += 1
            finally:
                await ApiResultCrud.insert_api_result(trace_id, e_id, response)

        end_time = time.time()
        count_result["duration"] = round(end_time - start_time, 1)
        await ApiReportCrud.update_api_report(report_id, count_result)
