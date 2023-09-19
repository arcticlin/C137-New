# coding=utf-8
"""
File: register_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import APIRouter, FastAPI

from app.router.auth.auth_router import auth
from app.router.project.project_router import project, directory
from app.router.admin.admin import admin
from app.router.users.user_center import uc
from app.router.api_case.api_case_router import case

from app.router.common_config.config_router import cconfig
from app.router.ws.ws import ws


def register_router(app: FastAPI):
    app.include_router(ws, prefix="/ws", tags=["websocket"])
    app.include_router(auth, prefix="/auth", tags=["用户中心"])
    app.include_router(project, prefix="/project", tags=["项目"])
    app.include_router(directory, prefix="/directory", tags=["目录"])
    app.include_router(admin, prefix="/admin", tags=["管理员"])
    app.include_router(uc, prefix="/userc", tags=["用户中心"])
    app.include_router(case, prefix="/apicase", tags=["接口测试"])
    app.include_router(cconfig, prefix="/config", tags=["配置中心"])
