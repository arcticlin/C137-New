# coding=utf-8
"""
File: vips_router.py
Author: bot
Created: 2023/7/26
Description:
"""
from fastapi import APIRouter, Depends, Query
from app.middleware.flyele_token import FlyeleToken
from app.services.flyele.flyele_services import FlyeleServices

vip = APIRouter()


@vip.get("/person", summary="添加个人会员")
async def add_vip(
    phone: str = Query(..., description="手机号"),
    days: int = Query(10, description="添加天数, 9999是永久会员"),
    headers=Depends(FlyeleToken()),
):
    """
    添加个人会员
    """
    user_ids = await FlyeleServices.get_user_id_by_python(phone, headers)
    await FlyeleServices.add_person_vip(user_ids, days, headers)
    return {"message": "操作成功"}


@vip.get("/team", summary="添加团队会员")
async def add_team_vip(
    phone: str = Query(..., description="手机号"),
    days: int = Query(10, description="添加天数"),
    headers=Depends(FlyeleToken()),
):
    user_ids = await FlyeleServices.get_user_id_by_python(phone, headers)
    await FlyeleServices.add_team_vip(user_ids, days, headers)
    return {"message": "操作成功"}


@vip.get("/expired", summary="过期会员")
async def expire_to_person(
    phone: str = Query(..., description="手机号"),
    types: int = Query(..., description="过期类型, 0: 过期成为非会员, 1: 过期成为个人会员(需存在团队会员)"),
    headers=Depends(FlyeleToken()),
):
    user_ids = await FlyeleServices.get_user_id_by_python(phone, headers)
    await FlyeleServices.expire_to_person(user_ids, types, headers)
    return {"message": "操作成功"}


@vip.get("/clear", summary="清除会员信息 *执行后账号状态为从未领取过会员")
async def clear_vip(
    phone: str = Query(..., description="手机号"),
    headers=Depends(FlyeleToken()),
):
    user_ids = await FlyeleServices.get_user_id_by_python(phone, headers)
    await FlyeleServices.clear_vip(user_ids, headers)
    return {"message": "操作成功"}
