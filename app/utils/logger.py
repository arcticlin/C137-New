# coding=utf-8
"""
File: logger.py
Author: bot
Created: 2023/7/25
Description:
"""
import inspect
import os.path
from base_config import Config
from loguru import logger


class Log:
    def __init__(self, name="C137"):
        if not os.path.exists(Config.LOG_DIR):
            os.mkdir(Config.LOG_DIR)
        self.business = name

    def info(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(
            inspect.currentframe().f_back
        )
        logger.bind(
            name="C137_Info.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).debug(message)

    def error(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(
            inspect.currentframe().f_back
        )
        logger.bind(
            name="C137_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).error(message)

    def warning(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(
            inspect.currentframe().f_back
        )
        logger.bind(
            name="C137_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).warning(message)

    def debug(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(
            inspect.currentframe().f_back
        )
        logger.bind(
            name="C137_Info.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).debug(message)

    def exception(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(
            inspect.currentframe().f_back
        )
        logger.bind(
            name="Kino_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).exception(message)
