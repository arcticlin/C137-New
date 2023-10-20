# coding=utf-8
"""
File: debug.py
Author: bot
Created: 2023/10/18
Description:
"""


import asyncio

from app.crud.project.project_member_crud import ProjectMCrud
from app.services.directory.directory_service import DirectoryService

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 调用异步方法
result = loop.run_until_complete(DirectoryService.get_project_directory_tree(1))

# 输出结果
print(result)
