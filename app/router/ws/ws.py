# coding=utf-8
"""
File: ws.py
Author: bot
Created: 2023/9/19
Description:
"""
from typing import Set

from fastapi import APIRouter, WebSocket, Query
from starlette.websockets import WebSocketDisconnect

from app.handler.auth.token_handler import UserToken
from app.services.ws.client_store import connected_clients
from app.services.ws.ws_service import WsService
from loguru import logger

ws = APIRouter()


@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    user_id = ""
    try:
        UserToken.parse_token(token)
        user_id = UserToken.get_user_id_from_token(token)
        await websocket.accept()
        if user_id not in connected_clients or connected_clients[user_id] != websocket:
            connected_clients[user_id] = websocket
        await websocket.send_json(WsService.connect_success())
        while True:
            data = await websocket.receive_text()
            for client in connected_clients.keys():
                await connected_clients[client].send_text(data)
    except WebSocketDisconnect as e:
        logger.debug(f"client: {user_id} disconnect")
        await WsService.remove_client(user_id)
    except Exception as e:
        pass
    finally:
        pass
