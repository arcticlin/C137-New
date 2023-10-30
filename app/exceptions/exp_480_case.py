# coding=utf-8
"""
File: exp_480_case.py
Author: bot
Created: 2023/8/2
Description:
"""


EXTRACT_NOT_EXISTS = (400, 40601, "提取变量不存在")
ASSERT_NOT_EXISTS = (400, 40602, "断言不存在")

CASE_ADD_FAILED = (400, 40480, "添加用例失败")
CASE_DELETE_FAILED = (400, 40481, "删除用例失败")

CASE_NOT_EXISTS = (400, 40482, "用例不存在")
CASE_EXISTS = (400, 40483, "目录用例已存在, 同一级目录仅不支持同名和同请求方式的用例")


PYTHON_SCRIPT_OUT_NAME_WRONG = (400, 41480, "出参变量不在执行脚本函数中")
BODY_CAN_NOT_SERIALIZABLE = (400, 41481, "body参数无法序列化")
