# coding=utf-8
"""
File: case_handler.py
Author: bot
Created: 2023/8/8
Description:
"""
import json
from typing import List, Union
import re

from app.handler.redis.api_redis import ApiRedis
from app.schemas.api_case.api_case_schemas import OrmFullCase
from app.handler.ahttp.async_http_client import AsyncRequest
from app.utils.time_utils import TimeUtils


class CaseHandler:
    def __init__(self, env_id: int, trace_id: str, user_id: int = None, case_id: int = None):
        self.env_id = env_id
        self.user_id = user_id
        self.case_id = "temp" if case_id is None else case_id
        self.trace_id = trace_id
        self.log = dict(var_replace=[])
        self.rds = ApiRedis(trace_id)

    @staticmethod
    def set_url_by_path(url: str, path: List[dict]):
        """
        根据path设置URL
        """
        # for x in path:
        #     if "{%s}" % x["key"] in url and x["enable"]:
        #         url = url.replace("{%s}" % x["key"], x["value"])
        for x in path:
            for key, value in x.items():
                if "{%s}" % key in url and value:
                    url = url.replace("{%s}" % key, value)
        return url

    @staticmethod
    def set_url_with_env(env_url: str, url: str):
        if not env_url.endswith("/") and not url.startswith("/"):
            return env_url + "/" + url
        return env_url + url

    @staticmethod
    def get_el_exp(src: str):
        """
        获取el表达式
        """
        re_pattern = re.compile(r"\$\{(.+?)\}")
        result = re_pattern.findall(src)
        return result[0] if result else None

    @staticmethod
    def get_el_exp_exclude(src: str) -> bool:
        """
        查询字符串是否存在除了el表达式以外的内容
        """
        re_pattern = re.compile(r"\$\{(.+?)\}")
        result = re_pattern.findall(src)
        if result:
            if "${%s}" % result[0] == src:
                return False
            return True
        return False

    async def get_var_from_redis(self, key: str):
        """
        获取变量
        """
        # 先从环境提取,再从用例提取

        env_obj = await self.rds.get_var_value(key, self.env_id, self.case_id, True)
        case_obj = await self.rds.get_var_value(key, self.env_id, self.case_id, False)

        if case_obj:
            return case_obj
        return env_obj

    async def parse_text(self, key: str):
        t = TimeUtils.get_current_time_without_year()
        if isinstance(key, str) and "${" in key:
            self.log["var_replace"].append(f"[{t}]: [参数替换] -> 获取El表达式变量: {key}")
            find_el = CaseHandler.get_el_exp(key)
            if find_el:
                result = await self.get_var_from_redis(find_el)
                if result:
                    self.log["var_replace"].append(f"[{t}]: [参数替换] -> 替换成功: {key} -> {result}")
                    replace_str_or_obj = CaseHandler.get_el_exp_exclude(key)
                    if replace_str_or_obj:
                        key = key.replace("${%s}" % find_el, str(result))
                        return key
                    return result
                self.log["var_replace"].append(f"[{t}]: [参数替换] -> 替换失败: {key} -> {result}")
        return key

    async def parse_list(self, key: list):
        temp = []
        for x in key:
            if isinstance(x, dict):
                result = await self.parse_obj(x)
                temp.append(result)
            elif isinstance(x, list):
                result = await self.parse_list(x)
                temp.append(result)
            else:
                result = await self.parse_text(x)
                temp.append(result)
        return temp

    async def parse_obj(self, obj: Union[dict, str]):
        temp = {}
        if isinstance(obj, str):
            try:
                obj = json.loads(obj)
            except Exception:
                obj = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                temp[key] = await self.parse_obj(value)
            elif isinstance(value, list):
                temp[key] = await self.parse_list(value)
            else:
                temp[key] = await self.parse_text(value)

        return temp

    async def parse_path(self, obj: list) -> List:
        temp_list = []
        for item in obj:
            if item["enable"]:
                temp_list.append({item["key"]: await self.parse_text(item["value"])})
        return temp_list

    async def parse_query(self, obj: list) -> dict:
        temp_dict = {}
        for item in obj:
            if item["enable"]:
                temp_dict[item["key"]] = await self.parse_text(item["value"])
        return temp_dict

    async def case_pick_up(self, env_url: str, obj: OrmFullCase):
        print("11", obj)
        print("22", obj.url_info)
        print("33", type(obj.url_info))
        url = obj.url_info.url
        method = obj.url_info.method
        headers = await self.parse_query([x.dict() for x in obj.header_info])
        query = await self.parse_query([x.dict() for x in obj.query_info])
        path = await self.parse_path([x.dict() for x in obj.path_info])
        body_type = obj.body_info.body_type
        body = await self.parse_obj(obj.body_info.body) if body_type != 0 else ""
        url = self.set_url_with_env(env_url, url)
        url = self.set_url_by_path(url, path)
        return url, method, headers, body, body_type, path, query

    async def case_executor(self, env_url: str, data: OrmFullCase):
        url, method, headers, body, body_type, path, query = await self.case_pick_up(env_url, data)
        await self.rds.set_case_log(data.case_id, self.log)
        r = await AsyncRequest.package_request(
            url=url,
            body_type=body_type,
            body=body,
            params=query,
            headers=headers,
        )
        response = await r.request_to(method)
        return response
