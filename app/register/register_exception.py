# coding=utf-8
"""
File: register_exception.py
Author: bot
Created: 2023/7/25
Description:
"""
from fastapi import FastAPI
from app.exceptions.commom_exception import validation_response_exp_handler
from fastapi.exceptions import ResponseValidationError


def register_exception(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=ResponseValidationError,
        handler=validation_response_exp_handler,
    )
