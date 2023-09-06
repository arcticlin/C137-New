# coding=utf-8
"""
File: api_request_temp.py
Author: bot
Created: 2023/9/5
Description:
"""
from pydantic import BaseModel


class TempBasicRequest(BaseModel):
    name: str
    request_type: int


class TempUrlRequest(BaseModel):
    url: str
    method: str


class TempRequestBody(BaseModel):
    body_type: int
    body: str = None


class TempRequestParam(BaseModel):
    key: str
    value: str
    types: int
    enable: bool


class TempRequestHeader(BaseModel):
    key: str
    value: str
    value_type: int
    enable: bool


class TempRequestSuffix(BaseModel):
    suffix_type: int
    name: str
    enable: bool
    sort: int
    execute_type: int
    script_id: int = None
    sql_id: int = None
    redis_id: int = None
    run_delay: int = None
    run_command: str = None
    run_out_name: str = None


class TempRequestAssert(BaseModel):
    name: str
    enable: bool
    assert_from: int
    assert_with: int
    assert_exp: str = None
    assert_value: str = None


class TempRequestExtract(BaseModel):
    name: str
    enable: bool
    extract_from: int
    extract_type: int
    extract_exp: str = None
    extract_out_name: str = None
    extract_index: int = None


class TempRequestApi(BaseModel):
    env_id: int
    basic_info: TempBasicRequest
    url_info: TempUrlRequest
    body_info: TempRequestBody
    query_info: list[TempRequestParam] = []
    path_info: list[TempRequestParam] = []
    header_info: list[TempRequestHeader] = []
    prefix_info: list[TempRequestSuffix] = []
    suffix_info: list[TempRequestSuffix] = []
    assert_info: list[TempRequestAssert] = []
    extract_info: list[TempRequestExtract] = []
