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
    url = AuthModule.login_path()
    data = AuthModule.login_form("tt", "1234")
    res = requests.post(url=url, json=data)
    return res.json()["data"]["token"]


# @pytest.fixture(scope="session")
# def create_project()