# coding=utf-8
"""
File: client_store.py
Author: bot
Created: 2023/9/19
Description:
"""
from typing import Set
from fastapi import WebSocket

connected_clients: Set[WebSocket] = set()
