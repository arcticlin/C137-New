# coding=utf-8
"""
File: header_crud.py
Author: bot
Created: 2023/10/25
Description:
"""
import json
from typing import List

from app.core.db_connector import async_session
from sqlalchemy import select, and_
from app.models.apicase.api_headers import ApiHeadersModel
from app.handler.serializer.response_serializer import C137Response
from loguru import logger

from app.services.api_case_new.case_params.headers.schema.response import ResponseHeaderInfo


class ApiHeaderCrud:
    @staticmethod
    async def query_header_by_case_id(case_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ApiHeadersModel).where(and_(ApiHeadersModel.case_id == case_id, ApiHeadersModel.deleted_at == 0))
            )
            result = smtm.scalars().all()
            return result

    @staticmethod
    async def query_header_by_env_id(env_id: int):
        async with async_session() as session:
            smtm = await session.execute(
                select(ApiHeadersModel).where(and_(ApiHeadersModel.env_id == env_id, ApiHeadersModel.deleted_at == 0))
            )
            result = smtm.scalars().all()
            return result

    @staticmethod
    def covert_values(value: str, value_type: int):
        try:
            if value_type == 1:
                return value
            elif value_type == 2:
                return int(value)
            elif value_type == 3:
                return bool(value)
            else:
                return json.loads(value)
        except Exception as e:
            logger.error(f"转换参数值失败, 原因: {e}")
            return value

    @staticmethod
    async def covert_header_to_dict(header_list: list):
        result = {}
        to_python = C137Response.orm_with_list(header_list)
        for header in to_python:
            result[header["key"]] = ApiHeaderCrud.covert_values(header["value"], header["value_type"])
        return result

    @staticmethod
    async def cover_header_to_ts(header_list: List) -> ResponseHeaderInfo:
        result = C137Response.orm_with_list()
