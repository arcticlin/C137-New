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
from app.services.common_config.schema.redis.info import RedisListOut, RedisDetailOut
from app.services.common_config.schema.redis.news import RedisAddOut


class ResponseRedisAdd(CommonResponse):
    data: RedisAddOut = Field(..., description="Redis配置ID")


class ResponseRedisList(CommonResponse):
    data: List[RedisListOut] = Field(..., description="Redis配置列表")


class ResponseRedisDetail(CommonResponse):
    data: RedisDetailOut = Field(..., description="Redis配置详情")
