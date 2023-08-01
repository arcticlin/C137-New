# coding=utf-8
"""
File: project_router.py
Author: bot
Created: 2023/7/28
Description:
"""


from fastapi import APIRouter, Depends, Query
from app.crud.project.project_crud import ProjectCrud
from app.crud.project.project_directory_crud import PDirectoryCrud
from app.handler.response_handler import C137Response
from app.schemas.project.pd_schema import AddPDirectoryRequest, DeletePDirectoryRequest
from app.schemas.project.project_schema import *
from app.middleware.access_permission import Permission
from app.services.project.project_service import ProjectService


project = APIRouter()


@project.get("/list", summary="获取项目列表, 我创建+我参与的+公开的", response_model=ProjectListResponse)
async def get_project_list(user_info=Depends(Permission())):
    result = await ProjectCrud.get_project_list(user_id=user_info["user_id"])
    return C137Response.success(data=result)


@project.post("/new", summary="创建项目", response_model=CommonResponse)
async def new_project(data: AddProjectRequest, user_info=Depends(Permission())):
    await ProjectCrud.add_project(data, user_info["user_id"])
    return C137Response.success(message="创建成功")


@project.delete("/{project_id}/delete", summary="删除项目", response_model=CommonResponse)
async def new_project(project_id: int, user_info=Depends(Permission())):
    await ProjectService.delete_project(project_id, operator=user_info["user_id"])
    return C137Response.success(message="删除成功")


@project.put("/{project_id}/update", summary="更新项目", response_model=CommonResponse)
async def update_project(project_id: int, data: UpdateProjectRequest, user_info=Depends(Permission())):
    await ProjectService.update_project(project_id, data, operator=user_info["user_id"])
    return C137Response.success(message="更新成功")


@project.post("/{project_id}/member/add", summary="添加成员", response_model=CommonResponse)
async def add_member(project_id: int, data: AddProjectMemberRequest, user_info=Depends(Permission())):
    await ProjectService.add_project_member(project_id, data, operator=user_info["user_id"])
    return C137Response.success(message="添加成功")


@project.get("/detail/{project_id}", summary="获取项目详情", response_model=ProjectDetailResponse)
async def get_project_detail(project_id: int):
    data = await ProjectService.get_project_detail(project_id)
    return C137Response.success(data=data)


@project.get("{project_id}/directory", summary="获取项目目录树")
async def get_project_dir_tree(project_id: int, directory: int = Query(None, description="目录id, 为空则查询根目录")):
    # data = await ProjectService.get_project_dir(project_id, directory)
    # return C137Response.success(data=data)
    data = await PDirectoryCrud.get_descendant_ids(directory)


@project.post("{project_id}/directory/new", summary="创建项目目录")
async def add_project_dir(project_id: int, data: AddPDirectoryRequest, user_info=Depends(Permission())):
    await ProjectService.add_project_dir(project_id, data, user_info["user_id"])
    return C137Response.success(message="创建成功")


# @project.post("{project_id}/directory/delete", summary="删除项目目录")
# async def deleted_dir(project_id: int, data: DeletePDirectoryRequest, user_info=Depends(Permission())):
#     await ProjectService.delete_project_dir(project_id, data, user_info["user_id"])
#     return C137Response.success(message="删除成功"
