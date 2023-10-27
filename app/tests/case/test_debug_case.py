# coding=utf-8
"""
File: test_debug_case.py
Author: bot
Created: 2023/10/27
Description:
"""
import pytest
import requests


def test_case_debugger(base_url, login_token):
    token = login_token
    url = f"{base_url}/c/debug"
    body = {
        "env_id": 1,
        "url_info": {"method": "GET", "url": "https://rickandmortyapi.com/api/character/159"},
        "body_info": {"body_type": 0},
    }
    r = requests.post(url=url, json=body, headers=token)
    print(r)
    print(r.text)
