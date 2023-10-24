# coding=utf-8
"""
File: rds_c_exp_450.py
Author: bot
Created: 2023/10/24
Description:
"""
REDIS_NOT_EXISTS = (400, 40450, "Redis配置不存在")
REDIS_NAME_EXISTS = (400, 40451, "Redis配置名称已存在")

REDIS_CONNECT_FAIL = (400, 40452, "Redis连接失败")


NO_ALLOW_TO_DELETE_REDIS = (400, 40453, "无权删除该Redis配置")
NO_ALLOW_TO_MODIFY_REDIS = (400, 40454, "无权修改该Redis配置")
