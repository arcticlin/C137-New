# coding=utf-8
"""
File: directory_router.py
Author: bot
Created: 2023/10/20
Description:
"""
from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response
from app.middleware.access_permission import Permission
from app.services.directory.directory_service import DirectoryService
from app.services.directory.schema.dir_new import (
    ResponseDirectoryNew,
    DirectoryNew,
    DirectoryUpdate,
    ResponseDirectoryList,
    ResponseDirectoryCaseList,
)

directory = APIRouter()


@directory.post("/add", summary="创建项目目录", response_model=ResponseDirectoryNew)
async def add_project_dir(data: DirectoryNew, user_info=Depends(Permission())):
    directory_id = await DirectoryService.add_project_dir(data, user_info["user_id"])
    return C137Response.success(data={"directory_id": directory_id})


@directory.delete("/delete/{directory_id}", summary="删除项目目录", response_model=CommonResponse)
async def deleted_dir_new(directory_id: int, user_info=Depends(Permission())):
    await DirectoryService.delete_directory_new(directory_id, user_info["user_id"])
    return C137Response.success(message="删除成功")


@directory.put("/update", summary="更新目录名", response_model=CommonResponse)
async def update_directory_name(data: DirectoryUpdate, user=Depends(Permission())):
    await DirectoryService.update_project_dir_name(data.project_id, data.directory_id, data.name, user["user_id"])
    return C137Response.success(message="更新成功")


@directory.get("/tree", summary="获取项目目录树", response_model=ResponseDirectoryList)
async def get_project_dir_tree(project_id: int = Query(..., description="项目ID")):
    result = await DirectoryService.get_project_directory_tree(project_id)
    return C137Response.success(data=result)


@directory.get("/case_list/{directory_id}", summary="获取目录下的用例列表", response_model=ResponseDirectoryCaseList)
async def get_case_list_in_directory(directory_id: int):
    case_list = await DirectoryService.get_case_list_in_directory(directory_id)
    return C137Response.success(data=case_list)
