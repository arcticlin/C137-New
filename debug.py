# coding=utf-8
"""
File: debug.py
Author: bot
Created: 2023/10/18
Description:
"""


import asyncio

from app.services.api_case_new.case.crud.case_crud import ApiCaseCrud
from app.services.api_case_new.case_service import CaseService
from app.services.common_config.crud.envs.env_crud import EnvCrud
from app.services.common_config.env_service import EnvService
from app.services.directory.directory_service import DirectoryService

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 调用异步方法
result = loop.run_until_complete(ApiCaseCrud.query_case_detail(2))

# 输出结果
print(result)
