"""
auth接口测试基类
"""
from base_config import Config


class AuthModule:

    BASE_PATH: str = "http//127.0.0.1:8888/auth"

    @staticmethod
    def register_path() -> str:
        return AuthModule.BASE_PATH + "/register"

    @staticmethod
    def login_path() -> str:
        return AuthModule.BASE_PATH + "/login"

    @staticmethod
    def register_form(username: str, password: str) -> dict:
        return {
            "username": username,
            "password": password,
        }

    @staticmethod
    def login_form(username: str, password: str) -> dict:
        return {
            "username": username,
            "password": password,
        }