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
from app.crud.api_case.extract_crud import ExtractCrud
from app.crud.api_case.suffix_crud import SuffixCrud
from app.exceptions.commom_exception import CustomException
from app.exceptions.case_exp import *
from app.handler.response_handler import C137Response
from app.schemas.api_case.api_case_schema_new import SchemaRequestAddCase, SchemaRequestDebugCase
from app.schemas.api_case.api_request_temp import TempRequestApi
from app.services.api_case.new_assert_services import NewAssertServices
from app.services.api_case.new_suffix_services import NewSuffixServices
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
    async def query_case_details(case_id: int):
        temp = SchemaRequestDebugCase()
        case_detail, case_path, case_header = await ApiCaseCrud.query_case_detail(case_id)
        if case_detail is None:
            raise CustomException(CASE_NOT_EXISTS)
        temp.case_id = case_id
        temp.directory_id = case_detail.directory_id
        temp.url_info = {"url": case_detail.url, "method": case_detail.method}
        temp.basic_info = {
            "name": case_detail.name,
            "request_type": case_detail.request_type,
            "directory_id": case_detail.directory_id,
            "tag": case_detail.tag,
            "status": case_detail.status,
            "priority": case_detail.priority,
            "case_type": case_detail.case_type,
        }
        temp.body_info = {"body_type": case_detail.body_type, "body": case_detail.body}
        json_body = case_detail.body
        if case_detail.body_type == 1:
            try:
                json_body = json.load(json_body)
            except Exception as e:
                logger.error(f"无法转化`{json_body}`为json格式, e: {e}")
            finally:
                temp.body_info = {"body_type": case_detail.body_type, "body": json_body}
        temp.query_info = [
            {
                "path_id": x.path_id if x.path_id else None,
                "key": x.key,
                "value": x.value,
                "types": x.types,
                "enable": x.enable,
            }
            for x in case_path
            if case_path.types == 2
        ]
        temp.path_info = [
            {
                "path_id": x.path_id if x.path_id else None,
                "key": x.key,
                "value": x.value,
                "types": x.types,
                "enable": x.enable,
            }
            for x in case_path
            if case_path.types == 1
        ]
        header_list = []

        for x in case_header:
            temp_value = x.value
            try:
                if x.types == 1:
                    temp_value = x.value
                if x.value_type == 2:
                    temp_value = int(x.value)
                elif x.value_type == 3:
                    if x.value.upper() == "TRUE":
                        temp_value = True
                    elif x.value.upper() == "FALSE":
                        temp_value = False
                    elif x.value.upper() == "1":
                        temp_value = True
                    else:
                        temp_value = False
                else:
                    temp_value = json.loads(x.value)
            except Exception as e:
                logger.error(f"无法转化`{x.value}`, e: {e}")
                temp_value = x.value
            finally:
                header_list.append(
                    {
                        "header_id": x.header_id if x.header_id else None,
                        "key": x.key,
                        "value": temp_value,
                        "value_type": x.value_type,
                        "enable": x.enable,
                    }
                )

    @staticmethod
    async def query_case_detail_form(case_id: int):
        temp = {}
        case_detail, case_path, case_header = await ApiCaseCrud.query_case_detail(case_id)
        if case_detail is None:
            raise CustomException(CASE_NOT_EXISTS)
        temp["case_id"] = case_id
        temp["directory_id"] = case_detail.directory_id
        temp["url_info"] = {"url": case_detail.url, "method": case_detail.method}
        temp["basic_info"] = {
            "name": case_detail.name,
            "request_type": case_detail.request_type,
            "directory_id": case_detail.directory_id,
            "tag": case_detail.tag,
            "status": case_detail.status,
            "priority": case_detail.priority,
            "case_type": case_detail.case_type,
        }
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
                temp["body_info"] = {"body_type": case_detail["body_type"], "body": json_body}
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
        temp["path_info"] = path_list
        temp["query_info"] = params_list
        temp["header_info"] = header_list
        prefix_info = await SuffixCrud.get_prefix(case_id=case_id)
        suffix_info = await SuffixCrud.get_suffix(case_id=case_id)
        assert_info = await AssertCurd.query_assert_detail(case_id=case_id)
        extract_info = await ExtractCrud.query_case_extract(case_id=case_id)
        # temp["case_info"] = case_detail
        temp["prefix_info"] = C137Response.orm_with_list(
            prefix_info, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        temp["suffix_info"] = C137Response.orm_with_list(
            suffix_info, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        temp["assert_info"] = C137Response.orm_with_list(
            assert_info, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        temp["extract_info"] = C137Response.orm_with_list(
            extract_info, "deleted_at", "case_id", "create_user", "update_user", "created_at", "updated_at"
        )
        return temp

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
    async def temp_request(data: SchemaRequestDebugCase, operator: int):
        case = CaseHandler(f"e:e_{data.env_id}_{operator}")
        suffix = NewSuffixServices(data.env_id, operator, None)

        # 获取环境信息
        env_url = await ApiCaseCrud.query_env_info(data.env_id)
        # 执行环境前置
        await suffix.execute_env_prefix(is_prefix=True)
        # 执行用例前置
        await suffix.execute_case_prefix(is_prefix=True, temp_prefix=data.prefix_info)

        # 获取用例信息(替换变量)
        response = await case.case_executor_with_model(env_url, data)
        # print(response)
        #
        # response["trace_id"] = trace_id
        #
        # # 执行环境断言
        # env_result = await NewAssertServices(trace_id).assert_from_env(data.env_id, response)
        # # 执行用例断言
        # temp_result = await NewAssertServices(trace_id).assert_from_temp(data.assert_info, response)
        #
        # # 如果不存在环境断言和用例断言的情况下, 判断状态码和内置Code
        # temp_final_result = True
        # if not env_result and not temp_result:
        #     if response["status_code"] != 200:
        #         temp_final_result = False
        #     if response["json_format"]:
        #         if response["response"].__contains__("code"):
        #             if response["response"]["code"] != 0:
        #                 temp_final_result = False
        # response["assert_result"] = {
        #     "env_assert": env_result,
        #     "temp_assert": temp_result,
        #     "final_result": False not in [e["result"] for e in env_result]
        #     and False not in [e["result"] for e in temp_result]
        #     and temp_final_result,
        # }
        # # 提取参数
        # extract_result = await ExtractServices(trace_id).extract(response, temp_extract=data.extract_info)
        # response["extract_result"] = extract_result
        #
        # return response
        # 执行环境前置
        # await SuffixServices(trace_id).execute_env_prefix(data.env_id)

    @staticmethod
    async def add_case_form(form: SchemaRequestAddCase, creator: int):
        repeat = await ApiCaseCrud.check_case_exists(form.directory_id, form.basic_info.name, form.url_info.method)
        if repeat:
            raise CustomException(CASE_EXISTS)
        case_id = await ApiCaseCrud.add_case_form(form, creator)
        return case_id
