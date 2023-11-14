# coding=utf-8
"""
File: dir_new.py
Author: bot
Created: 2023/10/20
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.core.basic_schema import CommonResponse


class DirectoryNew(BaseModel):
    project_id: int = Field(..., description="关联项目ID")
    name: str = Field(..., description="目录名")
    parent_id: int = None


class DirectoryUpdate(BaseModel):
    project_id: int = Field(..., description="关联项目ID")
    name: str = Field(..., description="目录名")


class DirectoryNewOut(BaseModel):
    directory_id: int = Field(..., description="目录ID")


class DirectoryOut(BaseModel):
    directory_id: int = Field(..., description="目录ID")
    project_id: int = Field(..., description="项目ID")
    name: str = Field(..., description="目录名")
    parent_id: int = None
    has_case: int = Field(..., description="是否存在子目录")
    children: List["DirectoryOut"] = []


class DirectoryCaseListOut(BaseModel):
    case_id: int = Field(..., description="用例ID")
    name: str = Field(..., description="用例名")
    method: str = Field(..., description="请求方法")
    priority: str = Field(..., description="优先级")
    status: int = Field(..., description="用例状态")
    create_user: int = Field(..., description="创建人")
    updated_at: int = Field(..., description="更新时间")


class ResponseDirectoryNew(CommonResponse):
    data: DirectoryNewOut


class ResponseDirectoryList(CommonResponse):
    data: List[DirectoryOut]


class ResponseDirectoryCaseList(CommonResponse):
    data: List[DirectoryCaseListOut]
