# coding=utf-8
"""
File: runner.py
Author: bot
Created: 2023/10/31
Description:
"""
from typing import List

from pydantic import BaseModel, Field, validator


class RequestRunSingleCase(BaseModel):
    env_id: int
    case_id: int


class RequestRunMultiCase(BaseModel):
    env_id: int
    case_id: List[int]
