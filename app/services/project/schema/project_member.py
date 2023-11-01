# coding=utf-8
"""
File: project_member.py
Author: bot
Created: 2023/10/18
Description:
"""
from pydantic import BaseModel, Field, validator
from app.core.basic_schema import CommonResponse
from typing import List


class ProjectAddMemberRequest(BaseModel):
    """添加项目成员Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")


class ProjectAssignMemberRequest(BaseModel):
    """添加项目成员Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")


class ProjectMemberOut(BaseModel):
    """项目成员展示Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")
    create_user: int = Field(..., title="创建人")
    created_at: int = Field(..., title="创建时间")


class ResponseProjectMember(CommonResponse):
    data: List[ProjectMemberOut] = Field(..., title="项目成员")
