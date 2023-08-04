# coding=utf-8
"""
File: sql_schema.py
Author: bot
Created: 2023/8/4
Description:
"""
from pydantic import BaseModel, Field
from app.schemas.response_schema import CommonResponse


class AddSqlRequest(BaseModel):

    name: str = Field(..., description="SQL配置名称")
    host: str = Field(..., description="SQL配置地址")
    port: int = Field(..., description="SQL配置端口")
    db_user: str = Field(..., description="SQL配置账号")
    db_password: str = Field(None, description="SQL配置密码")
    db_name: str = Field(..., description="SQL配置数据库名称")
    sql_type: int = Field(..., description="SQL配置类型, 1: Mysql  2: POSTGRESQL 3: MONGODB")


class UpdateSqlRequest(BaseModel):
    name: str = Field(None, description="SQL配置名称")
    host: str = Field(None, description="SQL配置地址")
    port: int = Field(None, description="SQL配置端口")
    db_user: str = Field(None, description="SQL配置账号")
    db_password: str = Field(None, description="SQL配置密码")
    db_name: str = Field(None, description="SQL配置数据库名称")
    sql_type: int = Field(None, description="SQL配置类型, 1: Mysql  2: POSTGRESQL 3: MONGODB")


class SqlDetailShow(BaseModel):
    sql_id: int = Field(..., description="SQL配置ID")
    name: str = Field(..., description="SQL配置名称")
    host: str = Field(..., description="SQL配置地址")
    port: int = Field(..., description="SQL配置端口")
    db_user: str = Field(..., description="SQL配置账号")
    db_password: str = Field(None, description="SQL配置密码")
    db_name: str = Field(..., description="SQL配置数据库名称")
    sql_type: int = Field(..., description="SQL配置类型, 1: Mysql  2: POSTGRESQL 3: MONGODB")
    create_user: int = Field(..., description="创建人")


class SqlDetailResponse(CommonResponse):
    data: SqlDetailShow
