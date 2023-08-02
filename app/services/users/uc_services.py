# coding=utf-8
"""
File: uc_services.py
Author: bot
Created: 2023/7/31
Description:
"""
from app.crud.auth.auth_crud import AuthCrud
from app.enums.enum_user import UserRoleEnum


class UserCenterServices:
    @staticmethod
    async def get_platform_user():
        result = await AuthCrud.get_all_user()
        user_list = []
        for user_id, nickname, email, role, department_id, avatar in result:
            user_list.append(
                {
                    "user_id": user_id,
                    "nickname": nickname,
                    "email": email,
                    "role": UserRoleEnum[role].value,
                    "department_id": department_id,
                    "avatar": avatar,
                }
            )
        return user_list
