# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/10/25
Description:
"""
import json

from pydantic import BaseModel, Field, validator
from loguru import logger

class OutHeaderInfo(BaseModel):
    header_id: int = Field(..., title="header id")
    key: str = Field(..., title="参数名")
    value_type: int = Field(..., title="参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON")
    value: str = Field(..., title="参数值")
    enable: bool = Field(True, title="是否启用")
    comment: str = Field(None, title="备注")

    @validator("value", pre=True, always=True)
    def convert_to_json(cls, v, values):
        # 参数值类型, 1: 字符串, 2: 数字, 3: 布尔值, 4: JSON
        try:
            vt = values.get("value_type")
            if vt == 1 and v:
                return v
            elif vt == 2 and v:
                return int(v)
            elif vt == 3 and v:
                if v.upper() == "TRUE":
                    return True
                elif v.upper == "FALSE":
                    return False
                elif v == "1":
                    return True
                else:
                    return False
            else:
                return json.loads(v)
        except json.JSONDecodeError:
            # 处理JSON解析错误，这里可以根据需要自定义处理逻辑
            logger.error(f"无法转换 value: {v}为{values.get('value_type')}类型")
            return v