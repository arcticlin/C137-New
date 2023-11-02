# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/10/25
Description:
"""
from pydantic import BaseModel, Field


class AddWithExtractInfo(BaseModel):
    name: str = Field(..., description="提取名称")
    description: str = Field(None, description="提取描述")
    enable: bool = Field(..., description="是否启用")
    case_id: int = Field(None, description="用例id")
    extract_from: int = Field(..., description="提取来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed")
    extract_type: int = Field(..., description="提取类型 1: Json-Path 2: Re_Gex")
    extract_exp: str = Field(None, description="提取表达式")
    extract_out_name: str = Field(..., description="提取值")
    extract_index: int = Field(None, description="提取索引")
    extract_to: int = Field(None, description="提取到 1: 环境变量 2: 用例变量")

