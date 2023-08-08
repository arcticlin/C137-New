# coding=utf-8
"""
File: api_case_services.py
Author: bot
Created: 2023/8/2
Description:
"""
import json

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.exceptions.commom_exception import CustomException
from app.exceptions.case_exp import *
from app.handler.response_handler import C137Response
from app.utils.new_logger import logger
from app.schemas.api_case.api_case_schema import AddApiCaseRequest
from app.handler.case_handler import CaseHandler

# from app.services.api_case.suffix_services import SuffixServices
from app.handler.script_handler import ScriptHandler
from app.services.api_case.suffix_services import SuffixServices
from app.handler.redis_handler import redis_client


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
        json_body = case_detail["body"]
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
        return case_detail

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
        # 获取环境信息
        # 获取用例信息
        await SuffixServices(trace_id).execute_env_prefix(env_id)
