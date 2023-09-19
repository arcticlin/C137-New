# coding=utf-8
"""
File: ws.py
Author: bot
Created: 2023/9/19
Description:
"""
from typing import Set

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.handler.token_handler import UserToken
from app.services.ws.client_store import connected_clients

ws = APIRouter()


@ws.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user_id = ""
    try:
        UserToken.parse_token(token)
        user_id = UserToken.get_user_id_from_token(token)
        await websocket.accept()
        if websocket not in connected_clients:
            await websocket.send_text("Welcome to websocket")
        connected_clients[user_id] = websocket
        while True:
            data = await websocket.receive_text()
            for client in connected_clients.keys():
                await connected_clients[client].send_text(data)
    except WebSocketDisconnect as e:
        pass
    except Exception as e:
        pass
    finally:
        if connected_clients.__contains__(user_id):
            connected_clients.pop(user_id)
        print(connected_clients)
