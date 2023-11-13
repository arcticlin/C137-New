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

from typing import List, Union, Tuple
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

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
        """
        if not primary_key or len(primary_key) == 0:
            return
        for ids in primary_key:
            field_name = model.__table__.primary_key.columns.keys()[0]
            smtm = await session.execute(select(model).where(model.__table__.c[field_name] == ids))
            obj = smtm.scalars().first()
            if obj:
                obj.deleted_at = int(datetime.now().timestamp())
                obj.update_user = operator

    @staticmethod
    async def update_model_with_session(
        session: AsyncSession, model, source_data: List[dict], primary_field_name: str, operator: int
    ):
        if not source_data or len(source_data) == 0:
            return
        for d in source_data:
            model_id = d[primary_field_name]
            smtm = await session.execute(
                select(model).where(
                    and_(model.__table__.c[primary_field_name] == model_id, model.__table__.c["deleted_at"] == 0)
                )
            )
            obj = smtm.scalars().first()
            if obj:
                DatabaseBulk.update_model(obj, d, operator)

    @staticmethod
    async def add_model_with_session(session: AsyncSession, model, source_data: List[dict], operator: int, **kwargs):
        serialized_data_list = []
        if not source_data or len(source_data) == 0:
            return
        for d in source_data:
            d["create_user"] = operator
            d["update_user"] = operator
            d["deleted_at"] = 0
            if kwargs.get("env_id"):
                d["env_id"] = kwargs.get("env_id")
            elif kwargs.get("case_id"):
                d["case_id"] = kwargs.get("case_id")
            serialized_data_list.append(d)
        if serialized_data_list:
            await session.execute(model.__table__.insert(), serialized_data_list)

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

    @staticmethod
    def get_delete_ids(existed_ids: List[int], new_form: List[dict], primary_key: str) -> List[int]:
        """获取删除的id"""
        form_ids = [i[primary_key] for i in new_form if i.__contains__(primary_key)]
        return [i for i in existed_ids if i not in form_ids]

    @staticmethod
    def parse_form_data(
        existed_ids: List[int], form_data: List[BaseModel], primary_key: str
    ) -> Tuple[List[int], List[dict], List[dict]]:
        """
        解析表单数据, 返回元祖(需删除, 需新增, 需修改)
        """
        serialized_data_list = [i.dict() for i in form_data]

        form_ids = [i[primary_key] for i in serialized_data_list if i.__contains__(primary_key)]

        # 需删除的IDS
        delete_ids = [i for i in existed_ids if i not in form_ids]

        # 需修改的数据
        update_data = [i for i in serialized_data_list if i.__contains__(primary_key) and i[primary_key] in existed_ids]

        # 需新增的数据
        add_data = [i for i in serialized_data_list if i.__contains__(primary_key) and i[primary_key] is None]

        return delete_ids, add_data, update_data
