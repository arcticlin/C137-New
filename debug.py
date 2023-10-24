# coding=utf-8
"""
File: debug.py
Author: bot
Created: 2023/10/18
Description:
"""


import asyncio

from app.services.common_config.crud.envs.env_crud import EnvCrud
from app.services.common_config.env_service import EnvService
from app.services.directory.directory_service import DirectoryService

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 调用异步方法
result = loop.run_until_complete(EnvCrud.env_exists_by_id(11))

# 输出结果
print(result)
