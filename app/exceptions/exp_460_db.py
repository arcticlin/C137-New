# coding=utf-8
"""
File: exp_460_db.py
Author: bot
Created: 2023/10/24
Description:
"""
SQL_CONNECT_FAIL = (400, 40460, "SQL连接失败")
SQL_EXECUTE_FAIL = (400, 40461, "SQL执行失败")


SQL_NOT_EXISTS = (400, 40462, "SQL配置不存在")
SQL_NAME_EXISTS = (400, 40463, "SQL配置名称已存在")

NO_ALLOW_TO_DELETE_SQL = (400, 40464, "无权删除该SQL配置")
NO_ALLOW_TO_MODIFY_SQL = (400, 40465, "无权修改该SQL配置")
