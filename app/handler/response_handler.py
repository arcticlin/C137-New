# coding=utf-8
"""
@author: linpang
@file: response_handler.py
@time: 2023/3/15 14:29
@description: 
"""
import inspect
from datetime import datetime
from typing import Any, List, Union, Dict, Sequence
from enum import Enum

from starlette.responses import JSONResponse


class C137Response:
    @staticmethod
    def orm_to_dict(obj: Any, *args) -> dict:
        """处理Sqlalchemy的Orm模型转Dict"""
        if getattr(obj, "__table__", None) is None:
            return obj

        orm_data = dict()
        for c in obj.__table__.columns:
            val = getattr(obj, c.name)
            if c.name in args:
                continue

            if isinstance(val, datetime):
                orm_data.__setitem__(c.name, int(val.timestamp()))
            elif isinstance(val, Enum):
                orm_data.__setitem__(c.name, val.value)
            elif val is None:
                continue
            else:
                orm_data.__setitem__(c.name, val)

        return orm_data

    @staticmethod
    def orm_with_list(obj: Sequence[Any], *args):
        return [C137Response.orm_to_dict(x, *args) for x in obj]

    @staticmethod
    def success(
        code: int = 0,
        data: Union[List, Dict] = None,
        message: str = "操作成功",
        total: int = None,
        headers: dict = None,
    ):
        response = dict()
        response.__setitem__("code", code)
        if data is not None:
            orm_translator = (
                C137Response.orm_with_list(data) if isinstance(data, list) else C137Response.orm_to_dict(data)
            )
            response.__setitem__("data", orm_translator)
        # else:
        #     if isinstance(data, dict):
        #         response.__setitem__("data", {})
        #     elif isinstance(data, list):
        #         response.__setitem__("data", [])
        #     else:
        #         response.__setitem__("data", None)
        # if message is not None:
        response.__setitem__("message", message)
        # if total is not None:
        response.__setitem__("total", total)
        if headers is not None:
            return JSONResponse(content=response, headers=headers)
        return response

    @staticmethod
    def join_username_to_model(obj: Any, user_name: str, addition_key_name: str):
        model_dict = C137Response.orm_to_dict(obj)
        model_dict[addition_key_name] = user_name
        return model_dict
