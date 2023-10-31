# coding=utf-8
"""
File: api_case_router.py
Author: bot
Created: 2023/8/2
Description:
"""

from fastapi import APIRouter, Depends


from app.handler.serializer.response_serializer import C137Response
from app.schemas.api_case.api_case_schema_new import SchemaRequestAddCase, SchemaRequestDebugCase
from app.schemas.api_case.api_case_schema_new_new import CaseFullAdd, CaseFullUpdate
from app.schemas.api_case.api_case_schemas import OrmFullCase
from app.schemas.api_case.api_path_schema import *
from app.schemas.api_case.api_headers_schema import *
from app.schemas.api_case.api_case_schema import *
from app.middleware.access_permission import Permission
from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.schemas.api_case.api_request_temp import TempRequestApi
from app.services.api_case.api_case_services import ApiCaseServices
import uuid


case = APIRouter()


# @case.get("/{case_id}", summary="查询用例详情", response_model=ApiCaseInfoResponse)
# async def get_api_case(case_id: int):
#     result = await ApiCaseServices.query_case_detail(case_id)
#
#     return C137Response.success(data=result)


@case.post("/add", summary="添加用例")
async def add_case(data: CaseFullAdd, user=Depends(Permission())):
    case_id = await ApiCaseServices.add_case(data, user["user_id"])
    return C137Response.success(data={"case_id": case_id})


@case.delete("/delete", summary="删除用例")
async def delete_api_case(data: DeleteApiCaseRequest, user=Depends(Permission())):
    await ApiCaseServices.delete_case(data.case_id, user["user_id"])
    return C137Response.success(message="删除成功")


@case.put("/update", summary="更新用例")
async def update_api_case(form: CaseFullUpdate, user=Depends(Permission())):
    await ApiCaseServices.update_case(form, user["user_id"])
    return C137Response.success(message="更新成功")


@case.post("/request", summary="调试请求用例")
async def debug_temp_case(data: OrmFullCase, user=Depends(Permission())):
    random_uid = f"c:runner_temp_request"
    result = await ApiCaseServices.temp_request(data, user["user_id"])
    return C137Response.success(data=result, headers={"trace_id": random_uid})


@case.get("/timer", summary="定时任务")
async def timer_runner():
    random_uid = str(uuid.uuid4())
    response = await ApiCaseServices.run_case_suite(random_uid, 5, [1, 29])
    return C137Response.success(data=response)


@case.get("/{case_id}", summary="查询用例详情")
async def get_api_case(case_id: int):
    result = await ApiCaseServices.query_case_details(case_id)
    return C137Response.success(data=result)
