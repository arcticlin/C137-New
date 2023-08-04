# coding=utf-8
"""
File: redis_schema.py
Author: bot
Created: 2023/8/4
Description:
"""

from pydantic import BaseModel, Field
from app.schemas.response_schema import CommonResponse


class AddRedisRequest(BaseModel):
    name: str = Field(..., description="Redis配置名称")
    host: str = Field(..., description="Redis配置地址")
    port: int = Field(..., description="Redis配置端口")
    username: str = Field(..., description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    # cluster: bool = Field(False, description="TODO: Redis集群..")


class UpdateRedisRequest(BaseModel):
    name: str = Field(None, description="Redis配置名称")
    host: str = Field(None, description="Redis配置地址")
    port: int = Field(None, description="Redis配置端口")
    username: str = Field(None, description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    # cluster: bool = Field(None, description="TODO: Redis集群..")


class RedisDetailShow(BaseModel):
    redis_id: int = Field(..., description="Redis配置ID")
    name: str = Field(..., description="Redis配置名称")
    host: str = Field(..., description="Redis配置地址")
    port: int = Field(..., description="Redis配置端口")
    username: str = Field(..., description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    # cluster: bool = Field(None, description="TODO: Redis集群..")
    create_user: int = Field(..., description="创建人")


class RedisDetailResponse(CommonResponse):
    data: RedisDetailShow
