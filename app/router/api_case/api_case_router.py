# coding=utf-8
"""
File: api_case_router.py
Author: bot
Created: 2023/8/2
Description:
"""

from fastapi import APIRouter, Depends


from app.handler.response_handler import C137Response
from app.schemas.api_case.api_case_schema_new import SchemaRequestAddCase, SchemaRequestDebugCase
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


@case.get("/{case_id}", summary="查询用例详情")
async def get_api_case(case_id: int):
    result = await ApiCaseServices.query_case_details(case_id)
    return C137Response.success(data=result)


@case.post("/add_form", summary="添加用例")
async def add_api_case_form(form: SchemaRequestAddCase, user=Depends(Permission())):
    case_id = await ApiCaseServices.add_case_form(form, user["user_id"])
    return C137Response.success(message="添加成功", data={"case_id": case_id})


@case.delete("/delete", summary="删除用例")
async def delete_api_case(data: DeleteApiCaseRequest, user=Depends(Permission())):
    await ApiCaseServices.delete_case(data.case_id, user["user_id"])
    return C137Response.success(message="删除成功")


@case.put("/update", summary="更新用例")
async def update_api_case():
    await ApiCaseServices.query_case_details(2)


@case.post("/request", summary="调试请求用例")
async def debug_temp_case(data: OrmFullCase, user=Depends(Permission())):
    random_uid = f"c:runner_temp_request"
    print("1")
    result = await ApiCaseServices.temp_request(data, user["user_id"])
    return C137Response.success(data=result, headers={"trace_id": random_uid})
