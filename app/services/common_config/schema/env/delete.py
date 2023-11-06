# coding=utf-8
"""
File: delete.py
Author: bot
Created: 2023/11/6
Description:
"""
from pydantic import BaseModel, Field


class RequestDeleteEnvVars(BaseModel):
    key: str
