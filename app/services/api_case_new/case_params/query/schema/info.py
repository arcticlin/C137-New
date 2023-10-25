# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""
from pydantic import BaseModel, Field


class OutParamsInfo(BaseModel):
    path_id: int = Field(..., title="path id")
    key: str = Field(..., title="参数名")
    types: int = Field(..., title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(..., title="参数值")
    enable: bool = Field(True, title="是否启用")
    comment: str = Field(None, title="备注")