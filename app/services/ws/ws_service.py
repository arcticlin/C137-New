# coding=utf-8
"""
File: ws_services.py
Author: bot
Created: 2023/10/13
Description:
"""
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
}
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
    async def ws_notify_update_user_list():
        for client in connected_clients:
            await connected_clients[client].send_json({"code": 1001})
