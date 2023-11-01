# coding=utf-8
"""
File: project_info.py
Author: bot
Created: 2023/10/18
Description:
"""
from typing import List

from pydantic import BaseModel, Field, validator
from app.core.basic_schema import CommonResponse


class ProjectInfoOut(BaseModel):
    project_id: int = Field(..., title="项目id")
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")
    create_user: int = Field(..., title="创建人")
    updated_at: int = Field(..., title="更新时间")
    created_at: int = Field(..., title="创建时间")
    total_case: int = Field(0, title="用例数量")
    new_case_today: int = Field(0, title="今日新增")
    members: int = Field(0, title="成员数量")


class ResponseProjectList(CommonResponse):
    data: List[ProjectInfoOut] = Field(..., title="项目列表")


class ResponseProjectDetail(CommonResponse):
    data: ProjectInfoOut = Field(..., title="项目详情")
