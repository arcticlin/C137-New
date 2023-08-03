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
    _instance = None

    def __new__(cls, name="C137"):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self, name="C137"):
        if not os.path.exists(Config.LOG_DIR):
            os.mkdir(Config.LOG_DIR)
        self.business = name

    # def __init__(self, name="C137"):
    #     if not os.path.exists(Config.LOG_DIR):
    #         os.mkdir(Config.LOG_DIR)
    #     self.business = name

    def d_info(self, who: int, do_what: str, to: int = None):
        message = f"用户: {who} -> {do_what}"
        if to is not None:
            message = message + f" -> {to}"
        self.info(message)

    def info(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(
            name="C137_Info.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).debug(message)

    def error(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(
            name="C137_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).error(message)

    def warning(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(
            name="C137_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).warning(message)

    def debug(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(
            name="C137_Info.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).debug(message)

    def exception(self, message: str):
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(
            name="Kino_error.log",
            func=func,
            line=line,
            business=self.business,
            file_name=file_name,
        ).exception(message)
