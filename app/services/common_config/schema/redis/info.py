# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field


class RedisListOut(BaseModel):
    redis_id: int = Field(..., description="Redis配置ID")
    name: str = Field(..., description="Redis配置名称")
    host: str = Field(..., description="Redis配置地址")


class RedisDetailOut(BaseModel):
    redis_id: int = Field(..., description="Redis配置ID")
    name: str = Field(..., description="Redis配置名称")
    host: str = Field(..., description="Redis配置地址")
    port: int = Field(..., description="Redis配置端口")
    username: str = Field(None, description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    db: int = Field(0, description="Redis配置DB")
    # cluster: bool = Field(None, description="TODO: Redis集群..")
    create_user: int = Field(..., description="创建人")
