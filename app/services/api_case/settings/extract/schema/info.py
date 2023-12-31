# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""
from typing import Any

from pydantic import BaseModel, Field


class OutExtractInfo(BaseModel):
    extract_id: int = Field(..., description="提取id")
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



class DebugExtractInfo(BaseModel):
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


class OutExtractResult(BaseModel):
    name: str = Field(None, description="提取名称")
    extract_key: str = Field(..., description="提取变量名")
    extract_value: Any = Field(None, description="变量值")
