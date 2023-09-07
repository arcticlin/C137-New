# coding=utf-8
"""
File: case_log.py
Author: bot
Created: 2023/8/9
Description:
"""

from datetime import datetime


class CaseLog:
    def __init__(self):
        self.log = []
        self.logs = {
            "env_prefix": [],
            "case_prefix": [],
            "case_vars": [],
            "case_suffix": [],
            "env_assert": [],
            "case_assert": [],
            "env_suffix": [],
            "extract": [],
        }

    def append(self, content, end=True):
        if end:
            self.log.append("[{}]: 步骤结束 -> {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content))
        else:
            self.log.append("[{}]: 步骤开始 -> {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content))

    def var_append(self, content):
        self.log.append("[{}]: 替换变量 -> {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content))

    def log_append(self, content, log_type):
        """
        添加日志
        :param content:
        :param log_type:
        :return:
        """

        if log_type == "env_prefix":
            t = "环境前置"
        elif log_type == "env_suffix":
            t = "环境后置"
        elif log_type == "case_prefix":
            t = "用例前置"
        elif log_type == "case_suffix":
            t = "用例后置"
        elif log_type == "case_vars":
            t = "用例变量转换"
        elif log_type == "case_assert":
            t = "用例断言"
        elif log_type == "env_assert":
            t = "环境断言"
        elif log_type == "extract":
            t = "提取变量"
        else:
            t = ""
        self.logs[log_type].append("[{}]: {} -> {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), t, content))

    def vars_append(self, content):
        self.logs["case_vars"].append("[{}]: 替换变量 -> {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content))

    def o_append(self, content):
        """
        原始append
        :param content:
        :return:
        """
        self.log.append(content)

    def join(self):
        return "\n".join(self.log)
