# coding=utf-8
"""
File: sql_router.py
Author: bot
Created: 2023/10/24
Description:
"""
from fastapi import APIRouter, Depends, Query

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.common_config.redis_service import RedisService
from app.services.common_config.schema.redis.news import RequestRedisAdd, RequestRedisPingByForm
from app.services.common_config.schema.redis.response import ResponseRedisList, ResponseRedisDetail, ResponseRedisAdd
from app.services.common_config.schema.redis.update import RequestRedisUpdate


rds_router = APIRouter(prefix="/redis")


@rds_router.get("/list", summary="Redis列表", response_model=ResponseRedisList)
async def get_redis_list(page: int = Query(1), page_size: int = Query(20), user_id=Depends(Permission())):
    result, total = await RedisService.query_redis_list(page, page_size)
    return C137Response.success(data=result, total=total)


@rds_router.post("/new", summary="创建Redis连接配置", response_model=ResponseRedisAdd)
async def create_redis_config(form: RequestRedisAdd, user_id=Depends(Permission())):
    r_id = await RedisService.create_redis_config(form, user_id["user_id"])
    return C137Response.success(data={"redis_id": r_id})


@rds_router.post("/ping", summary="Redis连接测试, 通过表单", response_model=CommonResponse)
async def ping_redis_by_form(form: RequestRedisPingByForm, user_id: int = Depends(Permission())):
    await RedisService.ping_redis_by_form(form)
    return C137Response.success(message="pong")


@rds_router.get("/{redis_id}/detail", summary="Redis连接配置详情", response_model=ResponseRedisDetail)
async def get_redis_detail(redis_id: int, user_id: int = Depends(Permission())):
    result = await RedisService.query_redis_by_id(redis_id)
    return C137Response.success(data=result)


@rds_router.get("/{redis_id}/ping", summary="Redis连接测试, 通过RedisID", response_model=CommonResponse)
async def ping_redis_by_id(redis_id: int, user_id: int = Depends(Permission())):
    await RedisService.ping_redis_by_id(redis_id)
    return C137Response.success(message="pong")


@rds_router.put("/{redis_id}/update", summary="更新Redis连接配置", response_model=CommonResponse)
async def update_redis_config(redis_id: int, form: RequestRedisUpdate, user_id=Depends(Permission())):
    await RedisService.update_redis_config(redis_id, form, user_id["user_id"])
    return C137Response.success()


@rds_router.delete("/{redis_id}/delete", summary="删除Redis连接配置", response_model=CommonResponse)
async def delete_redis_config(redis_id: int, user_id=Depends(Permission())):
    await RedisService.delete_redis_config(redis_id, user_id["user_id"])
    return C137Response.success()
