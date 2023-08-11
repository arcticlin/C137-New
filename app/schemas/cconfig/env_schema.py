# coding=utf-8
"""
File: env_schema.py
Author: bot
Created: 2023/8/11
Description:
"""
from pydantic import BaseModel, Field
from app.schemas.response_schema import CommonResponse


class EnvAddRequest(BaseModel):
    name: str = Field(..., description="环境名称")
    url: str = Field(..., description="环境URL")


class EnvUpdateRequest(BaseModel):
    name: str = Field(None, description="环境名称")
    url: str = Field(None, description="环境URL")


class EnvListShow(BaseModel):
    env_id: int = Field(..., description="环境ID")
    name: str = Field(..., description="环境名称")
    url: str = Field(..., description="环境URL")
    create_user: int = Field(..., description="创建人")


class EnvListResponse(CommonResponse):
    data: list[EnvListShow] = Field(..., description="环境列表")
    total: int = Field(..., description="总数")
