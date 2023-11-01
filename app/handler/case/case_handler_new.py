# coding=utf-8
"""
File: case_handler_new.py
Author: bot
Created: 2023/10/30
Description:
"""
import json
import re
from typing import Union, List

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_480_case import BODY_CAN_NOT_SERIALIZABLE
from app.handler.ahttp.async_http_client import AsyncRequest
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.case.schema.debug_form import RequestDebugForm
from app.services.api_case_new.case.schema.info import OutCaseDetailInfo
from app.services.api_case_new.case_params.headers.schema.info import DebugHeaderInfo, OutHeaderInfo
from app.services.api_case_new.case_params.query.schema.info import DebugParamsInfo, OutParamsInfo
from app.services.common_config.schema.env.responses import EnvDetailOut
from app.utils.time_utils import TimeUtils


# 定义类型别名
ParamInfoList = Union[List[DebugParamsInfo], List[OutParamsInfo]]
HeaderInfoList = Union[List[DebugHeaderInfo], List[OutHeaderInfo]]
CaseDetailInfo = Union[RequestDebugForm, OutCaseDetailInfo]


class CaseHandler:
    def __init__(self, case_form: CaseDetailInfo, env_form: EnvDetailOut, rds: ApiRedis):
        self.rds = rds
        self.case_form = case_form
        self.log = dict(var_replace=[])
        self.env_form = env_form

    @staticmethod
    def replace_path_in_url(url: str, path: dict):
        for key, value in path.items():
            if "{%s}" % key in url and value:
                url = url.replace("{%s}" % key, value)
        return url

    @staticmethod
    def pick_up_url_with_env(env_url: str, case_url: str):
        if not env_url.endswith("/") and not case_url.startswith("/"):
            return env_url + "/" + case_url
        if env_url.endswith("/") and case_url.startswith("/"):
            return env_url[:-1] + "/" + case_url[1:]
        return env_url + case_url

    @staticmethod
    def get_el_exp(src: str):
        """
        提取文本中${}括号内的变量
        """
        re_pattern = re.compile(r"\$\{(.+?)}")
        result = re_pattern.findall(src)
        return result[0] if result else None

    @staticmethod
    def get_el_exp_exclude(src: str) -> bool:
        """
        查询字符串是否存在除了el表达式以外的内容, 用于判断替换成字符串或其他数据类型
        比如传入的是"title_${today_timestamp}" -> "title_1635552000"
        比如传入的是"${today_timestamp}" -> 1635552000
        """
        result = CaseHandler.get_el_exp(src)
        if result:
            if "${%s}" % result == src:
                return False
            return True
        return False

    async def get_var_from_redis(self, key: str):
        """
        从Redis中读取环境变量
        """
        env_obj = await self.rds.get_var_value(key, True)
        case_obj = await self.rds.get_var_value(key, False)

        if case_obj:
            return case_obj
        return env_obj

    async def parse_string(self, key: str):
        log = self.log["var_replace"]
        t = TimeUtils.get_current_time_without_year()
        if isinstance(key, int):
            return key
        if "${" in key:
            log.append(f"[{t}]: [参数替换] -> 获取El表达式变量: {key}")
            find_el = CaseHandler.get_el_exp(key)
            if find_el:
                get_var = await self.get_var_from_redis(find_el)
                if get_var:
                    replace_str_or_obj = CaseHandler.get_el_exp_exclude(key)
                    if replace_str_or_obj:
                        key = key.replace("${%s}" % find_el, str(get_var))
                        log.append(f"[{t}]: [参数替换] -> 替换成功: {key} -> {get_var}, 数据类型为: 字符串")
                        return key
                    log.append(f"[{t}]: [参数替换] -> 替换成功: {key} -> {get_var}, 数据类型为: {type(get_var).__name__}")
                    return get_var
                log.append(f"[{t}]: [参数替换] -> 替换失败: {key} -> {get_var}")
        return key

    async def parse_list_or_obj(self):
        pass

    async def parse_params(self, obj: Union[ParamInfoList, HeaderInfoList]):
        """
        解析query参数
        """
        temp_dict = dict()
        for x in obj:
            if x.enable:
                key = await self.parse_string(x.key)
                value = await self.parse_string(x.value)
                temp_dict[key] = value
        return temp_dict

    async def parse_list(self, key: list):
        temp = []
        for x in key:
            if isinstance(x, dict):
                result = await self.parse_obj(x)

            elif isinstance(x, list):
                result = await self.parse_list(x)

            else:
                result = await self.parse_string(x)
            temp.append(result)
        return temp

    async def parse_obj(self, key: dict):
        temp = {}
        for key, value in key.items():
            key = await self.parse_string(key)
            if isinstance(value, dict):
                result = await self.parse_obj(value)
            elif isinstance(value, list):
                result = await self.parse_list(value)
            elif isinstance(value, str):
                result = await self.parse_string(value)
            else:
                result = value
            temp[key] = result
        return temp

    async def parse_body(self, body: str):
        try:
            body = json.loads(body)
        except Exception:
            raise CustomException(BODY_CAN_NOT_SERIALIZABLE)
        if isinstance(body, dict):
            return await self.parse_obj(body)
        elif isinstance(body, list):
            return await self.parse_list(body)
        else:
            return await self.parse_string(body)

    async def case_pick_up(self):
        url = self.case_form.url_info.url
        method = self.case_form.url_info.method.upper()
        env_headers = await self.parse_params(self.env_form.headers_info)
        headers = await self.parse_params(self.case_form.header_info)
        env_headers.update(headers)
        env_query = await self.parse_params(self.env_form.query_info)
        query = await self.parse_params(self.case_form.query_info)
        env_query.update(query)
        path = await self.parse_params(self.case_form.path_info)
        body_type = self.case_form.body_info.body_type
        body = self.case_form.body_info.body
        if body_type == 0:
            body = ""
        elif body_type == 1:
            body = await self.parse_body(body)
        url = self.replace_path_in_url(url, path)
        # 临时域名,跳过环境域名,比如用于请求阿里云OSS
        if self.case_form.basic_info and self.case_form.basic_info.temp_domain:
            url = self.pick_up_url_with_env(self.case_form.basic_info.temp_domain, url)
        else:
            url = self.pick_up_url_with_env(self.env_form.domain, url)
        await self.rds.set_case_log(self.log)
        return url, method, env_headers, body, body_type, path, env_query

    async def case_executor(self):
        url, method, headers, body, body_type, path, query = await self.case_pick_up()
        r = await AsyncRequest.package_request(
            url=url,
            body_type=body_type,
            body=body,
            params=query,
            headers=headers,
        )
        response = await r.request_to(method)
        return response
