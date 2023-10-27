# coding=utf-8
"""
File: conftest.py
Author: bot
Created: 2023/8/1
Description:
"""
import pytest
import requests

from app.tests.module.auth.api_auth import AuthModule


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8888"


@pytest.fixture(scope="session")
def login_token(base_url):
    url = f"{base_url}{AuthModule.login_path()}"
    data = AuthModule.login_form("test01", "123456")
    print(data)
    res = requests.post(url=url, json=data)
    print("res", res)
    return {"authorization": res.json()["data"]["token"], "accept": "application/json, text/plain, */*"}


# @pytest.fixture(scope="session")
# def create_project()
