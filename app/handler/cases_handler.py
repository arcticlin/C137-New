# coding=utf-8
"""
File: cases_handler.py
Author: bot
Created: 2023/8/8
Description:
"""
import json
from typing import List
import re

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.handler.redis_handler import redis_client
from app.utils.case_log import CaseLog
from app.handler.async_http_client import AsyncRequest


class CaseHandler:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.log = CaseLog()

    @staticmethod
    def set_url_by_path(url: str, path: List[dict]):
        """
        根据path设置URL
        """
        for x in path:
            if "{%s}" % x["key"] in url and x["enable"]:
                url = url.replace("{%s}" % x["key"], x["value"])
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
        obj = await redis_client.get_kv(self.trace_id)

        if obj is None:
            return None
        result = obj.get("vars", {}).get(key, None)
        return result

    async def parse_text(self, key: str):
        if isinstance(key, str) and "${" in key:
            self.log.vars_append(f"尝试替换变量: {key}")
            find_el = CaseHandler.get_el_exp(key)
            if find_el:
                result = await self.get_var_from_redis(find_el)
                if result:
                    self.log.vars_append(f"替换变量成功: {key} -> {result}")
                    replace_str_or_obj = CaseHandler.get_el_exp_exclude(key)
                    if replace_str_or_obj:
                        key = key.replace("${%s}" % find_el, str(result))
                        return key
                    return result
                self.log.vars_append(f"替换变量失败: {key} -> {result}")
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

    async def parse_obj(self, obj: dict):
        temp = {}
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

    async def case_pick_up(self, env_url: str, obj: dict):
        """
        拼接用例
        """
        url = obj["url"]
        method = obj["method"]
        headers = await self.parse_query(obj["headers"])
        body = {}
        body_type = obj["body_type"]
        if body_type == 1:
            body = obj["body"]
        path: list = await self.parse_path(obj["path"])
        query: dict = await self.parse_query(obj["query"])
        body: dict = await self.parse_obj(body) if body else {}
        url = self.set_url_with_env(env_url, url)
        return url, method, headers, body, body_type, path, query

    async def case_executor(self, env_url: str, obj: dict):
        """
        执行用例
        """
        url, method, headers, body, body_type, path, query = await self.case_pick_up(env_url, obj)
        await redis_client.set_case_log_load(self.trace_id, self.log.logs, "case_vars")
        r = await AsyncRequest.package_request(
            url=url,
            body_type=body_type,
            body=body,
            params=query,
            headers=headers,
        )
        response = await r.request_to(method)
        return response
