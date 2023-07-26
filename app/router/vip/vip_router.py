# coding=utf-8
"""
File: vip_router.py
Author: bot
Created: 2023/7/26
Description:
"""


from datetime import datetime, timedelta

from fastapi import FastAPI, Body, Query
import requests

# from login_module import LoginModule
from pydantic import BaseModel, Field


class AddVip(BaseModel):
    phone: str = Field(..., description="手机号")
    days: str = Field(..., description="添加天数, 9999为永久")


class AddTeamVip(BaseModel):
    phone: str = Field(..., description="手机号")
    days: int = Field(..., description="添加天数,不可为9999")


class ExpiredVip(BaseModel):
    phone: str = Field(..., description="手机号")
    types: int = Field(..., description="过期类型, 0: 过期成为非会员, 1: 过期成为个人会员(需存在团队会员)")


class ClearVip(BaseModel):
    phone: str = Field(..., description="手机号")


def expired_now():
    now = datetime.now()
    ago_five = now - timedelta(minutes=5)
    return int(ago_five.timestamp())


def format_output(code: int, reason=None):
    if code == 1:
        return {"message": "操作成功"}
    else:
        return {"message": "操作失败", "reason": reason}


DOMAIN = "https://api-test.flyele.vip"

app = FastAPI(title="测试组")


@app.post("/vip/person", summary="添加个人会员")
async def add_vip(
    phone: str = Query(..., description="手机号"),
    days: int = Query(10, description="添加天数, 9999是永久会员"),
):
    token, user_id = LoginModule.login(phone)
    if user_id is None:
        return format_output(0, token)
    url = f"{DOMAIN}/userc/v2/member/backend"
    data = {"user_ids": [user_id], "duration": days, "vip_type": 1}
    response = requests.post(url=url, json=data, headers=token)
    if response.status_code != 200:
        print(f"添加个人会员-{days}失败: {phone}, {response.text}")
        return format_output(0, response.text)
    else:
        print(f"添加个人会员-{days}成功: {phone}")
        return format_output(1)


@app.post("/vip/team", summary="添加团队会员")
async def add_team_vip(
    phone: str = Query(..., description="手机号"),
    days: int = Query(10, description="添加天数"),
):
    token, user_id = LoginModule.login(phone)
    if user_id is None:
        return format_output(0, token)
    url = f"{DOMAIN}/userc/v2/member/backend"
    data = {"user_ids": [user_id], "duration": days, "vip_type": 2}
    response = requests.post(url=url, json=data, headers=token)
    if response.status_code != 200:
        print(f"添加团队会员-{days}失败: {phone}, {response.text}")
        return format_output(0, response.text)
    else:
        print(f"添加团队会员-{days}成功: {phone}")
        return format_output(1)


@app.post("/vip/expire", summary="过期会员")
async def expire_to_person(
    phone: str = Query(..., description="手机号"),
    types: int = Query(..., description="过期类型, 0: 过期成为非会员, 1: 过期成为个人会员(需存在团队会员)"),
):
    token, user_id = LoginModule.login(phone)
    if user_id is None:
        return format_output(0, token)
    url = f"{DOMAIN}/userc/v2/member/clear"
    data = {
        "expire_at": expired_now(),
        "expire_type": types,
        "is_clear_bind": 2,
        "operate_type": "expire",
        "user_id": [user_id],
    }
    response = requests.post(url=url, json=data, headers=token)
    if response.status_code != 200:
        print(f"过期会员失败: {phone}, {response.text}")
        return format_output(0, response.text)
    else:
        print(f"过期会员成功: {phone}")
        return format_output(1)


@app.post("/vip/clear", summary="清除会员信息 *执行后账号状态为从未领取过会员")
async def clear_vip(phone: str = Query(..., description="手机号")):
    token, user_id = LoginModule.login(phone)
    if user_id is None:
        return format_output(0, token)
    url = f"{DOMAIN}/userc/v2/member/clear"
    data = {"user_id": [user_id], "operate_type": "delete", "is_clear_bind": 1}
    response = requests.post(url=url, json=data, headers=token)
    if response.status_code != 200:
        print(f"清除会员失败: {phone}, {response.text}")
        return format_output(0, response.text)
    else:
        print(f"清除会员成功: {phone}")
        return format_output(1)
