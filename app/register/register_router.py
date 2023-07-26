# coding=utf-8
"""
File: register_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import APIRouter, FastAPI

from app.router.vip.vips_router import vip
from app.router.statistics.statistics import statistics


def register_router(app: FastAPI):
    app.include_router(vip, prefix="/vip", tags=["会员权益"])
    app.include_router(statistics, prefix="/statistics", tags=["统计数据推送"])
