# coding=utf-8
"""
File: news.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse


class RequestRedisAdd(BaseModel):
    name: str = Field(..., description="Redis配置名称")
    host: str = Field(..., description="Redis配置地址")
    port: int = Field(..., description="Redis配置端口")
    db: int = Field(0, description="Redis配置DB")
    username: str = Field(None, description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    # cluster: bool = Field(False, description="TODO: Redis集群..")


class RedisAddOut(BaseModel):
    redis_id: int = Field(..., description="Redis配置ID")


class RequestRedisPingByForm(BaseModel):
    host: str = Field(..., description="Redis配置地址")
    port: int = Field(..., description="Redis配置端口")
    db: int = Field(0, description="Redis配置DB")
    username: str = Field(None, description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
