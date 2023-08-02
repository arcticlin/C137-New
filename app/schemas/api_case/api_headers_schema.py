# coding=utf-8
"""
File: api_headers_schema.py
Author: bot
Created: 2023/8/2
Description:
"""
from pydantic import BaseModel, Field


class AddApiHeaderRequest(BaseModel):
    key: str = Field(..., title="请求头key")
    value: str = Field(..., title="请求头value")
    value_type: str = Field(..., title="请求头value类型")
    enable: bool = Field(..., title="是否启用")
    comment: str = Field(None, title="备注")


class UpdateApiHeaderRequest(BaseModel):
    header_id: int = Field(..., title="请求头id")
    key: str = Field(None, title="请求头key")
    value: str = Field(None, title="请求头value")
    value_type: str = Field(None, title="请求头value类型")
    enable: bool = Field(None, title="是否启用")
    comment: str = Field(None, title="备注")


class DeleteApiHeaderRequest(BaseModel):
    header_id: int = Field(..., title="请求头id")


class ApiHeaderShow(BaseModel):
    header_id: int = Field(..., title="请求头id")
    key: str = Field(..., title="请求头key")
    value: str = Field(..., title="请求头value")
    value_type: str = Field(..., title="请求头value类型")
    enable: bool = Field(..., title="是否启用")
    comment: str = Field(None, title="备注")
