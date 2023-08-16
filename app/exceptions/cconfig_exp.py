# coding=utf-8
"""
File: cconfig_exp.py
Author: bot
Created: 2023/8/4
Description:
"""

REDIS_NOT_EXISTS = (400, 40501, "Redis配置不存在")
REDIS_NAME_EXISTS = (400, 40502, "Redis名称已存在")

SQL_NOT_EXISTS = (400, 40503, "SQL配置不存在")
SQL_NAME_EXISTS = (400, 40504, "SQL名称已存在")

SCRIPT_NOT_EXISTS = (400, 40505, "脚本配置不存在")
SCRIPT_NAME_EXISTS = (400, 40506, "脚本名称已存在")


ENV_NOT_EXISTS = (400, 40507, "环境不存在")
ENV_NAME_EXISTS = (400, 40508, "环境名称已存在")

SUFFIX_NOT_EXISTS = (400, 40509, "环境不存在")
SUFFIX_IS_EXISTS = (400, 40510, "环境名称已存在")
