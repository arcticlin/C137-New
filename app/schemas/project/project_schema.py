from typing import List

from pydantic import BaseModel, Field

from app.schemas.response_schema import CommonResponse
from app.enums.enum_project import ProjectRoleEnum


class ProjectBaseSchema(BaseModel):
    project_id: int = Field(..., title="项目id")
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")
    created_at: int = Field(..., title="创建时间")


class AddProjectRequest(BaseModel):
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


class UpdateProjectRequest(BaseModel):
    project_name: str = Field(None, title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(None, title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


class AddProjectMemberRequest(BaseModel):
    user_id: int = Field(..., title="用户id")
    role: ProjectRoleEnum = Field(..., title="角色")


class ProjectMemberShow(BaseModel):
    user_id: int = Field(..., title="用户id")
    role: ProjectRoleEnum = Field(..., title="角色")
    create_user: int = Field(..., title="创建人")
    created_at: int = Field(..., title="创建时间")


class ProjectDetailShow(BaseModel):
    project_info: ProjectBaseSchema = Field(..., title="项目信息")
    project_member: List[ProjectMemberShow] = Field(..., title="项目成员")


class ProjectListShow(BaseModel):
    project_id: int = Field(..., title="项目id")
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")
    create_user: int = Field(..., title="创建人")
    updated_at: int = Field(..., title="更新时间")
    created_at: int = Field(..., title="创建时间")


class ProjectListResponse(CommonResponse):
    data: List[ProjectListShow] = Field(..., title="项目列表")


class ProjectDetailResponse(CommonResponse):
    data: ProjectDetailShow = Field(..., title="项目详情")
