# coding=utf-8
"""
File: api_case_router.py
Author: bot
Created: 2023/8/2
Description:
"""

from fastapi import APIRouter, Depends
from app.handler.response_handler import C137Response
from app.schemas.api_case.api_path_schema import *
from app.schemas.api_case.api_headers_schema import *
from app.schemas.api_case.api_case_schema import *
from app.middleware.access_permission import Permission
from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.services.api_case.api_case_services import ApiCaseServices
import uuid

from app.services.api_case.suffix_services import SuffixServices

case = APIRouter()


@case.get("/{case_id}", summary="查询用例详情", response_model=ApiCaseInfoResponse)
async def get_api_case(case_id: int):
    result = await ApiCaseServices.query_case_detail(case_id)

    return C137Response.success(data=result)


@case.post("/add", summary="添加用例")
async def add_api_case(data: AddApiCaseRequest, user=Depends(Permission())):
    pass


@case.delete("/delete", summary="删除用例")
async def delete_api_case(data: DeleteApiCaseRequest, user=Depends(Permission())):
    await ApiCaseServices.delete_case(data.case_id, user["user_id"])
    return C137Response.success(message="删除成功")


@case.put("/update", summary="更新用例")
async def update_api_case(data: UpdateApiCaseRequest, user=Depends(Permission())):
    pass


@case.post("/debug", summary="调试用例")
async def debug_api_case(data: DebugApiCaseRequest):
    random_uid = f"c:runner_{str(uuid.uuid4())}"
    result = await ApiCaseServices.debug_case_execute(data.env_id, data.case_id, random_uid)
    return C137Response.success(data=result, headers={"trace_id": random_uid})
