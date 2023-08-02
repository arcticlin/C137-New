# coding=utf-8
"""
File: project_directory_router.py
Author: bot
Created: 2023/8/1
Description:
"""
from fastapi import APIRouter

pd = APIRouter(prefix="/directory")


@pd.delete("/delete")
async def get_project_directory():
    pass
