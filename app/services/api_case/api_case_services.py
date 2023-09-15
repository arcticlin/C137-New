# coding=utf-8
"""
File: api_case_services.py
Author: bot
Created: 2023/8/2
Description:
"""
from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.crud.api_case.assert_crud import AssertCurd
from app.crud.api_case.extract_crud import ExtractCrud
from app.crud.api_case.suffix_crud import SuffixCrud
from app.exceptions.commom_exception import CustomException
from app.exceptions.case_exp import *
from app.handler.new_redis_handler import redis_client
from app.handler.response_handler import C137Response
from app.schemas.api_case.api_case_schema_new import SchemaRequestAddCase
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
from app.services.api_case.suffix_services import NewSuffixServices
from app.handler.cases_handler import CaseHandler


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
    async def query_case_details(case_id: int):
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
        temp.basic_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBaseInfo).dict()
        temp.url_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseUrl).dict()
        temp.body_info = C137Response.orm_to_pydantic(case_detail, Orm2CaseBody).dict()
        temp.query_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams).dict() for x in case_path if x.types == 1]
        temp.path_info = [C137Response.orm_to_pydantic(x, Orm2CaseParams).dict() for x in case_path if x.types == 2]
        temp.header_info = [C137Response.orm_to_pydantic(x, Orm2CaseHeader).dict() for x in case_header]
        temp.prefix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix).dict() for x in prefix_info]
        temp.suffix_info = [C137Response.orm_to_pydantic(x, Orm2CaseSuffix).dict() for x in suffix_info]
        temp.assert_info = [C137Response.orm_to_pydantic(x, Orm2CaseAssert).dict() for x in assert_info]
        temp.extract_info = [C137Response.orm_to_pydantic(x, Orm2CaseExtract).dict() for x in extract_info]

        return temp

    @staticmethod
    async def temp_request(data: OrmFullCase, operator: int):
        case = CaseHandler(env_id=data.env_id, case_id=data.case_id, user_id=operator)
        await redis_client.init_case_log_body(operator, data.case_id)
        suffix = NewSuffixServices(data.env_id, operator, None)

        # 获取环境信息
        env_url = await ApiCaseCrud.query_env_info(data.env_id)
        # 执行环境前置
        await suffix.execute_env_prefix(is_prefix=True)
        # 执行用例前置
        await suffix.execute_case_prefix(is_prefix=True, temp_prefix=data.prefix_info)

        # 执行用例信息(替换变量)
        response = await case.case_executor(env_url, data)

        response["trace_id"] = f"c:c_temp_{operator}"

        # 执行用例后置
        await suffix.execute_case_prefix(is_prefix=False, temp_prefix=data.suffix_info)
        # 实例化断言模块
        asserts = AssertService(env_id=data.env_id, user_id=operator, async_response=response, case_id=data.case_id)
        # 执行环境断言
        env_result = await asserts.assert_from_env()
        # 执行用例断言
        case_result = await asserts.assert_from_case(data=data.assert_info)
        _flag = asserts.assert_response_result(env_result, case_result)
        if len(env_result) == 0 and len(case_result) == 0:
            if response["status_code"] != 200:
                _flag = [False]
            if response["json_format"]:
                if response["response"].__contains__("code"):
                    if response["response"]["code"] != 0:
                        _flag = [False]
        response["assert_result"] = {
            "env_assert": env_result,
            "case_assert": case_result,
            "final_result": False not in _flag,
        }
        # 执行提取参数
        extract = ExtractService(env_id=data.env_id, user_id=operator, async_response=response, case_id=data.case_id)
        extract_result = await extract.extract(extract_data=data.extract_info)
        response["extract_result"] = extract_result
        response["log"] = await redis_client.get_case_log(operator, data.case_id)
        return response

    @staticmethod
    async def add_case_form(form: SchemaRequestAddCase, creator: int):
        repeat = await ApiCaseCrud.check_case_exists(form.directory_id, form.basic_info.name, form.url_info.method)
        if repeat:
            raise CustomException(CASE_EXISTS)
        case_id = await ApiCaseCrud.add_case_form(form, creator)
        return case_id
