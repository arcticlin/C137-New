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
import struct

from app.services.ws.ws_service import WsService
from app.services.ws_test.crud.ws_case.ws_case_crud import WsCaseCrud


class WsTestService:
    def __init__(self, ws_url: str, operator: int, heartbeat: int = 5):
        self.ws_url = ws_url
        self.ws_flag = ws_url[-5:]
        self.heartbeat = heartbeat
        self.current_case = {
            "case_id": 0,
            "ws_code": 0,
            "json_exp": "",
            "expected": "",
        }
        self.last_activity_time = datetime.now()
        self.operator = operator
        self.current_ws_obj = dict()
        self.connect_status = None

    @staticmethod
    def parse_fx_ws(data: dict):
        """解析FX_WS"""
        mapping = {
            "a": "ref_id",  # 关联id，根据ref_type类型确认是事项id还是项目id等
            "b": "ref_type",  # 关联类型，1->事项，2->笔记，3->项目，4->空间，5->私聊
            "c": "code",  # 消息编码
            "d": "message_id",  # 消息id
            "e": "creator_id",  # 创建人id
            "f": "comment_id",  # 评论id
            "g": "title",  # 标题
            "h": "message",  # 消息内容
            "i": "send_from",  # 发送平台，1→微信小程序，2->PC，3->APP，4->WEB
            "j": "file_id",  # 文件ID
            "k": "affected",  # 是否受影响，1->是
            "l": "creator_nick",  # 创建人名称
            "m": "message_type",  # 消息类型，对应移动端A类消息推送message_type对应值
            "n": "subtitle",  # 子标题
            "o": "repeat_id",  # 循环周期id
            "p": "changes",  # 变更内容
            "q": "batch_id",  # 批量id
            "r": "batch_type",  # 批量类型,1->create,2->accept,3->refuse,4->finish
            "s": "is_query_comment",  # 是否查询评论
            "t": "is_accept",  # 是否已接受，事项message_type == 1使用
        }
        parse_code = dict()
        for key, value in data.items():
            if key in mapping:
                parse_code[mapping[key]] = value
        return parse_code

    async def send_heartbeat(self, websocket: websockets.WebSocketClientProtocol):
        # 发送心跳包
        while True:
            try:
                print("发送心跳包")
                await asyncio.sleep(self.heartbeat)
                await websocket.send(struct.pack(">I", 1))
            except websockets.ConnectionClosed:
                break
            except Exception as e:
                print(f"心跳包: {e}")

    async def start_listener(self):
        async with websockets.connect(self.ws_url) as websocket:
            heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
            # 存储当前websocket对象, 连接池和连接状态
            self.current_ws_obj[self.ws_flag] = dict()
            self.current_ws_obj[self.ws_flag]["connect"] = websocket
            self.current_ws_obj[self.ws_flag]["status"] = True
            try:
                await self.receive_message(websocket)
            except websockets.ConnectionClosed:
                logger.warning("连接已断开")
            finally:
                heartbeat_task.cancel()
                await websocket.close()
                self.current_ws_obj[self.ws_flag]["status"] = False
                # 清理当前websocket对象, 防止无法垃圾回收
                self.current_ws_obj[self.ws_flag]["connect"] = None

    async def receive_message(self, websocket: websockets.WebSocketClientProtocol):
        while True:
            if (datetime.now() - self.last_activity_time).seconds > 300:
                logger.warning("超时未操作，断开连接")
                break
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                self.last_activity_time = datetime.now()
                if type(message) == str and message == "0":
                    continue
                if not message:
                    continue
                data = msgpack.unpackb(message, raw=False)
                await self.handle_message(data)
            except asyncio.TimeoutError:
                # 无消息无需处理, 继续等待
                continue

    async def handle_message(self, ws_data: dict) -> None:
        """处理消息, 与self.current_case做比较"""
        data = self.parse_fx_ws(ws_data)
        if self.current_case["case_id"] == 0:
            return
        if self.current_case["ws_code"] == data.get("code"):
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
                            await self.normal_message(data)
                            return
                else:
                    await self.normal_message(data)
                    return
        else:
            await self.normal_message(data)

    async def success_message(self, data: dict):
        """发送成功消息"""
        await WsService.ws_notify_ws_test([self.operator], data, True)
        self.clear_case()

    async def normal_message(self, data: dict):
        await WsService.ws_notify_ws_test([self.operator], data, False)

    def clear_case(self):
        self.current_case = {
            "case_id": 0,
            "ws_code": 0,
            "json_exp": "",
            "expected": "",
        }

    async def add_case(self, case_id: int):
        case_info = await WsCaseCrud.query_case_as_dict(case_id)
        self.current_case = case_info
        # self.current_case = case_data

    async def disconnect(self):
        if self.current_ws_obj:
            await self.current_ws_obj[self.ws_flag].close()
