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
from fastapi import status
from fastapi.encoders import jsonable_encoder
from app.utils.logger import Log

log = Log("commom_exception")


async def validation_response_exp_handler(request, exc: ResponseValidationError):
    log.error(
        f"ResponseValidationError: {json.dumps(exc.errors(), ensure_ascii=False, indent=2)}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {"code": 40500, "message": "参数错误", "error_msg": exc.errors()}
        ),
    )
