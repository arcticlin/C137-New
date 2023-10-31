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
        "env_id": 6,
        "url_info": {"method": "GET", "url": "api/character/159"},
        "body_info": {"body_type": 0},
        "prefix_info": [
            {
                "suffix_type": 1,
                "name": "设置今天截止",
                "enable": True,
                "sort": 1,
                "execute_type": 5,
                "run_out_name": "today_end",
                "run_command": """from datetime import datetime\ntoday_end = int(datetime.now().replace(hour=23, minute=59, second=59, microsecond=0).timestamp())""",
            }
        ],
        "assert_info": [
            {
                "name": "状态码",
                "enable": True,
                "assert_from": 3,
                "assert_type": 1,
                "assert_exp": None,
                "assert_value": 400,
            }
        ],
        "extract_info": [
            {
                "name": "提取URL",
                "enable": True,
                "extract_from": 2,
                "extract_type": 1,
                "extract_exp": "$.url",
                "extract_out_name": "rick_url",
                "extract_index": 0,
            },
            {
                "name": "提取Location",
                "enable": True,
                "extract_from": 2,
                "extract_type": 2,
                "extract_exp": r".*" + "(Earth\s\(.*\)" + r",",
                "extract_out_name": "location",
                "extract_index": 0,
            },
        ],
    }
    r = requests.post(url=url, json=body, headers=token)
    print(r)
    print(r.text)
