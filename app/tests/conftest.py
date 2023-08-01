# coding=utf-8
"""
File: conftest.py
Author: bot
Created: 2023/8/1
Description:
"""
import pytest


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8888"
