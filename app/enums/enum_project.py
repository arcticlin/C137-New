# coding=utf-8
"""
File: enum_project.py
Author: bot
Created: 2023/7/28
Description:
"""
from enum import Enum, unique


@unique
class ProjectRoleEnum(Enum):
    MEMBER = 1
    CREATOR = 2
    LEADER = 3
