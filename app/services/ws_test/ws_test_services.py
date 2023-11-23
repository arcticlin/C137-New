# coding=utf-8
"""
File: ws_test_services.py
Author: bot
Created: 2023/11/23
Description:
"""
import json
from datetime import datetime

import websockets
import asyncio
from loguru import logger
import msgpack
import jsonpath

from app.services.ws.ws_service import WsService


class WsTestService:
    def __init__(self, ws_url: str, operator: int, heartbeat: int = 2):
        self.ws_url = ws_url
        self.heartbeat = heartbeat
        self.current_case = {
            "case_id": 0,
            "ws_code": 0,
            "json_exp": "",
            "expected": "",
        }
        self.last_activity_time = datetime.now()
        self.operator = operator

    async def send_heartbeat(self, websocket: websockets.WebSocketClientProtocol):
        # 发送心跳包
        while True:
            try:
                await websocket.send(1)
                await asyncio.sleep(self.heartbeat)
            except websockets.ConnectionClosed:
                break

    async def start_listener(self):
        async with websockets.connect(self.ws_url) as websocket:
            heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
            try:
                await self.receive_message(websocket)
            finally:
                heartbeat_task.cancel()
                await websocket.close()

    async def receive_message(self, websocket: websockets.WebSocketClientProtocol):
        while True:
            if (datetime.now() - self.last_activity_time).seconds > 300:
                logger.warning("超时未操作，断开连接")
                break
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                self.last_activity_time = datetime.now()
                print("1111", message, type(message))
                data = msgpack.unpackb(message, raw=False)
                await self.handle_message(data)
            except asyncio.TimeoutError:
                # 无消息无需处理, 继续等待
                continue

    async def handle_message(self, data) -> None:
        """处理消息, 与self.current_case做比较"""
        logger.info(f"收到消息:{json.dumps(data, ensure_ascii=False)}")
        if self.current_case["case_id"] == 0:
            # 未开始测试
            logger.info("未开始已测试")
            return
        logger.info("开始测试")
        if self.current_case["ws_code"] == data.get("co"):
            if not self.current_case["json_exp"]:
                # 无需验证
                await self.success_message(data)
                return
            else:
                get_exp = jsonpath.jsonpath(data, self.current_case["json_exp"])
                if get_exp:
                    if not self.current_case["expected"]:
                        await self.success_message(data)
                        return
                    else:
                        if str(get_exp[0]) == self.current_case["expected"]:
                            await self.success_message(data)
                            return
                        else:
                            return
        else:
            return

    async def success_message(self, data: dict):
        """发送成功消息"""
        await WsService.ws_notify_ws_test([self.operator], data)
        self.clear_case()

    def clear_case(self):
        self.current_case = {
            "case_id": 0,
            "ws_code": 0,
            "json_exp": "",
            "expected": "",
        }

    def add_case(self, case_data: dict):
        logger.info(f"添加了用例:{json.dumps(case_data, ensure_ascii=False)}")
        self.current_case = case_data
