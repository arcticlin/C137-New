# coding=utf-8
"""
File: time_utils.py
Author: bot
Created: 2023/9/14
Description:
"""
from datetime import datetime


class TimeUtils:
    @staticmethod
    def get_current_time_without_year():
        """
        获取当前时间, 格式为 m-d h:m:s
        """
        now = datetime.now()
        return now.strftime("%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(TimeUtils.get_current_time_without_year())
