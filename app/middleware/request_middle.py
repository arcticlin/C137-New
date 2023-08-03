# coding=utf-8
"""
File: request_middle.py
Author: bot
Created: 2023/8/2
Description:
"""
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.utils.new_logger import logger


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        logger.debug(
            f"{response.status_code} {request.client.host} {request.method} {request.url} " f"{end_time-start_time}"
        )
        return response
