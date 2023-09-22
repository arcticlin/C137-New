# coding=utf-8
"""
File: uvicorn_runner.py
Author: bot
Created: 2023/8/3
Description:
"""
import os, logging, sys, inspect

from uvicorn import Config, Server, main
from uvicorn.supervisors import ChangeReload
from base_config import Config as BConfig
from app.utils.new_logger import logger


LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


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

        logger.opt(depth=depth, exception=record.exc_info, colors=True).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS, "colorize": True}])


class FixedLoggingConfig(Config):
    """Subclass of uvicorn config that re-configures logging."""

    serialize_logs = False

    def configure_logging(self) -> None:  # noqa: D102
        self.use_colors = True
        super().configure_logging()
        setup_logging()


def run(host="0.0.0.0", port=8080, log_level=LOG_LEVEL, json_logs=JSON_LOGS, reload=False):  # noqa: S104
    """Run the Uvicorn server.

    Parameters:
        host: The host to bind.
        port: The port to use.
        log_level: The log level.
        json_logs: Whether to serialize logs in JSON.
        reload: Whether to enable live-reload.
    """
    FixedLoggingConfig.serialize_logs = json_logs
    config = FixedLoggingConfig(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )

    server = Server(config)

    setup_logging()

    if reload:
        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()
    else:
        server.run()


if __name__ == "__main__":
    run(port=BConfig.SERVER_PORT, reload=True)
