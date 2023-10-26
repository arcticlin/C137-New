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
    types: int = Field(..., title="参数值类型, 1:path 2: qeury")
    value: str = Field(..., title="参数值")
    enable: bool = Field(True, title="是否启用")
    comment: str = Field(None, title="备注")