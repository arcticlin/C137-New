# coding=utf-8
"""
File: response_schema.py
Author: bot
Created: 2023/7/25
Description:
"""
from pydantic import BaseModel, Field
from typing import Union, Dict, List


class CommonResponse(BaseModel):
    code: int
    message: str = None
    error_msg: str = None
    total: int = None
    data: Union[Dict, List] = None

    # def dict(self, *args, **kwargs):
    #     return BaseModel.model_dump(self, *args, **kwargs, exclude_none=True)
