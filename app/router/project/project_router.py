# coding=utf-8
"""
File: project_router.py
Author: bot
Created: 2023/7/28
Description:
"""


from fastapi import APIRouter
from app.crud.project.project_crud import ProjectCrud

project = APIRouter()


@project.get("/project")
async def get_project():
    await ProjectCrud.query_project(1)


@project.get("/projects")
async def get_projects():
    await ProjectCrud.query_projects(1)
