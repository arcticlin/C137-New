# coding=utf-8
"""
File: new_logger.py
Author: bot
Created: 2023/8/2
Description:
"""

from loguru import logger
import sys, os
from base_config import Config


if not os.path.exists(Config.LOG_DIR):
    os.mkdir(Config.LOG_DIR)


if Config.ENV == "dev":
    # 需要输出到控制台
    logger.add(
        sink=sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{function}:{line} | {message}",
        level="DEBUG",
        backtrace=True if Config.ENV == "dev" else False,  # 替换为判断当前是否是开发环境的条件
        colorize=True,
    )
else:
    # 需要输出到文件中，保留10天日志文件，文件大小限制在30M
    logger.add(
        sink="%s/logfile_{time}.log" % Config.LOG_DIR,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{function}:{line} | {message}",
        rotation="10 days",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        enqueue=True,
        # max_size=30 * 1024 * 1024,  # 30M，单位是字节
    )
