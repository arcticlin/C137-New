# coding=utf-8
"""
File: new.py
Author: bot
Created: 2023/11/2
Description:
"""
from pydantic import BaseModel, Field


class UpdateReportData(BaseModel):
    success: int = Field(0, title="成功用例数")
    failed: int = Field(0, title="失败用例数")
    xfail: int = Field(0, title="预期失败用例数")
    skip: int = Field(0, title="跳过用例数")
    duration: float = Field(0, title="总耗时")
    status: int = Field(0, title="状态. 0: 未执行, 1: 执行中, 2: 执行完成, 3: 执行失败")
