# coding=utf-8
"""
File: response_schema.py
Author: bot
Created: 2023/7/25
Description:
"""
from pydantic import BaseModel, Field
from typing import Union, Dict, List, Optional


class CommonResponse(BaseModel):
    # model_config = ConfigDict(extra="ignore", ignored_types=(type(None),))

    code: int
    message: Optional[str] = Field(None, description="返回信息")
    error_msg: Optional[str] = Field(None, description="错误信息")
    total: Optional[int] = Field(None, description="统计次数")
    data: Optional[Union[Dict, List]] = Field(None, description="返回data")

    def dict(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return BaseModel.dict(self, *args, **kwargs)
