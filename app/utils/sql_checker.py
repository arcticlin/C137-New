# coding=utf-8
"""
File: sql_checker.py
Author: bot
Created: 2023/8/2
Description:
"""


class SqlChecker:
    @staticmethod
    def check_permission(operator: int, check_list: str):
        if "," in check_list:
            check_list = check_list.split(",")
        else:
            check_list = [check_list]
        if str(operator) in check_list:
            return True
        return False
