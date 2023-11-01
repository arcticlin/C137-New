# coding=utf-8
"""
File: response.py
Author: bot
Created: 2023/10/24
Description:
"""
from typing import List

from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse
from app.services.common_config.schema.sql.info import SqlListOut, SqlDetailOut
from app.services.common_config.schema.sql.news import RequestSqlAdd


class ResponseSqlAdd(CommonResponse):
    data: RequestSqlAdd = Field(..., description="SQL配置ID")


class ResponseSqlList(CommonResponse):
    data: List[SqlListOut] = Field(..., description="SQL配置列表")


class ResponseSqlDetail(CommonResponse):
    data: SqlDetailOut = Field(..., description="SQL配置详情")
