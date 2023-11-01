# coding=utf-8
"""
File: project_new.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field, validator
from app.core.basic_schema import CommonResponse


class ProjectNewRequest(BaseModel):
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


class ProjectNewOut(BaseModel):
    project_id: int = Field(..., title="项目id")


class ResponseProjectNew(CommonResponse):
    data: ProjectNewOut = Field(..., title="项目id")
