# coding=utf-8
"""
File: ws_test.py
Author: bot
Created: 2023/11/20
Description:
"""
import asyncio
from typing import Dict, List

from fastapi import APIRouter, Query, Depends

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.ws_test.schema.ws_case.new import RequestAddWsCase
from app.services.ws_test.schema.ws_case.response import ResponseWsCaseList, ResponseWsCaseDetail
from app.services.ws_test.schema.ws_case.update import RequestUpdateWsCase
from app.services.ws_test.schema.ws_code.info import ResponseWsCodeList, ResponseWsCodeDetail
from app.services.ws_test.schema.ws_code.new import ResponseAddWsCode, RequestAddWsCode
from app.services.ws_test.schema.ws_code.update import RequestUpdateWsCode
from app.services.ws_test.schema.ws_plan.info import RequestQueryPlanList
from app.services.ws_test.schema.ws_plan.new import RequestAddWsPlan, RequestTestConnect, RequestTestRunCase
from app.services.ws_test.schema.ws_plan.response import ResponsePlanAdd, ResponsePlanList
from app.services.ws_test.schema.ws_plan.update import RequestUpdatePlan, RequestRemovePlanCase, RequestAddPlanCase
from app.services.ws_test.schema.ws_result.info import RequestMarkCase
from app.services.ws_test.schema.ws_result.response import ResponseStatisResult, ResponseWsCaseResult
from app.services.ws_test.services.ws_case_services import WsCaseService
from app.services.ws_test.services.ws_code_services import WsCodeService
from app.services.ws_test.services.ws_plan_services import WsPlanService
from app.services.ws_test.ws_test_services import WsTestService

wst = APIRouter()

ws_plan: Dict[str, WsTestService] = dict()


@wst.get("/code/list", summary="获取项目的WS_CODE列表", response_model=ResponseWsCodeList)
async def query_code_list(project_id: int = Query(..., description="项目ID")):
    """
    获取项目的WS_CODE列表
    :param project_id: 项目ID
    :return:
    """
    result, total = await WsCodeService.query_code_list(project_id)
    return C137Response.success(data=result, total=total)


@wst.post("/code/add", summary="添加WS_CODE", response_model=ResponseAddWsCode)
async def add_ws_code(data: RequestAddWsCode, user=Depends(Permission())):
    """
    添加WS_CODE
    :param data: WS_CODE信息
    :return:
    """
    # return await WsCodeService.add_ws_code(data
    ws_id = await WsCodeService.add_code_in_project(data, user["user_id"])
    return C137Response.success(data={"ws_id": ws_id})


@wst.get("/code/{ws_id}/detail", summary="获取WS_CODE详情", response_model=ResponseWsCodeDetail)
async def query_code_detail(ws_id: int, user=Depends(Permission())):
    """
    获取WS_CODE详情
    :param ws_id: WS_CODE ID
    :return:
    """
    result = await WsCodeService.query_code_detail(ws_id)
    return C137Response.success(data=result)


@wst.put("/code/{ws_id}/update", summary="修改WS_CODE详情", response_model=CommonResponse)
async def update_code_detail(ws_id: int, data: RequestUpdateWsCode, user=Depends(Permission())):
    """
    获取WS_CODE详情
    :param ws_id: WS_CODE ID
    :return:
    """
    await WsCodeService.update_code_detail(ws_id, data, user["user_id"])
    return C137Response.success()


@wst.delete("/code/{ws_id}/delete", summary="删除WS_CODE", response_model=CommonResponse)
async def delete_ws_code(ws_id: int, user=Depends(Permission())):
    """
    删除WS_CODE
    :param ws_id: WS_CODE ID
    :return:
    """
    await WsCodeService.remove_code(ws_id, user["user_id"])
    return C137Response.success()


@wst.post("/case/{ws_id}/add", summary="添加WS_CODE下的用例", response_model=CommonResponse)
async def add_ws_case(ws_id: int, data: RequestAddWsCase, user=Depends(Permission())):
    data.__setattr__("ws_id", ws_id)
    case_id = await WsCaseService.add_case_in_ws(data, user["user_id"])
    return C137Response.success(data={"case_id": case_id})


@wst.get("/case/{ws_id}/list", summary="获取WS_CODE下的用例列表", response_model=ResponseWsCaseList)
async def get_ws_cases(ws_id: int, user=Depends(Permission())):
    result = await WsCaseService.query_case_list(ws_id)
    return C137Response.success(data=result)


