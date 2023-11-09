# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field


class ScriptListOut(BaseModel):
    script_id: int = Field(..., description="脚本配置ID")
    name: str = Field(..., description="脚本配置名称")
    tag: str = Field(None, description="脚本配置标签")
    var_key: str = Field(..., description="脚本配置调用键")
    create_user: int = Field(..., description="创建人")
    public: bool = Field(..., description="脚本配置是否公开")


class ScriptDetailOut(BaseModel):
    script_id: int = Field(..., description="脚本配置ID")
    name: str = Field(..., description="脚本配置名称")
    description: str = Field(None, description="脚本配置描述")
    tag: str = Field(None, description="脚本配置标签")
    var_key: str = Field(..., description="脚本配置调用键")
    var_script: str = Field(..., description="脚本配置脚本")
    public: bool = Field(..., description="脚本配置是否公开")
    create_user: int = Field(..., description="创建人")
