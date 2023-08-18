# coding=utf-8
"""
File: config_router.py
Author: bot
Created: 2023/8/4
Description:
"""

from fastapi import APIRouter, Query, Depends

from app.schemas.api_settings.suffix_schema import AddSuffixSchema, DeleteSuffixSchema, EnableSuffixSchema
from app.schemas.cconfig.env_schema import EnvListResponse, EnvAddRequest, EnvUpdateRequest
from app.schemas.response_schema import CommonResponse
from app.schemas.cconfig.sql_schema import *
from app.schemas.cconfig.redis_schema import *
from app.schemas.cconfig.script_schema import *
from app.middleware.access_permission import Permission
from app.services.cconfig.cconfig_services import CommonConfigServices
from app.handler.response_handler import C137Response
from app.handler.db_handler import DataBaseConnect
from app.schemas.cconfig.env_schema import EnvDetailResponse
from app.services.api_case.suffix_services import SuffixServices

cconfig = APIRouter()


@cconfig.get("/env/list", summary="获取环境列表", response_model=EnvListResponse)
async def get_env_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
):
    total, result = await CommonConfigServices.query_env_list(page, page_size)
    return C137Response.success(data=result, total=total)


@cconfig.get("/env/detail/{env_id}", summary="获取环境详情", response_model=EnvDetailResponse)
async def get_env_list(env_id: int):
    result = await CommonConfigServices.query_env_detail(env_id)
    return C137Response.success(data=result)


@cconfig.post("/env/add", summary="新增环境")
async def add_env(form: EnvAddRequest, user=Depends(Permission())):
    await CommonConfigServices.add_env(form, user["user_id"])
    return C137Response.success(message="添加成功")


@cconfig.post("/suffix/add", summary="新增前后置")
async def add_suffix(form: AddSuffixSchema, user=Depends(Permission())):
    await SuffixServices.add_suffix(form, user["user_id"])
    return C137Response.success(message="添加成功")


@cconfig.post("/suffix/delete", summary="删除前后置")
async def delete_suffix(data: DeleteSuffixSchema, user=Depends(Permission())):
    await SuffixServices.delete_suffix(data, user["user_id"])
    return C137Response.success(message="删除成功")


@cconfig.post("/suffix/enable", summary="删除前后置")
async def delete_suffix(data: EnableSuffixSchema, user=Depends(Permission())):
    await SuffixServices.enable_suffix(data, user["user_id"])
    return C137Response.success(message="删除成功")


@cconfig.post("/env/update/{env_id}", summary="更新环境")
async def update_env(env_id: int, form: EnvUpdateRequest, user=Depends(Permission())):
    await CommonConfigServices.update_env(env_id, form, user["user_id"])
    return C137Response.success(message="更新成功")


@cconfig.get("/redis/list", summary="获取Redis配置列表", response_model=RedisListResponse)
async def get_redis_config_list():
    result = await CommonConfigServices.query_redis_list()
    return C137Response.success(data=result)


@cconfig.post("/redis/new", summary="新增Redis配置")
async def new_redis_config(data: AddRedisRequest, user=Depends(Permission())):
    await CommonConfigServices.add_redis_config(data, user["user_id"])
    return C137Response.success(message="添加成功")


@cconfig.post("/redis/{redis_id}", summary="获取Redis配置")
async def get_redis_config_detail(redis_id: int, user=Depends(Permission())):
    result = await CommonConfigServices.query_redis_detail(redis_id)
    return C137Response.success(data=result)


@cconfig.put("/redis/{redis_id}", summary="更新Redis配置")
async def update_redis_config(redis_id: int, data: UpdateRedisRequest, user=Depends(Permission())):
    await CommonConfigServices.update_redis_config(data, redis_id, user["user_id"])
    return C137Response.success(message="更新成功")