@wst.get("/case/{ws_id}/detail/{case_id}", summary="获取WS用例详情", response_model=ResponseWsCaseDetail)
async def get_ws_case_detail(ws_id: int, case_id: int, user=Depends(Permission())):
    result = await WsCaseService.query_case_detail(ws_id, case_id)
    return C137Response.success(data=result)


@wst.put("/case/{ws_id}/update", summary="修改WS_CODE下的用例", response_model=CommonResponse)
async def update_ws_case(ws_id: int, data: RequestUpdateWsCase, user=Depends(Permission())):
    await WsCaseService.update_case_detail(ws_id, data, user["user_id"])
    return C137Response.success()


@wst.delete("/case/{ws_id}/delete/{case_id}", summary="删除WS_CODE下的用例", response_model=CommonResponse)
async def delete_ws_case(ws_id: int, case_id: int, user=Depends(Permission())):
    await WsCaseService.remove_case(ws_id, case_id, user["user_id"])
    return C137Response.success()


@wst.post("/plan/add", summary="添加测试计划", response_model=ResponsePlanAdd)
async def add_ws_plan(data: RequestAddWsPlan, user=Depends(Permission())):
    pass


@wst.post("/plan/list", summary="获取测试计划列表", response_model=ResponsePlanList)
async def get_ws_plan_list(
    form: RequestQueryPlanList,
    user=Depends(Permission()),
):
    result, total = await WsPlanService.get_plan_list(
        form.page, form.page_size, form.filter_user, form.filter_name, form.filter_status, form.filter_project
    )
    return C137Response.success(data=result, total=total)


@wst.put("/plan/update", summary="修改测试计划", response_model=CommonResponse)
async def update_ws_plan(data: RequestUpdatePlan, user=Depends(Permission())):
    pass


@wst.post("/plan/case/remove", summary="删除测试用例", response_model=CommonResponse)
async def remove_ws_plan_case(data: RequestRemovePlanCase, user=Depends(Permission())):
    pass


@wst.post("/plan/case/add", summary="添加测试用例", response_model=CommonResponse)
async def remove_ws_plan_case_add(data: RequestAddPlanCase, user=Depends(Permission())):
    pass


@wst.post("/plan/{project_id}/add", summary="添加测试用例", response_model=CommonResponse)
async def remove_ws_plan_case_add(data: RequestAddPlanCase, user=Depends(Permission())):
    pass


@wst.delete("/plan/{plan_id}/delete", summary="删除测试计划", response_model=CommonResponse)
async def delete_ws_plan(plan_id: int, user=Depends(Permission())):
    pass


@wst.get("/plan/{plan_id}/statics", summary="获取测试计划统计", response_model=ResponseStatisResult)
async def get_ws_plan_statics(plan_id: int, user=Depends(Permission())):
    pass


@wst.get("/plan/{plan_id}/result", summary="获取测试计划结果", response_model=ResponseWsCaseResult)
async def get_ws_plan_result(plan_id: int, user=Depends(Permission())):
    pass


@wst.post("/plan/{plan_id}/result/mark", summary="标记用例情况", response_model=CommonResponse)
async def mark_ws_plan_result(plan_id: int, data: RequestMarkCase, user=Depends(Permission())):
    pass


@wst.post("/plan/{plan_id}/result/done", summary="提交测试计划", response_model=CommonResponse)
async def done_ws_plan_result(plan_id: int, user=Depends(Permission())):
    pass


@wst.post(
    "/plan/{plan_id}/test/connect",
)
async def test_connect(plan_id: int, form: RequestTestConnect, user=Depends(Permission())):
    w = WsTestService(
        ws_url=form.ws_url,
        operator=user["user_id"],
    )
    asyncio.create_task(w.start_listener())
    ws_plan[str(plan_id)] = w
    if w.current_ws_obj[w.ws_url[-5:]]["status"]:
        return C137Response.success(data={"status": 1})
    else:
        return C137Response.failed("连接失败")


@wst.get(
    "/plan/{plan_id}/test/disconnect",
)
async def test_disconnect(plan_id: int, user=Depends(Permission())):
    w = ws_plan.get(str(plan_id))
    if w:
        await ws_plan[str(plan_id)].disconnect()
        if w.current_ws_obj[w.ws_url[-5:]]["status"]:
            return C137Response.failed("断开失败")
        del ws_plan[str(plan_id)]
        return C137Response.success()


@wst.post("/plan/{plan_id}/test/run_case")
async def test_run_case(plan_id: int, form: RequestTestRunCase, user=Depends(Permission())):
    w = ws_plan.get(str(plan_id))
    if w:
        await ws_plan[str(plan_id)].add_case(form.case_id)
        return C137Response.success()
    else:
        return C137Response.failed("未连接")
