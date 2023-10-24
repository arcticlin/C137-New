# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field


class RequestSqlUpdate(BaseModel):
    name: str = Field(None, description="SQL配置名称")
    host: str = Field(None, description="SQL配置地址")
    port: int = Field(None, description="SQL配置端口")
    db_user: str = Field(None, description="SQL配置账号")
    db_password: str = Field(None, description="SQL配置密码")
    db_name: str = Field(None, description="SQL配置数据库名称")
    sql_type: int = Field(None, description="SQL配置类型, 1: Mysql  2: POSTGRESQL 3: MONGODB")
