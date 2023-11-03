# coding=utf-8
"""
File: ws_services.py
Author: bot
Created: 2023/10/13
Description:
"""
from typing import List

from app.services.ws.client_store import connected_clients
from fastapi import WebSocket
from loguru import logger

"""
{
  "code": 200,
  "user_id": "",
  "project_id": "",
  "env_id": "",
  "case_id": "",
  "msg": ""
}
"""
"""
10001: 消息通知
1001: 更新用户列表
1002: 更新项目列表
"""


class WsService:
    @staticmethod
    async def send_message():
        pass

    @staticmethod
    def connect_success():
        return {"code": 1000}

    @staticmethod
    async def remove_client(client_identify: str):
        if client_identify in connected_clients:
            del connected_clients[client_identify]
        else:
            logger.debug("client not in connected_clients")

    @staticmethod
    async def ws_notify_message(user_id: List[int], message: str):
        for uid in user_id:
            if str(uid) in connected_clients:
                await connected_clients[str(uid)].send_json({"code": 10001, "msg": message})

    @staticmethod
    async def ws_notify_update_user_list():
        print("here", connected_clients)
        for client in connected_clients:
            await connected_clients[client].send_json({"code": 1001})

    @staticmethod
    async def ws_notify_update_project_list(user_id: List[int]):
        for uid in user_id:
            if str(uid) in connected_clients:
                await connected_clients[str(uid)].send_json({"code": 1002})

    @staticmethod
    async def ws_notify_invited_in_project(user_id: List[int], project_id: int):
        for uid in user_id:
            if str(uid) in connected_clients:
                await connected_clients[str(uid)].send_json({"code": 1002})
