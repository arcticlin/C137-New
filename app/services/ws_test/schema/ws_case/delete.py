# coding=utf-8
"""
File: delete.py
Author: bot
Created: 2023/11/21
Description:
"""
from typing import List

from pydantic import BaseModel, Field


class RequestDeleteWsCase(BaseModel):
    case_id: List[int] = Field(..., description="case_id列表")
