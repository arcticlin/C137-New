# coding=utf-8
"""
File: auth_exp.py
Author: bot
Created: 2023/7/26
Description:
"""

ACCOUNT_EXISTS = (400, 40410, "账号已存在")
NICKNAME_EXISTS = (400, 40410, "昵称已存在")
ACCOUNT_NOT_EXISTS = (400, 40411, "账号不存在, 请先注册~")
PASSWORD_INCORRECT = (400, 40412, "密码错误")
ACCOUNT_IS_BANNED = (400, 40413, "账号已被禁用~")

TOKEN_IS_EXPIRED = (401, 40402, "Token已过期")
TOKEN_IS_INVALID = (401, 40401, "无效的Token")
AUTH_WITHOUT_TOKEN = (401, 40403, "缺少Token")
AUTH_NOT_PERMISSION = (401, 40404, "权限不足")

RESET_CODE_INCORRECT = (400, 40420, "重置码错误")
