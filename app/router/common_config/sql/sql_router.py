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
from app.services.common_config.schema.sql.news import RequestSqlAdd, RequestSqlPingByForm, RequestSqlCommandDebug
from app.services.common_config.schema.sql.response import ResponseSqlAdd, ResponseSqlDetail, ResponseSqlList
from app.services.common_config.schema.sql.update import RequestSqlUpdate
from app.services.common_config.sql_service import SqlService

sql_router = APIRouter(prefix="/sql")


@sql_router.get("/list", summary="SQL列表", response_model=ResponseSqlList)
async def get_sql_list(page: int = Query(1), page_size: int = Query(20), user_id=Depends(Permission())):
    result, total = await SqlService.query_sql_list(page, page_size)
    return C137Response.success(data=result, total=total)


@sql_router.post("/new", summary="创建SQL连接配置", response_model=ResponseSqlAdd)
async def create_sql_config(form: RequestSqlAdd, user_id=Depends(Permission())):
    s_id = await SqlService.create_sql_config(form, user_id["user_id"])
    return C137Response.success(data={"sql_id": s_id})


@sql_router.post("/ping", summary="SQL连接测试, 通过表单", response_model=CommonResponse)
async def ping_sql_by_form(form: RequestSqlPingByForm, user_id=Depends(Permission())):
    await SqlService.ping_sql_by_form(form)
    return C137Response.success(message="pong")


@sql_router.post("/debug", summary="SQL调试语句", response_model=CommonResponse)
async def ping_sql_by_form(form: RequestSqlCommandDebug, user_id=Depends(Permission())):
    await SqlService.debug_sql_command(form)
    return C137Response.success(message="pong")


@sql_router.get("/{sql_id}/detail", summary="SQL连接配置详情", response_model=ResponseSqlDetail)
async def get_sql_detail(sql_id: int, user_id=Depends(Permission())):
    result = await SqlService.query_sql_by_id(sql_id)
    return C137Response.success(data=result)


@sql_router.get("/{sql_id}/ping", summary="SQL连接测试, 通过RedisID", response_model=CommonResponse)
async def ping_sql_by_id(sql_id: int, user_id=Depends(Permission())):
    await SqlService.ping_sql_by_id(sql_id)
    return C137Response.success(message="pong")


@sql_router.put("/{sql_id}/update", summary="更新SQL连接配置", response_model=CommonResponse)
async def update_sql_config(sql_id: int, form: RequestSqlUpdate, user_id=Depends(Permission())):
    await SqlService.update_sql_config(sql_id, form, user_id["user_id"])
    return C137Response.success()


@sql_router.delete("/{sql_id}/delete", summary="删除SQL连接配置", response_model=CommonResponse)
async def delete_sql_config(sql_id: int, user_id=Depends(Permission())):
    await SqlService.delete_sql_config(sql_id, user_id["user_id"])
    return C137Response.success()
