# coding=utf-8
"""
File: project_router.py
Author: bot
Created: 2023/7/28
Description:
"""


from fastapi import APIRouter, Depends
from app.crud.project.project_crud import ProjectCrud
from app.handler.response_handler import C137Response
from app.schemas.project.project_schema import *
from app.middleware.access_permission import Permission
from app.services.project.project_service import ProjectService

project = APIRouter()


@project.get(
    "/project/list", summary="获取项目列表, 我创建+我参与的+公开的", response_model=ProjectListResponse
)
async def get_project_list(user_info=Depends(Permission())):
    result = await ProjectCrud.get_project_list(user_id=user_info["user_id"])
    return C137Response.success(data=result)


#
#
# @project.get("/project/{project_id}/detail")
# async def get_project_detail(project_id: int):
#     await ProjectCrud.get_project_detail(project_id)
#


@project.post("/project/new")
async def new_project(data: AddProjectRequest, user_info=Depends(Permission())):
    await ProjectCrud.add_project(data, user_info["user_id"])
    return C137Response.success(message="创建成功")


@project.delete("/project/{project_id}/delete")
async def new_project(project_id: int, user_info=Depends(Permission())):
    await ProjectService.delete_project(project_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


@project.put("/project/{project_id}/update", summary="更新项目")
async def update_project(
    project_id: int, data: UpdateProjectRequest, user_info=Depends(Permission())
):
    await ProjectService.update_project(project_id, data, operator=user_info["user_id"])
    return C137Response.success(message="更新成功")


# @project.post("/project/{project_id}/member/add")
# async def add_member(project_id: int, data: AddMemberRequest):
#     pass
