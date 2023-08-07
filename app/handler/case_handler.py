# coding=utf-8
"""
File: case_handler.py
Author: bot
Created: 2023/8/7
Description:
"""
from typing import List

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.exceptions.commom_exception import CustomException
from app.handler.response_handler import C137Response
import json
from app.exceptions.case_exp import *
from app.utils.new_logger import logger


class CaseHandler:
    @staticmethod
    async def get_env_url(env_id: int) -> str:
        """
        获取环境URL
        """
        return await ApiCaseCrud.query_env_info(env_id)

    @staticmethod
    async def get_case_detail(case_id: int):
        """
        获取用例详情
        """
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
        json_body = case_detail["body"] if case_detail.get("body", False) else ""
        if case_detail["body_type"] == 1 and json_body:
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
        if json_body:
            case_detail["body"] = json_body
        return case_detail

    @staticmethod
    async def get_prefix(env_id: int = None, case_id: int = None):
        """
        获取前缀
        """
        pass

    @staticmethod
    async def get_suffix(env_id: int = None, case_id: int = None):
        """
        获取后缀
        """
        pass

    @staticmethod
    async def get_assert():
        """
        获取断言
        """
        pass

    @staticmethod
    async def get_mock_data():
        """
        获取mock数据
        """
        pass

    @staticmethod
    async def get_el_exp():
        """
        获取el表达式
        """
        pass

    @staticmethod
    async def set_out_put():
        """
        设置输出
        """
        pass

    @staticmethod
    def set_url_by_path(url: str, path: List[dict]):
        """
        根据path设置url
        """
        for x in path:
            if "{%s}" % x["key"] in url and x["enable"]:
                url = url.replace("{%s}" % x["key"], x["value"])
        return url

    @staticmethod
    def set_request_params(params: List[dict]):
        """
        设置请求参数
        """
        temp = {}
        for x in params:
            if x["enable"]:
                temp[x["key"]] = x["value"]
        return temp

    @staticmethod
    def set_request_headers(headers: List[dict]):
        """
        设置请求头
        """
        temp = {}
        for x in headers:
            if x["enable"]:
                t_key = x["key"]
                t_value = x["value"]
                t_value_type = x["value_type"]
                if t_value_type == 2:
                    temp[t_key] = int(t_value)
                elif t_value_type == 3:
                    temp[t_key] = True if t_value.upper() == "TRUE" else False
                elif t_value_type == 4:
                    temp[t_key] = json.loads(t_value)
                else:
                    temp[t_key] = t_value
        return temp

    @staticmethod
    async def debug_case_execute(env_id: int, case_id: int):
        """
        调试用例信息
        """
        env_url = await CaseHandler.get_env_url(env_id)
        load_env_prefix = await CaseHandler.get_prefix()
        print("env_url: ", env_url)
        case_detail = await CaseHandler.get_case_detail(case_id)
        case_url = case_detail["url"]
        case_method = case_detail["method"]
        case_headers = CaseHandler.set_request_headers(case_detail["headers"])
        case_params = CaseHandler.set_request_params(case_detail["query"])
        case_url = CaseHandler.set_url_by_path(case_url, case_detail["path"])
        print("case_url: ", case_url)
        print("case_method: ", case_method)
        print("case_headers: ", case_headers)
        print("case_params: ", case_params)
