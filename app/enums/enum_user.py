# coding=utf-8
"""
File: enum_user.py
Author: bot
Created: 2023/7/25
Description:
"""

from enum import Enum, unique


@unique
class UserRoleEnum(Enum):
    NORMAL_USER = 1
    ADMIN = 2
