# coding=utf-8
"""
File: api_case.py
Author: bot
Created: 2023/10/26
Description:
"""
from typing import List

from fastapi import APIRouter, Depends, Query

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
import uuid

from app.middleware.access_permission import Permission
from app.services.api_case.case.schema.debug_form import RequestDebugForm
from app.services.api_case.case.schema.new import RequestApiCaseNew
from app.services.api_case.case.schema.response import ResponseCaseNew, ResponseCaseDetail, ResponseDebugResult
from app.services.api_case.case.schema.runner import RequestRunSingleCase, RequestRunMultiCase
from app.services.api_case.case_service import CaseService
from app.services.directory.schema.dir_new import ResponseDirectoryCaseList

cases = APIRouter()


@cases.post("/add", summary="添加用例", response_model=ResponseCaseNew)
async def add_case(data: RequestApiCaseNew, user=Depends(Permission())):
    case_id = await CaseService.add_api_case(data, user["user_id"])
    return C137Response.success(data={"case_id": case_id})


# @cases.post("/debug", summary="调试用例", response_model=ResponseDebugResult)
@cases.post("/debug", summary="调试用例", response_model=CommonResponse)
async def debug_case(form: RequestDebugForm, user=Depends(Permission())):
    random_uid = str(uuid.uuid4())
    response = await CaseService.debug_temp_case(random_uid, form, user["user_id"])
    return C137Response.success(data=response)


@cases.post("/run_case", summary="执行用例", response_model=CommonResponse)
async def run_single_case(data: RequestRunMultiCase, user=Depends(Permission())):
    random_uid = str(uuid.uuid4())
    response = await CaseService.run_case_by_id(
        "dff8e6de-811f-45d4-93bd-2a38cb9fc2f5", data.env_id, data.case_id, user["user_id"]
    )
    return C137Response.success(data=response)


@cases.get("/case_list", summary="用例列表", response_model=ResponseDirectoryCaseList)
async def get_case_list(
    directory_id: int = Query(..., description="目录ID"),
    page: int = Query(1, description="页数"),
    page_size: int = Query(20, description="页码"),
    filter_user: int = Query(None, description="筛选用户"),
    filter_status: int = Query(None, description="筛选状态"),
    filter_priority: str = Query(None, description="筛选优先级"),
    filter_name: str = Query(None, description="筛选经常"),
    user=Depends(Permission()),
):
    case_list, count = await CaseService.get_case_list(
        directory_id, page, page_size, filter_user, filter_status, filter_priority, filter_name
    )
    return C137Response.success(data=case_list, total=count)


@cases.delete("/{case_id}/delete", summary="删除用例", response_model=CommonResponse)
async def delete_case(case_id: int, user=Depends(Permission())):
    await CaseService.delete_api_case(case_id, user["user_id"])
    return C137Response.success(message="删除成功")


@cases.put("/{case_id}/update", summary="更新用例", response_model=CommonResponse)
async def update_case(case_id: int, user=Depends(Permission())):
    pass


@cases.get("/{case_id}/detail", summary="用例详情", response_model=ResponseCaseDetail)
async def case_detail(case_id: int, user=Depends(Permission())):
    result = await CaseService.query_case_detail(case_id, user["user_id"])
    return C137Response.success(data=result)