@cconfig.delete("/redis/{redis_id}", summary="删除Redis配置")
async def delete_redis_config(redis_id: int, user=Depends(Permission())):
    await CommonConfigServices.delete_redis_config(redis_id, user["user_id"])
    return C137Response.success(message="删除成功")


@cconfig.get("/sql/list", summary="获取sql配置列表", response_model=SqlListResponse)
async def get_sql_config_list():
    result = await CommonConfigServices.query_sql_list()
    return C137Response.success(data=result)


@cconfig.post("/sql/new", summary="新增sql配置")
async def new_sql_config(data: AddSqlRequest, user=Depends(Permission())):
    await CommonConfigServices.add_sql_config(data, user["user_id"])
    return C137Response.success(message="添加成功")


@cconfig.post("/sql/ping", summary="测试sql连接")
async def ping_sql(data: PingSqlRequest):
    await CommonConfigServices.ping_sql(data.sql_id)
    return C137Response.success(message="连接成功")


@cconfig.post("/sql/execute", summary="执行sql")
async def execute_sql(data: ExecuteSqlRequest):
    result = await CommonConfigServices.execute_sql(data.sql_id, data.text)
    return C137Response.success(data=result)


@cconfig.post("/sql/execute/debug", summary="执行sql")
async def execute_sql(data: ExecuteSqlDebugRequest):
    result = await CommonConfigServices.execute_sql(data.sql_id, data.text, data.run_out_name)
    return C137Response.success(data=result)


@cconfig.post("/sql/{sql_id}", summary="获取sql配置")
async def get_sql_config_detail(sql_id: int, user=Depends(Permission())):
    result = await CommonConfigServices.query_sql_detail(sql_id)
    return C137Response.success(data=result)


@cconfig.put("/sql/{sql_id}", summary="更新sql配置")
async def update_sql_config(sql_id: int, data: UpdateSqlRequest, user=Depends(Permission())):
    await CommonConfigServices.update_sql_config(data, sql_id, user["user_id"])
    return C137Response.success(message="更新成功")


@cconfig.delete("/sql/{sql_id}", summary="删除sql配置")
async def delete_sql_config(sql_id: int, user=Depends(Permission())):
    await CommonConfigServices.delete_sql_config(sql_id, user["user_id"])
    return C137Response.success(message="删除成功")


@cconfig.get("/script/list", summary="获取script配置列表")
async def get_script_config_list(
    user_id: int = Query(0, description="查看我的脚本, 不传则是我+公共的"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
):
    total, result = await CommonConfigServices.query_script_list(page, page_size, user_id)
    return C137Response.success(data=result, total=total)


@cconfig.post("/script/new", summary="新增script配置")
async def new_script_config(data: AddScriptRequest, user=Depends(Permission())):
    await CommonConfigServices.add_script_config(data, user["user_id"])
    return C137Response.success(message="添加成功")


@cconfig.post("/script/{script_id}", summary="获取script配置")
async def get_script_config_detail(script_id: int, user=Depends(Permission())):
    result = await CommonConfigServices.query_script_detail(script_id)
    return C137Response.success(data=result)


@cconfig.put("/script/{script_id}", summary="更新script配置")
async def update_script_config(script_id: int, data: UpdateScriptRequest, user=Depends(Permission())):
    await CommonConfigServices.update_script_config(data, script_id, user["user_id"])
    return C137Response.success(message="更新成功")


@cconfig.delete("/script/{script_id}", summary="删除script配置")
async def delete_script_config(script_id: int, user=Depends(Permission())):
    await CommonConfigServices.delete_script_config(script_id, user["user_id"])
    return C137Response.success(message="删除成功")


@cconfig.post("/script/execute/debug", summary="执行script脚本")
async def debug_script(data: DebugScriptSchema):
    result = await CommonConfigServices.new_python_script_debug(data)
    return C137Response.success(data=result)


@cconfig.post("/redis/ping", summary="测试redis连接")
async def ping_redis(data: PingRedisRequest):
    pass
