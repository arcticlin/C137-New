# coding=utf-8
"""
File: user.py
Author: bot
Created: 2023/7/25
Description:
"""
from app.core.db_connector import BaseMixin, Base
from sqlalchemy import String, Column, INT, DATETIME, BOOLEAN, TEXT
from sqlalchemy import Enum as SqlEnum
from app.enums.enum_user import UserRoleEnum


class UserModel(Base, BaseMixin):
    __tablename__ = "users"

    id = Column(INT, primary_key=True, autoincrement=True)

    account = Column(String(64), nullable=False, index=True, comment="登录账号")
    password = Column(String(64), nullable=False, comment="密码")

    nickname = Column(String(64), nullable=False, comment="昵称")
    email = Column(String(64), nullable=True, comment="邮箱")

    user_role = Column(
        SqlEnum(UserRoleEnum),
        default=UserRoleEnum.NORMAL_USER,
        comment="用户权限, 1: 普通用户, 2: 管理员",
    )

    department_id = Column(INT, nullable=True, comment="部门id")
    valid = Column(BOOLEAN, default=True, comment="账号可用状态")

    avatar = Column(TEXT, nullable=True, comment="头像")
    last_login = Column(DATETIME, comment="记录最后一次登录时间")

    def __init__(
        self,
        account,
        password,
        nickname=None,
        email=None,
        user_role=UserRoleEnum.NORMAL_USER,
        department_id=None,
        avatar=None,
    ):
        self.account = account
        self.password = password
        self.nickname = nickname if nickname is not None else account
        self.email = email
        self.user_role = user_role
        self.department_id = department_id
        self.avatar = avatar
