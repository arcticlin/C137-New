# coding=utf-8
"""
File: update.py
Author: bot
Created: 2023/10/23
Description:
"""
from pydantic import BaseModel, Field


class RequestHeaderUpdate(BaseModel):
    header_id: int = Field(None, title="header id")
    key: str = Field(None, title="参数名")
    value_type: int = Field(None, title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(None, title="参数值")
    enable: bool = Field(None, title="是否启用")
    comment: str = Field(None, title="备注")
