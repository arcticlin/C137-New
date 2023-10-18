# coding=utf-8
"""
File: debug.py
Author: bot
Created: 2023/10/18
Description:
"""


import asyncio

from app.crud.auth.auth_crud import AuthCrud

# 创建一个事件循环
loop = asyncio.get_event_loop()

# 调用异步方法
result = loop.run_until_complete(AuthCrud.get_user_by_account("test01"))

# 输出结果
print(result)
