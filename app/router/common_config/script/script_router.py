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
from app.services.common_config.schema.script.news import RequestScriptAdd, RequestScriptDebugByForm
from app.services.common_config.schema.script.response import (
    ResponseScriptAdd,
    ResponseScriptDetail,
    ResponseScriptList,
)
from app.services.common_config.schema.script.update import RequestScriptUpdate
from app.services.common_config.script_service import ScriptService

script_router = APIRouter(prefix="/script")


@script_router.get("/list", summary="公共脚本列表", response_model=ResponseScriptList)
async def get_script_list(page: int = Query(1), page_size: int = Query(20), user_id=Depends(Permission())):
    result, total = await ScriptService.query_script_list(page, page_size, user_id["user_id"])
    return C137Response.success(data=result, total=total)


@script_router.post("/new", summary="创建公共脚本", response_model=ResponseScriptAdd)
async def create_script_config(form: RequestScriptAdd, user_id=Depends(Permission())):
    script_id = await ScriptService.create_script_config(form, user_id["user_id"])
    return C137Response.success(data={"script_id": script_id})


@script_router.post("/debug", summary="公共脚本调试", response_model=CommonResponse)
async def ping_script_by_form(form: RequestScriptDebugByForm, user_id=Depends(Permission())):
    result = await ScriptService.debug_script_by_form(form)
    return C137Response.success(data=result)


@script_router.get("/{script_id}/detail", summary="公共脚本详情", response_model=ResponseScriptDetail)
async def get_script_detail(script_id: int, user_id=Depends(Permission())):
    result = await ScriptService.query_script_by_id(script_id)
    return C137Response.success(data=result)


@script_router.get("/{script_id}/run", summary="公共脚本运行", response_model=CommonResponse)
async def ping_script_by_id(script_id: int, user_id=Depends(Permission())):
    result = await ScriptService.debug_script_by_id(script_id)
    return C137Response.success(data=result)


@script_router.put("/{script_id}/update", summary="更新公共脚本", response_model=CommonResponse)
async def update_script_config(script_id: int, form: RequestScriptUpdate, user_id=Depends(Permission())):
    await ScriptService.update_script_config(script_id, form, user_id["user_id"])
    return C137Response.success()


@script_router.delete("/{script_id}/delete", summary="删除公共脚本", response_model=CommonResponse)
async def delete_script_config(script_id: int, user_id=Depends(Permission())):
    await ScriptService.delete_script_config(script_id, user_id["user_id"])
    return C137Response.success()
