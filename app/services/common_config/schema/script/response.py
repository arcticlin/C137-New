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
from app.services.common_config.schema.script.info import ScriptListOut, ScriptDetailOut
from app.services.common_config.schema.script.news import ScriptAddOut
from app.services.common_config.schema.sql.info import SqlListOut, SqlDetailOut
from app.services.common_config.schema.sql.news import RequestSqlAdd


class ResponseScriptAdd(CommonResponse):
    data: ScriptAddOut = Field(..., description="Script配置ID")


class ResponseScriptList(CommonResponse):
    data: List[ScriptListOut] = Field(..., description="Script配置列表")


class ResponseScriptDetail(CommonResponse):
    data: ScriptDetailOut = Field(..., description="Script配置详情")
