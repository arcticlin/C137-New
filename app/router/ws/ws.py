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


# @ws.websocket("/ws/{token}", name="websocket")
# async def websocket_endpoint(websocket: WebSocket, token: str):
#     try:
#         # UserToken.parse_token(token)
#         await websocket.accept()
#         print("11")
#         if websocket not in connected_clients:
#             await websocket.send_text("Welcome to websocket")
#         connected_clients.add(websocket)
#         while True:
#             data = await websocket.receive_text()
#             for client in connected_clients:
#                 await client.send_text(data)
#     except WebSocketDisconnect:
#         connected_clients.remove(websocket)
#         await websocket.close()
#     except Exception as e:
#         connected_clients.remove(websocket)
#         await websocket.close(code=1000)
#         raise e
