# coding=utf-8
"""
File: ws_test.py
Author: bot
Created: 2023/11/20
Description:
"""
from fastapi import APIRouter, Query, Depends

from app.core.basic_schema import CommonResponse
from app.middleware.access_permission import Permission
from app.services.ws_test.schema.ws_code.info import ResponseWsCodeList, ResponseWsCodeDetail
from app.services.ws_test.schema.ws_code.new import ResponseAddWsCode, RequestAddWsCode

wst = APIRouter()


@wst.get("/ws_test/list", summary="获取项目的WS_CODE列表", response_model=ResponseWsCodeList)
async def query_code_list(project_id: int = Query(..., description="项目ID")):
    """
    获取项目的WS_CODE列表
    :param project_id: 项目ID
    :return:
    """
    # return await WsCodeService.query_code_list(project_id)


@wst.post("/ws_test/add", summary="添加WS_CODE", response_model=ResponseAddWsCode)
async def add_ws_code(data: RequestAddWsCode, user=Depends(Permission())):
    """
    添加WS_CODE
    :param data: WS_CODE信息
    :return:
    """
    # return await WsCodeService.add_ws_code(data


@wst.get("/ws_test/{ws_id}/detail", summary="获取WS_CODE详情", response_model=ResponseWsCodeDetail)
async def query_code_detail(ws_id: int):
    """
    获取WS_CODE详情
    :param ws_id: WS_CODE ID
    :return:
    """
    # return await WsCodeService.query_code_detail(ws_id)


@wst.put("/ws_test/{ws_id}/update", summary="修改WS_CODE详情", response_model=CommonResponse)
async def query_code_detail(ws_id: int):
    """
    获取WS_CODE详情
    :param ws_id: WS_CODE ID
    :return:
    """
    # return await WsCodeService.query_code_detail(ws_id)
