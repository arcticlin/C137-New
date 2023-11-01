# coding=utf-8
"""
File: register_router.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import FastAPI

from app.router.auth.auth_router import auth
from app.router.project.project_router import project
from app.router.user.user import user
from app.router.oss.oss import oss

from app.router.project.directory_router import directory
from app.router.admin.admin import admin

from app.router.ws.ws import ws
from app.router.jobs.jobs import jobs
from app.router.common_config.env.env import envs
from app.router.common_config.redis.redis_router import rds_router
from app.router.common_config.sql.sql_router import sql_router
from app.router.common_config.script.script_router import script_router
from app.router.api_case.api_case import cases


def register_router(app: FastAPI):
    app.include_router(ws)
    app.include_router(auth, prefix="/auth", tags=["账号管理"])
    app.include_router(user, prefix="/user", tags=["用户中心"])
    app.include_router(admin, prefix="/admin", tags=["管理员"])
    app.include_router(jobs, prefix="/jobs", tags=["定时任务"])
    app.include_router(project, prefix="/project", tags=["项目"])
    app.include_router(directory, prefix="/directory", tags=["目录"])
    app.include_router(cases, prefix="/api_case", tags=["接口测试"])
    app.include_router(envs, prefix="/config", tags=["配置信息"])
    app.include_router(rds_router, prefix="/config", tags=["配置信息"])
    app.include_router(sql_router, prefix="/config", tags=["配置信息"])
    app.include_router(script_router, prefix="/config", tags=["配置信息"])
    app.include_router(oss, prefix="/oss", tags=["oss"])
