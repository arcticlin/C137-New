# coding=utf-8
"""
File: api_path_schema.py
Author: bot
Created: 2023/8/2
Description:
"""
from pydantic import BaseModel, Field


class AddApiPathRequest(BaseModel):
    key: str = Field(..., title="请求路径key")
    value: str = Field(..., title="请求路径value")
    types: int = Field(..., title="类型, 1: Path, 2: Query")
    enable: bool = Field(..., title="是否启用")
    comment: str = Field(None, title="备注")


class UpdateApiPathRequest(BaseModel):
    path_id: int = Field(..., title="请求路径id")
    key: str = Field(None, title="请求路径key")
    value: str = Field(None, title="请求路径value")
    types: int = Field(None, title="类型, 1: Path, 2: Query")
    enable: bool = Field(None, title="是否启用")
    comment: str = Field(None, title="备注")


class DeleteApiPathRequest(BaseModel):
    path_id: int = Field(..., title="请求路径id")


class ApiPathShow(BaseModel):
    path_id: int = Field(..., title="请求头id")
    key: str = Field(..., title="请求路径key")
    value: str = Field(..., title="请求路径value")
    types: int = Field(..., title="类型, 1: Path, 2: Query")
    enable: bool = Field(..., title="是否启用")
    comment: str = Field(None, title="备注")
