# coding=utf-8
"""
File: pd_schema.py
Author: bot
Created: 2023/8/1
Description:
"""
from pydantic import BaseModel


class AddPDirectoryRequest(BaseModel):
    project_id: int
    name: str
    parent_id: int = None


class DeletePDirectoryRequest(BaseModel):
    project_id: int
    directory_id: int


class UpdatePDirectoryRequest(BaseModel):
    directory_id: int
    name: str
