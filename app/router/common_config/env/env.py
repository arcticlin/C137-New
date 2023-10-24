# coding=utf-8
"""
File: env.py
Author: bot
Created: 2023/10/23
Description:
"""
from fastapi import APIRouter, Depends, Query

from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.common_config.schema.env.news import RequestEnvNew
from app.services.common_config.schema.env.responses import ResponseEnvList, ResponseEnvDetail, ResponseEnvAdd
from app.core.basic_schema import CommonResponse
from app.services.common_config.env_service import EnvService

envs = APIRouter(prefix="/envs")


@envs.get("/list", summary="环境列表", response_model=ResponseEnvList)
async def get_env_list(page: int = Query(1), page_size: int = Query(20), user_id=Depends(Permission())):
    result, total = await EnvService.get_env_list(page, page_size, user_id["user_id"])
    return C137Response.success(data=result, total=total)


@envs.post("/new", summary="新建环境", response_model=ResponseEnvAdd)
async def new_env(data: RequestEnvNew, user_id=Depends(Permission())):
    pass


@envs.get("/{env_id}", summary="环境详情", response_model=ResponseEnvDetail)
async def get_env_detail(env_id: int, user_id=Depends(Permission())):
    result = await EnvService.get_env_detail(env_id)
    return C137Response.success(data=result)


@envs.delete("/{env_id}", summary="删除环境", response_model=CommonResponse)
async def delete_env(env_id: int, user_id=Depends(Permission())):
    pass


@envs.put("/{env_id}", summary="更新环境", response_model=CommonResponse)
async def update_env(env_id: int, user_id=Depends(Permission())):
    pass
