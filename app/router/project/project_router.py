# coding=utf-8
"""
File: project_router.py
Author: bot
Created: 2023/7/28
Description:
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from app.crud.project.project_crud import ProjectCrud
from app.crud.project.project_directory_crud import PDirectoryCrud
from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest, DeletePDirectoryRequest, UpdatePDirectoryRequest
from app.schemas.project.project_schema import *
from app.schemas.api_case.api_case_schema import ApiCaseListResponse
from app.middleware.access_permission import Permission
from app.services.project.project_service import ProjectService
from app.utils.new_logger import logger


project = APIRouter()
directory = APIRouter()


@project.get("/list", summary="获取项目列表, 我创建+我参与的+公开的", response_model=ProjectListResponse)
async def get_project_list(user_info=Depends(Permission())):
    result = await ProjectService.get_project_list(user_id=user_info["user_id"])
    return C137Response.success(data=result)


@project.post("/new", summary="创建项目", response_model=ProjectCreateResponse)
async def new_project(data: AddProjectRequest, user_info=Depends(Permission())):
    project_id = await ProjectService.add_project(data, user_info["user_id"])
    return C137Response.success(data={"project_id": project_id}, message="创建成功")


@project.put("/update", summary="更新项目", response_model=CommonResponse)
async def update_project(data: UpdateProjectRequest, user_info=Depends(Permission())):
    await ProjectService.update_project(data, operator=user_info["user_id"])
    return C137Response.success(message="更新成功")


@project.get("/{project_id}/detail", summary="获取项目详情", response_model=ProjectDetailResponse)
async def get_project_detail(project_id: int, user_info=Depends(Permission())):
    data = await ProjectService.get_project_detail(project_id, user_info["user_id"])
    return C137Response.success(data=data)


@project.get("/{project_id}/members", summary="获取项目成员", response_model=ProjectMemberResponse)
async def get_project_members(project_id: int):
    members = await ProjectService.get_project_members(project_id)
    return C137Response.success(data=members)


@project.delete("/{project_id}/delete", summary="删除项目", response_model=CommonResponse)
async def new_project(project_id: int, user_info=Depends(Permission())):
    await ProjectService.delete_project(project_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


@project.post("/{project_id}/member/add", summary="添加成员", response_model=CommonResponse)
async def add_member(project_id: int, data: AddProjectMemberRequest, user_info=Depends(Permission())):
    await ProjectService.add_member(project_id, data.user_id, data.role, operator=user_info["user_id"])
    return C137Response.success(message="添加成功")


@project.delete("/{project_id}/member/delete/{user_id}", summary="移出成员", response_model=CommonResponse)
async def remove_member(project_id: int, user_id: int, user_info=Depends(Permission())):
    await ProjectService.remove_member(project_id, user_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


@project.put("/{project_id}/member/update", summary="更新成员权限", response_model=CommonResponse)
async def update_member_role(project_id: int, data: UpdatePMRequest, user_info=Depends(Permission())):
    await ProjectService.update_member(project_id, data.user_id, data.role, operator=user_info["user_id"])
    return C137Response.success(message="更新成功")


@project.put("/{project_id}/member/quit", summary="退出项目", response_model=CommonResponse)
async def exit_project(project_id: int, user_info=Depends(Permission())):
    await ProjectService.member_exit(project_id, user_info["user_id"])
    return C137Response.success(message="退出成功")


@directory.post("/add", summary="创建项目目录", response_model=CommonResponse)
async def add_project_dir(data: AddPDirectoryRequest, user_info=Depends(Permission())):
    await ProjectService.add_project_dir(data, user_info["user_id"])
    return C137Response.success(message="创建成功")


@directory.delete("/delete/{directory_id}", summary="删除项目目录")
async def deleted_dir_new(directory_id: int, user_info=Depends(Permission())):
    await ProjectService.delete_directory_new(directory_id, user_info["user_id"])
    return C137Response.success(message="删除成功")


@directory.put("/update", summary="更新目录名", response_model=CommonResponse)
async def update_directory_name(data: UpdatePDirectoryRequest, user=Depends(Permission())):
    await ProjectService.update_project_directory_name(data.directory_id, data.name, user["user_id"])
    return C137Response.success(message="更新成功")


@directory.get("/tree/{project_id}", summary="获取项目目录树")
async def get_project_dir_tree(project_id: int):
    result = await ProjectService.get_project_directory_tree(project_id)
    return C137Response.success(data=result)


@directory.get("/case_list/{directory_id}", summary="获取目录下的用例列表", response_model=ApiCaseListResponse)
async def get_case_list_in_directory(directory_id: int):
    case_list = await ProjectService.get_case_list_in_directory(directory_id)
    return C137Response.success(data=case_list)
