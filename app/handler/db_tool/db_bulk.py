# coding=utf-8
"""
File: db_bulk.py
Author: bot
Created: 2023/7/28
Description: 批量操作
"""
import inspect
from datetime import datetime
import json

from typing import List, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.handler.serializer.response_serializer import C137Response
from app.models.api_case.api_case import ApiCaseModel


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
        print(changed_var)
        return changed_var

    @staticmethod
    def delete_model(model_instance, operator=None):
        """删除"""
        model_instance.deleted_at = int(datetime.now().timestamp())
        # model_instance.updated_at = datetime.now()
        if operator and hasattr(model_instance, "update_user"):
            setattr(model_instance, "update_user", operator)

    @staticmethod
    async def deleted_model_with_session(session: AsyncSession, model, primary_key: List[int], operator: int):
        """
        软删除
        primary_key可能等于整型,'',或者是逗号分隔的字符串
        """
        if not primary_key:
            return
        for ids in primary_key:
            field_name = model.__table__.primary_key.columns.keys()[0]
            smtm = await session.execute(select(model).where(model.__table__.c[field_name] == ids))
            obj = smtm.scalars().first()
            if obj:
                obj.deleted_at = int(datetime.now().timestamp())
                obj.update_user = operator

    @staticmethod
    async def bulk_add_data(session, model, data: List[BaseModel], *ignore_key, **addition_data):
        """批量添加数据"""
        serialized_data_list = []
        for item in data:
            serialized_data = item.dict()
            if ignore_key:
                for key in ignore_key:
                    if key in serialized_data:
                        serialized_data.pop(key)
            if addition_data:
                for key, value in addition_data.items():
                    serialized_data[key] = (
                        json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
                    )
                serialized_data_list.append(serialized_data)
        if serialized_data_list:
            await session.execute(model.__table__.insert(), serialized_data_list)

    @staticmethod
    def serializer_comma_string(comma_string: str, is_int: bool = False) -> list:
        """将sql concat的字符串转换为列表"""
        if "," in comma_string:
            if is_int:
                check_list = [int(i) for i in comma_string.split(",") if i]
            else:
                check_list = [i for i in comma_string.split(",") if i]
        else:
            if is_int:
                check_list = [int(comma_string)]
            else:
                check_list = [comma_string]
        return check_list
