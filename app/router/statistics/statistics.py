# coding=utf-8
"""
File: statistics.py
Author: bot
Created: 2023/7/26
Description:
"""
from fastapi import APIRouter, Depends, Query


from app.middleware.flyele_token import FlyeleToken
from app.services.flyele.flyele_services import FlyeleServices


statistics = APIRouter()


@statistics.get("/push", summary="调用后端推送")
async def backend_push(
    phone: str = Query(..., description="手机号"),
    headers=Depends(FlyeleToken()),
):
    await FlyeleServices.push_statistics(phone, headers)
    return {"message": "操作成功"}
