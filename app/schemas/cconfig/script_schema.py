# coding=utf-8
"""
File: script_schema.py
Author: bot
Created: 2023/8/4
Description:
"""
from pydantic import BaseModel, Field
from app.schemas.response_schema import CommonResponse


class AddScriptRequest(BaseModel):

    name: str = Field(..., description="脚本配置名称", max_length=16)
    description: str = Field(None, description="脚本配置描述", max_length=64)
    tag: str = Field(None, description="脚本配置标签", max_length=16)
    var_key: str = Field(..., description="脚本配置调用键", max_length=16)
    var_script: str = Field(..., description="脚本配置脚本", max_length=1024)
    public: bool = Field(..., description="脚本配置是否公开")


class DebugScript(BaseModel):
    script_id: int


class UpdateScriptRequest(BaseModel):
    name: str = Field(None, description="脚本配置名称", max_length=16)
    description: str = Field(None, description="脚本配置描述", max_length=64)
    tag: str = Field(None, description="脚本配置标签", max_length=16)
    var_key: str = Field(None, description="脚本配置调用键", max_length=16)
    var_script: str = Field(None, description="脚本配置脚本", max_length=1024)
    public: bool = Field(None, description="脚本配置是否公开")


class ScriptDetailSHow(BaseModel):
    script_id: int = Field(..., description="脚本配置ID")
    name: str = Field(..., description="脚本配置名称")
    description: str = Field(None, description="脚本配置描述")
    tag: str = Field(None, description="脚本配置标签")
    var_key: str = Field(..., description="脚本配置调用键")
    var_script: str = Field(..., description="脚本配置脚本")
    public: bool = Field(..., description="脚本配置是否公开")
    create_user: int = Field(..., description="创建人")