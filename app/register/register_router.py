# coding=utf-8
"""
File: register_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import APIRouter, FastAPI

from app.router.auth.auth_router import auth
from app.router.project.project_router import project
from app.router.admin.admin import admin
from app.router.users.user_center import uc


def register_router(app: FastAPI):
    app.include_router(auth, prefix="/auth", tags=["用户中心"])
    app.include_router(project, prefix="/project", tags=["项目"])
    app.include_router(admin, prefix="/admin", tags=["管理员"])
    app.include_router(uc, prefix="/userc", tags=["用户中心"])
