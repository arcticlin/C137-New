# -*- coding: UTF-8 -*-
"""
@Project ：backend 
@File    ：async_http_client.py
@Author  ：linpang
@Date    ：2023/1/3 17:14
@Desc    : 
"""

import json, time, aiohttp
from aiohttp import FormData


class AsyncRequest:
    def __init__(self, url: str, timeout=15, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def get_cookie(self, session):
        cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in cookies.items()}

    @staticmethod
    def get_body_from_kwargs(kwargs):
        # 从kwargs里提取body
        if kwargs.get("json") is not None:
            return kwargs.get("json")
        return kwargs.get("data")

    @staticmethod
    async def get_request_data(body):
        if isinstance(body, bytes):
            request_body = body.decode()
        elif isinstance(body, FormData):
            request_body = str(body)
        elif isinstance(body, str):
            request_body = body
        else:
            request_body = body
        # return json.dumps(request_body, ensure_ascii=False)
        return request_body

    @staticmethod
    async def get_response(response):
        """解析响应为json或text"""
        try:
            res = await response.json(encoding="utf-8")
            return res, True
            # return json.dumps(res, ensure_ascii=False), True
        except:
            res = await response.text()
            return res, False

    @staticmethod
    async def package_request(url: str, body_type: int, timeout=15, **kwargs):
        """组装前端的请求, 变为实际请求参数"""
        if not url.startswith(("http://", "https://")):
            raise Exception("请求URL需带上http或https")
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        if body_type == 1:
            if "Content-Type" not in headers or "content-type" not in headers:
                headers["Content-Type"] = "application/json; charset=UTF-8"
            try:
                body = kwargs.get("body")
                if body and isinstance(body, str):
                    body = json.loads(body)
            except Exception as e:
                raise Exception(f"Json格式不正确: {e}")
            _request = AsyncRequest(url=url, headers=headers, params=params, timeout=timeout, json=body)
        else:
            _request = AsyncRequest(
                url=url,
                headers=headers,
                params=params,
                timeout=timeout,
                data=kwargs.get("body"),
            )
        return _request

    @staticmethod
    async def collect_request(
        request_data,
        status_code: int = 200,
        response=None,
        response_headers=None,
        request_headers=None,
        cookie: dict = None,
        elapsed=None,
        **kwargs,
    ):
        """收集请求的数据和响应的结果并返回"""
        if request_headers is None:
            request_headers = {}
        else:
            # request_headers = json.dumps({k: v for k, v in request_headers.items()}, ensure_ascii=False)
            request_headers = {k: v for k, v in request_headers.items()}
        if response_headers is None:
            response_headers = {}
        else:
            # response_headers = json.dumps({k: v for k, v in response_headers.items()}, ensure_ascii=False)
            response_headers = {k: v for k, v in response_headers.items()}
        if cookie is None:
            cookie = {}
        else:
            cookie = json.dumps(cookie, ensure_ascii=False)
        return {
            "status_code": status_code,
            "request_headers": request_headers,
            "request_data": await AsyncRequest.get_request_data(request_data),
            "response_headers": response_headers,
            "response": response,
            "elapsed": elapsed,
            "cookies": cookie,
            **kwargs,
        }

    @staticmethod
    def collect_response_for_test(response: dict):
        status_code = response["status_code"]
        response_header = response["response_headers"]
        response_cookie = response["cookies"]
        response_body = response["response"]
        response_elapsed = int(response["elapsed"].replace("ms", ""))
        return status_code, response_header, response_cookie, response_body, response_elapsed

    async def request_to(self, method: str):
        start = time.time()
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request(method, self.url, timeout=self.timeout, ssl=False, **self.kwargs) as res:
                cost = "%.0fms" % ((time.time() - start) * 1000)
                response, json_format = await AsyncRequest.get_response(res)
                cookie = self.get_cookie(session)
                return await self.collect_request(
                    request_data=AsyncRequest.get_body_from_kwargs(self.kwargs),
                    status_code=res.status,
                    response=response,
                    response_headers=res.headers,
                    request_headers=res.request_info.headers,
                    cookie=cookie,
                    elapsed=cost,
                    json_format=json_format,
                    url=str(res.request_info.url),
                    method=res.request_info.method,
                )
