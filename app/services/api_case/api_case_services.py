# coding=utf-8
"""
File: api_case_services.py
Author: bot
Created: 2023/8/2
Description:
"""
import json
from datetime import datetime

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.crud.api_case.assert_crud import AssertCurd
from app.crud.api_case.suffix_crud import SuffixCrud
from app.exceptions.commom_exception import CustomException
from app.exceptions.case_exp import *
from app.handler.response_handler import C137Response
from app.schemas.api_case.api_request_temp import TempRequestApi
from app.services.api_case.new_assert_services import NewAssertServices
from app.utils.new_logger import logger
from app.schemas.api_case.api_case_schema import AddApiCaseRequest
from app.handler.cases_handler import CaseHandler

# from app.services.api_case.suffix_services import SuffixServices
from app.handler.script_handler import ScriptHandler
from app.services.api_case.suffix_services import SuffixServices
from app.services.api_case.assert_services import AssertServices
from app.handler.redis_handler import redis_client
from app.services.api_case.extract_services import ExtractServices


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
    async def query_case_detail(case_id: int):
        temp = {}
        case_detail, case_path, case_header = await ApiCaseCrud.query_case_detail(case_id)
        if case_detail is None:
            raise CustomException(CASE_NOT_EXISTS)
        case_detail = C137Response.orm_to_dict(case_detail, "deleted_at")
        case_path = C137Response.orm_with_list(
            case_path, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        case_header = C137Response.orm_with_list(
            case_header, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        # 处理Body
        json_body = case_detail["body"] if case_detail.get("body", False) else None
        if case_detail["body_type"] == 1:
            try:
                json_body = json.loads(json_body)
            except Exception as e:
                logger.error(f"无法转化`{json_body}`为json格式, e: {e}")
            finally:
                case_detail["body"] = json_body

        # 处理Path
        path_list = [x for x in case_path if x["types"] == 2]
        params_list = [x for x in case_path if x["types"] == 1]
        header_list = []
        # 处理Headers
        for x in case_header:
            handle_value = x["value"]
            if x["value_type"] == 2:
                handle_value = int(handle_value)
            elif x["value_type"] == 3:
                if handle_value.upper() == "TRUE":
                    handle_value = True
                elif handle_value.upper() == "FALSE":
                    handle_value = False
                elif handle_value.upper() == "1":
                    handle_value = True
                else:
                    handle_value = False
            elif x["value_type"] == 4:
                handle_value = json.loads(handle_value)
            x["value"] = handle_value
            header_list.append(x)
        case_detail["path"] = path_list
        case_detail["query"] = params_list
        case_detail["headers"] = header_list
        prefix_info = await SuffixCrud.get_prefix(case_id=case_id)
        suffix_info = await SuffixCrud.get_suffix(case_id=case_id)
        assert_info = await AssertCurd.query_assert_detail(case_id=case_id)
        temp["case_info"] = case_detail
        temp["prefix_info"] = C137Response.orm_with_list(prefix_info)
        temp["suffix_info"] = C137Response.orm_with_list(suffix_info)
        temp["assert_info"] = C137Response.orm_with_list(assert_info)
        return temp

    @staticmethod
    async def handle_temp_case(data: TempRequestApi):
        temp = {}
        # 用例名称
        t_name = data.basic_info.name
        # TODO: 处理非HTTP请求
        # 请求方法
        t_method, t_url = data.url_info.method, data.url_info.url
        t_query, t_path, t_headers = data.query_info, data.path_info, data.header_info

    @staticmethod
    async def add_case(case_detail: AddApiCaseRequest, creator: int):
        check_case_exists = await ApiCaseCrud.check_case_exists(
            case_detail.directory_id,
            case_detail.name,
            case_detail.method,
        )
        if check_case_exists:
            raise CustomException(CASE_EXISTS)
        case_id = await ApiCaseCrud.add_api_case(case_detail, creator)
        return case_id

    @staticmethod
    async def debug_case_execute(env_id: int, case_id: int, trace_id: str):
        case = CaseHandler(trace_id)

        # 获取环境信息
        env_url = await ApiCaseCrud.query_env_info(env_id)
        # 获取用例信息
        case_detail = await ApiCaseServices.query_case_detail(case_id)

        # 执行环境前置
        await SuffixServices(trace_id).execute_env_prefix(env_id)

        # 执行用例前置
        await SuffixServices(trace_id).execute_case_prefix(case_id)

        # 获取用例信息(替换变量)
        response = await case.case_executor(env_url, case_detail)
        print(response)

        # 执行用例后置
        await SuffixServices(trace_id).execute_case_suffix(case_id)

        # 执行环境后置
        await SuffixServices(trace_id).execute_env_suffix(env_id)

        # 环境断言
        env_result = await AssertServices(trace_id).assert_from_env(env_id, response)

        # 用例断言
        case_result = await AssertServices(trace_id).assert_from_case(case_id, response)

        # 提取参数
        await ExtractServices(trace_id).extract(case_id, response)

        execute_info = await redis_client.get_kv(trace_id)

        # 返回结果
        return {
            "response": response,
            "execute_info": execute_info,
            "env_assert": env_result,
            "case_assert": case_result,
        }

    @staticmethod
    async def temp_request(data: TempRequestApi, trace_id: str):
        case = CaseHandler(trace_id)

        # 获取环境信息
        env_url = await ApiCaseCrud.query_env_info(data.env_id)
        # 执行环境前置
        await SuffixServices(trace_id).execute_env_prefix(data.env_id)

        # 处理临时用例
        # 获取用例信息(替换变量)
        response = await case.case_executor_with_model(env_url, data)
        print(response)

        response["trace_id"] = trace_id

        # 执行环境断言
        env_result = await NewAssertServices(trace_id).assert_from_env(data.env_id, response)
        temp_result = await NewAssertServices(trace_id).assert_from_temp(data.assert_info, response)
        response["assert_result"] = {
            "env_assert": env_result,
            "temp_assert": temp_result,
            "final_result": False not in [e["result"] for e in env_result]
            and False not in [e["result"] for e in temp_result],
        }
        return response
        # 执行环境前置
        # await SuffixServices(trace_id).execute_env_prefix(data.env_id)
