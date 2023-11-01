# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field


class RequestRedisUpdate(BaseModel):
    name: str = Field(None, description="Redis配置名称")
    host: str = Field(None, description="Redis配置地址")
    port: int = Field(None, description="Redis配置端口")
    db: int = Field(None, description="Redis配置DB")
    username: str = Field(None, description="Redis配置账号")
    password: str = Field(None, description="Redis配置密码")
    # cluster: bool = Field(None, description="TODO: Redis集群..")
