# coding=utf-8
"""
File: ws_service.py
Author: bot
Created: 2023/9/19
Description:
"""
from app.services.ws.client_store import connected_clients
from fastapi import WebSocket


class WsService:
    @staticmethod
    async def send_message(message: str, client: WebSocket = None):
        for client in connected_clients:
            await client.send_text(message)
