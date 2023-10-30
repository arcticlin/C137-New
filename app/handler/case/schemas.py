# coding=utf-8
"""
File: schemas.py
Author: bot
Created: 2023/10/30
Description:
"""
from pydantic import BaseModel, Field


class AsyncResponseSchema(BaseModel):
    status_code: int = Field(..., title="状态码")
    url: str = Field(..., title="请求地址")
    method: str = Field(..., title="请求方法")
    request_headers: dict = Field({}, title="请求头")
    request_data: dict = Field({}, title="请求体")
    response_headers: dict = Field({}, title="响应头")
    response: dict = Field({}, title="响应体")
    elapsed: str = Field(None, title="响应时间")
    cookies: str = Field(None, title="cookie")
    json_format: bool = Field(False, title="是否格式化json")
