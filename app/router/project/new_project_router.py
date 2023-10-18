# coding=utf-8
"""
File: new_project_router.py
Author: bot
Created: 2023/10/18
Description:
"""
from fastapi import APIRouter, Depends, Query

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.project.new_project_service import ProjectService
from app.services.project.schema.project_info import ResponseProjectList, ResponseProjectDetail
from app.services.project.schema.project_member import (
    ResponseProjectMember,
    ProjectAddMemberRequest,
    ProjectAssignMemberRequest,
)
from app.services.project.schema.project_new import ResponseProjectNew, ProjectNewRequest
from app.services.project.schema.project_update import ProjectUpdateRequest

project = APIRouter()


@project.get("/list", summary="获取项目列表, 我创建+我参与的+公开的", response_model=ResponseProjectList)
async def get_project_list():
    return {"code": 0, "message": "success", "data": []}


@project.post("/new", summary="创建项目", response_model=ResponseProjectNew)
async def new_project(data: ProjectNewRequest, user_info=Depends(Permission())):
    project_id = await ProjectService.add_project(data, user_info["user_id"])
    return C137Response.success(data={"project_id": project_id})


@project.put("/{project_id}/update", summary="更新项目", response_model=CommonResponse)
async def update_project(project_id: int, data: ProjectUpdateRequest, user_info=Depends(Permission())):
    await ProjectService.update_project(project_id, data, operator=user_info["user_id"])
    return C137Response.success(message="更新成功")


@project.get("/{project_id}/detail", summary="获取项目详情", response_model=ResponseProjectDetail)
async def get_project_detail(project_id: int, user_info=Depends(Permission())):
    data = await ProjectService.get_project_detail(project_id, user_info["user_id"])
    return C137Response.success(data=data)


@project.get("/{project_id}/members", summary="获取项目成员", response_model=ResponseProjectMember)
async def get_project_members(project_id: int):
    members = await ProjectService.get_project_members(project_id)
    return C137Response.success(data=members)


@project.delete("/{project_id}/delete", summary="删除项目", response_model=CommonResponse)
async def new_project(project_id: int, user_info=Depends(Permission())):
    await ProjectService.delete_project(project_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


@project.post("/{project_id}/member/add", summary="添加成员", response_model=CommonResponse)
async def add_member(project_id: int, data: ProjectAddMemberRequest, user_info=Depends(Permission())):
    await ProjectService.add_member(project_id, data.user_id, data.role, operator=user_info["user_id"])
    return C137Response.success(message="添加成功")


@project.delete("/{project_id}/member/delete/{user_id}", summary="移出成员", response_model=CommonResponse)
async def remove_member(project_id: int, user_id: int, user_info=Depends(Permission())):
    await ProjectService.remove_member(project_id, user_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


#
# @project.put("/{project_id}/member/update", summary="更新成员权限", response_model=CommonResponse)
# async def update_member_role(project_id: int, data: ProjectAssignMemberRequest, user_info=Depends(Permission())):
#     await ProjectService.update_member(project_id, data.user_id, data.role, operator=user_info["user_id"])
#     return C137Response.success(message="更新成功")
#
#
# @project.put("/{project_id}/member/quit", summary="退出项目", response_model=CommonResponse)
# async def exit_project(project_id: int, user_info=Depends(Permission())):
#     await ProjectService.member_exit(project_id, user_info["user_id"])
#     return C137Response.success(message="退出成功")
