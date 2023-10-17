from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel, Field, validator

from app.schemas.response_schema import CommonResponse


class ProjectBaseSchema(BaseModel):
    """项目基本Schema"""

    project_id: int = Field(..., title="项目id")
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")
    created_at: int = Field(..., title="创建时间")


class AddProjectRequest(BaseModel):
    """添加项目Schema"""

    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


class UpdateProjectRequest(BaseModel):
    """更新项目Schema"""

    project_id: int
    project_name: str = Field(None, title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(None, title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


class AddProjectMemberRequest(BaseModel):
    """添加项目成员Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")


class UpdatePMRequest(BaseModel):
    """添加项目成员Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")


class ProjectMemberShow(BaseModel):
    """项目成员展示Schema"""

    user_id: int = Field(..., title="用户id")
    role: int = Field(..., title="角色")
    create_user: int = Field(..., title="创建人")
    created_at: int = Field(..., title="创建时间")


class ProjectListShow(BaseModel):
    """项目列表展示Schema"""

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


class ProjectListResponse(CommonResponse):
    """项目列表响应Schema"""

    data: List[ProjectListShow] = Field(..., title="项目列表")


class ProjectDetailResponse(CommonResponse):
    """项目详情响应Schema"""

    data: ProjectBaseSchema = Field(..., title="项目详情")


class ProjectMemberResponse(CommonResponse):
    data: List[ProjectMemberShow] = Field(..., title="项目成员列表")


class ProjectCreateShow(BaseModel):
    project_id: int = Field(..., title="项目id")


class ProjectCreateResponse(CommonResponse):
    data: ProjectCreateShow = Field(..., title="项目创建返回")
