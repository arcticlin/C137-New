# coding=utf-8
"""
File: flyele_token.py
Author: bot
Created: 2023/7/26
Description:
"""
from fastapi.security import APIKeyHeader
from fastapi import Depends


class FlyeleToken:
    oauth_schema = APIKeyHeader(name="Authorization", auto_error=False)

    async def __call__(self, token: str = Depends(oauth_schema)):
        return {"accept": "application/json", "authorization": f"{token}"}
