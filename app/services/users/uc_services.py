# coding=utf-8
"""
File: uc_services.py
Author: bot
Created: 2023/7/31
Description:
"""
from app.crud.auth.auth_crud import AuthCrud


class UserCenterServices:
    @staticmethod
    async def get_platform_user():
        result = await AuthCrud.get_all_user()
        return result
