# coding=utf-8
"""
File: commom_exception.py
Author: bot
Created: 2023/7/25
Description:
"""
import json

from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi import status, Request
from fastapi.encoders import jsonable_encoder
from app.utils.new_logger import logger


class CustomException(Exception):
    def __init__(self, exception_error: tuple[int, int, str]) -> None:
        self.status_code = exception_error[0]
        self.internal_code = exception_error[1]
        self.error_message = exception_error[2]

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.error_message!r})"


async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"请求异常: {json.dumps(exc.error_message, ensure_ascii=False, indent=2)}")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"code": exc.internal_code, "error_msg": f"{exc.error_message}"}),
    )


async def validation_response_exp_handler(request, exc: ResponseValidationError):
    logger.error(f"响应校验异常: {json.dumps(exc.errors(), ensure_ascii=False, indent=2)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"code": 40500, "message": "参数错误", "error_msg": exc.errors()}),
    )
