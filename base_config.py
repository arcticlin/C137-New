# coding=utf-8
"""
File: base_config.py
Author: bot
Created: 2023/7/25
Description: FastAPI基本配置
"""


import os
from typing import List

# from pydantic_settings import SettingsConfigDict
from pydantic import BaseSettings

ROOT = os.path.dirname(__file__)


class BasicConfig(BaseSettings):
    # Sqlalchemy的连接方式
    SQLALCHEMY_URI: str = ""
    ASYNC_SQLALCHEMY_URI: str = ""

    ENV: str

    # MYSQL 配置
    MYSQL_DROP_BEFORE_START: bool
    MYSQL_TRACK_MODIFICATION: bool = False

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PWD: str
    MYSQL_DBNAME: str

    # Redis 连接配置
    REDIS_ON: bool = False
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PWD: str
    REDIS_NODES: List[dict] = []

    # Token_info
    # 过期时间, 分钟为单位 60分钟 * 24小时 * 7天
    EXPIRED_MIN: int = 60 * 24 * 7
    TOKEN_KEY: str
    TOKEN_SALT: str
    TOKEN_STRONG_VERIFY: bool

    # Log 路径
    LOG_DIR: str = os.path.join(ROOT, "logs")

    # Middleware, 跨域配置
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = True

    # User权限
    U_MEMBER: int = 1
    U_SUPERVISOR: int = 2

    # FastAPI基本信息

    title: str = "C137"
    SERVER_PORT: int

    # Celery配置
    CELERY_BROKER_URL: str
    CELERY_STATUS_BACKEND: str


class DevConfig(BasicConfig):
    # model_config = SettingsConfigDict(
    #     env_file=os.path.join(ROOT, "env_config", "dev.env"), env_file_encoding="utf-8"
    # )
    class Config:
        env_file = os.path.join(ROOT, "env_config", "dev.env")
        env_file_encoding = "utf-8"

    ENV = "dev"
    REDIS_ON: bool = False
    title: str = "C137_Dev"
    MYSQL_DROP_BEFORE_START: bool = False
    TOKEN_STRONG_VERIFY = False


class DockerConfig(BasicConfig):
    # model_config = SettingsConfigDict(
    #     env_file=os.path.join(ROOT, "env_config", "dev.docker.env"),
    #     env_file_encoding="utf-8",
    # )
    class Config:
        env_file = os.path.join(ROOT, "env_config", "dev.env")
        env_file_encoding = "utf-8"

    ENV = "docker"
    REDIS_ON: bool = False
    title: str = "C137_Docker"
    MYSQL_DROP_BEFORE_START: bool = False
    TOKEN_STRONG_VERIFY = False


get_env_from_sys = os.environ.get("c137_env", "dev")

# Todo: 后续实例化生产环境
if get_env_from_sys == "docker":
    Config = DockerConfig()
else:
    Config = DevConfig()

Config.SQLALCHEMY_URI = f"mysql+mysqlconnector://{Config.MYSQL_USER}:{Config.MYSQL_PWD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DBNAME}"

# 给SQLALCHEMY_URI赋值
Config.ASYNC_SQLALCHEMY_URI = (
    f"mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PWD}"
    f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DBNAME}"
)
