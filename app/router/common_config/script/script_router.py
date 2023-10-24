# coding=utf-8
"""
File: sql_router.py
Author: bot
Created: 2023/10/24
Description:
"""
from fastapi import APIRouter, Depends

from app.core.basic_schema import CommonResponse
from app.middleware.access_permission import Permission
from app.services.common_config.schema.script.news import RequestScriptAdd, RequestScriptDebugByForm
from app.services.common_config.schema.script.response import (
    ResponseScriptAdd,
    ResponseScriptDetail,
    ResponseScriptList,
)
from app.services.common_config.schema.script.update import RequestScriptUpdate


script_router = APIRouter(prefix="/script")


@script_router.get("/list", summary="公共脚本列表", response_model=ResponseScriptList)
async def get_script_list(user_id: int = Depends(Permission())):
    pass


@script_router.post("/new", summary="创建公共脚本", response_model=ResponseScriptAdd)
async def create_script_config(form: RequestScriptAdd, user_id: int = Depends(Permission())):
    pass


@script_router.post("/debug", summary="公共脚本调试", response_model=CommonResponse)
async def ping_script_by_form(form: RequestScriptDebugByForm, user_id: int = Depends(Permission())):
    pass


@script_router.get("/{script_id}/detail", summary="公共脚本详情", response_model=ResponseScriptDetail)
async def get_script_detail(script_id: int, user_id: int = Depends(Permission())):
    pass


@script_router.get("/{script_id}/run", summary="公共脚本运行", response_model=CommonResponse)
async def ping_script_by_id(script_id: int, user_id: int = Depends(Permission())):
    pass


@script_router.put("/{script_id}/update", summary="更新公共脚本", response_model=CommonResponse)
async def update_script_config(form: RequestScriptUpdate, user_id: int = Depends(Permission())):
    pass


@script_router.delete("/{script_id}/delete", summary="删除公共脚本", response_model=CommonResponse)
async def delete_script_config(script_id: int, user_id: int = Depends(Permission())):
    pass
