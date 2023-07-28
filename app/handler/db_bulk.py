# coding=utf-8
"""
File: db_bulk.py
Author: bot
Created: 2023/7/28
Description: 批量操作
"""


from datetime import datetime
import json
from typing import List
from pydantic import BaseModel


class DatabaseBulk:
    @staticmethod
    def update_model(model_instance, source: dict, operator=None) -> List:
        """更新"""
        changed_var = []
        for var, value in source.items():
            if value is None:
                continue
            value = json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
            if getattr(model_instance, var) != value:
                changed_var.append(var)
                setattr(model_instance, var, value)
        if operator and hasattr(model_instance, "update_user"):
            changed_var.append("update_user")
            setattr(model_instance, "update_user", operator)

        # setattr(model_instance, "update_at", datetime.now())
        # changed_var.append("update_at")

        return changed_var

    @staticmethod
    def delete_model(model_instance, operator=None):
        """删除"""
        model_instance.deleted_at = int(datetime.now().timestamp())
        # model_instance.updated_at = datetime.now()
        if operator and hasattr(model_instance, "update_user"):
            setattr(model_instance, "update_user", operator)

    @staticmethod
    async def bulk_add_data(session, model, data: List[BaseModel], **addition_data):
        """批量添加数据"""
        serialized_data_list = []
        for item in data:
            serialized_data = item.dict()
            if addition_data:
                for key, value in addition_data.items():
                    serialized_data[key] = (
                        json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
                    )
                serialized_data_list.append(serialized_data)
        await session.execute(model.__table__.insert(), serialized_data_list)
