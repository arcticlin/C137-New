# coding=utf-8
"""
File: news.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field
from app.core.basic_schema import CommonResponse


class RequestScriptAdd(BaseModel):
    name: str = Field(..., description="脚本配置名称", max_length=16)
    description: str = Field(None, description="脚本配置描述", max_length=64)
    tag: str = Field(None, description="脚本配置标签", max_length=16)
    var_key: str = Field(..., description="脚本配置调用键", max_length=16)
    var_script: str = Field(..., description="脚本配置脚本", max_length=1024)
    public: bool = Field(..., description="脚本配置是否公开")


class ScriptAddOut(BaseModel):
    script_id: int = Field(..., description="SCRIPT_ID")


class RequestScriptDebugByForm(BaseModel):
    var_key: str = Field(..., description="脚本配置调用键", max_length=16)
    var_script: str = Field(..., description="脚本配置脚本", max_length=1024)
