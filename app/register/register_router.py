# coding=utf-8
"""
File: register_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import APIRouter, FastAPI
from app.router.auth.auth_router import auth


def register_router(app: FastAPI):
    app.include_router(auth, prefix="/auth", tags=["用户中心"])
