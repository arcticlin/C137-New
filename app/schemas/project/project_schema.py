from typing import List

from pydantic import BaseModel, Field

from app.schemas.response_schema import CommonResponse


class ProjectBaseSchema(BaseModel):
    project_id: int = Field(..., title="项目id")
    project_name: str = Field(..., title="项目名称")
    project_desc: str = Field(None, title="项目描述")
    public: bool = Field(..., title="是否公开")
    project_avatar: str = Field(None, title="项目头像")


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