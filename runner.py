# coding=utf-8
"""
File: runner.py
Author: bot
Created: 2023/8/3
Description:
"""
import os
import logging
import sys, inspect

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from uvicorn import Server, Config
from app.utils.new_logger import logger
from base_config import Config as BConfig

from main import app


LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False
WORKERS = int(os.environ.get("GUNICORN_WORKERS", "1"))


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = inspect.currentframe(), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# def setup_logging():
#     # intercept everything at the root logger
#     logging.root.handlers = [InterceptHandler()]
#     logging.root.setLevel(LOG_LEVEL)
#
#     # remove every other logger's handlers
#     # and propagate to root logger
#     for name in logging.root.manager.loggerDict.keys():
#         logging.getLogger(name).handlers = []
#         logging.getLogger(name).propagate = True
#
#     # configure loguru
#     logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


if __name__ == "__main__":
    # server = Server(
    #     Config(
    #         "main:app",
    #         host="0.0.0.0",
    #         port=BConfig.SERVER_PORT,
    #         log_level=LOG_LEVEL,
    #         reload=True,
    #     ),
    # )
    # setup_logging()
    #
    # server.run()
    intercept_handler = InterceptHandler()
    # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
    # logging.root.handlers = [intercept_handler]
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

    options = {
        "bind": f"0.0.0.0:{BConfig.SERVER_PORT}",
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
        "reload": True,
    }

    StandaloneApplication(app, options).run()
