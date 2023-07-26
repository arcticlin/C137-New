# coding=utf-8
"""
File: flyele_services.py
Author: bot
Created: 2023/7/26
Description:
"""
from datetime import datetime, timedelta

import requests
from app.exceptions.commom_exception import CustomException
import re
from typing import List, Dict


class FlyeleServices:
    @staticmethod
    def expired_now():
        now = datetime.now()
        ago_five = now - timedelta(minutes=5)
        return int(ago_five.timestamp())

    @staticmethod
    def has_chinese_comma(text):
        pattern = re.compile(r"，")  # 匹配中文逗号
        return bool(pattern.search(text))

    @staticmethod
    def remove_duplicate(data: List[Dict]):
        unique_info = []
        for item in data:
            if item not in unique_info:
                unique_info.append(item)
        return unique_info

    @staticmethod
    async def get_user_id_by_python(phone: str, headers: dict) -> List:
        if FlyeleServices.has_chinese_comma(phone):
            raise CustomException((200, 40000, "手机号不能包含中文逗号"))
        if "," in phone:
            phone = phone.strip()
        url = "https://api-test.flyele.vip/userc/v2/userInfos"
        params = {"telephone": phone}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 401:
            raise CustomException((200, 40001, "token失效, 请重新在页面右上角放入新的Token"))
        user_info: List[Dict] = response.json()["data"]
        no_repeat = FlyeleServices.remove_duplicate(user_info)
        return [x["user_id"] for x in no_repeat]

    @staticmethod
    async def add_person_vip(user_ids: List[str], days: int, headers: dict):
        url = "https://api-test.flyele.vip/userc/v2/member/backend"
        data = {"user_ids": user_ids, "duration": days, "vip_type": 1}
        response = requests.post(url=url, json=data, headers=headers)
        if response.status_code != 200:
            raise CustomException((200, 40002, response.text))

    @staticmethod
    async def add_team_vip(user_ids: List[str], days: int, headers: dict):
        url = "https://api-test.flyele.vip/userc/v2/member/backend"
        data = {"user_ids": user_ids, "duration": days, "vip_type": 2}
        response = requests.post(url=url, json=data, headers=headers)
        if response.status_code != 200:
            raise CustomException((200, 40003, response.text))

    @staticmethod
    async def expire_to_person(user_ids: List[str], types: int, headers: dict):
        url = "https://api-test.flyele.vip/userc/v2/member/clear"
        data = {
            "user_ids": user_ids,
            "expire_at": FlyeleServices.expired_now(),
            "expire_type": types,
            "is_clear_bind": 2,
            "operate_type": "expire",
        }
        response = requests.delete(url=url, json=data, headers=headers)
        if response.status_code != 200:
            raise CustomException((200, 40004, response.text))

    @staticmethod
    async def clear_vip(user_ids: List[str], headers: dict):
        url = "https://api-test.flyele.vip/userc/v2/member/clear"
        data = {
            "user_ids": user_ids,
            "is_clear_bind": 1,
            "operate_type": "delete",
        }
        response = requests.delete(url=url, json=data, headers=headers)
        if response.status_code != 200:
            raise CustomException((200, 40005, response.text))

    @staticmethod
    async def push_statistics(phone: str, headers: dict):
        url = "https://api-test.flyele.vip/statistics/v2/user_action/statistics/send"
        user_ids = await FlyeleServices.get_user_id_by_python(phone, headers)
        params = {"users_id": ",".join(user_ids)}
        response = requests.post(url=url, params=params, headers=headers)
        if response.status_code != 200:
            raise CustomException((200, 40006, response.text))
