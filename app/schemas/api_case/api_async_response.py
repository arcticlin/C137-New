# coding=utf-8
"""
File: api_async_response.py
Author: bot
Created: 2023/9/27
Description:
"""
from typing import Optional, Union, List
from pydantic import BaseModel, Field


class ApiAsyncResponse(BaseModel):
    status_code: int
    request_headers: dict = Field({}, description="请求头")
    request_data: Optional[dict] = Field(None, description="请求数据")
    response_headers: dict = Field({}, description="响应数据")
    response: Optional[Union[dict, str]] = Field(None, description="响应数据")
    elapsed: str = Field(None, description="响应时间")
    cookie: str = Field(None, description="cookie")
    json_format: bool = Field(False, description="是否格式化json")
    url: str = Field(..., description="请求地址")
    method: str = Field(..., description="请求方法")
    extract_result: List[dict] = Field([], description="提取结果")
    assert_result: List[dict] = Field([], description="断言结果")
    env_assert: List[dict] = Field([], description="环境断言结果")
    case_assert: List[dict] = Field([], description="用例断言结果")
    final_result: bool = Field(False, description="最终结果")
