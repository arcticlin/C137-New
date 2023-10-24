# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/10/24
Description:
"""
from pydantic import BaseModel, Field


class RequestScriptUpdate(BaseModel):
    name: str = Field(None, description="脚本配置名称", max_length=16)
    description: str = Field(None, description="脚本配置描述", max_length=64)
    tag: str = Field(None, description="脚本配置标签", max_length=16)
    var_key: str = Field(None, description="脚本配置调用键", max_length=16)
    var_script: str = Field(None, description="脚本配置脚本", max_length=1024)
    public: bool = Field(None, description="脚本配置是否公开")
