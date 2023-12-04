# coding=utf-8
"""
File: ws_plan_crud.py
Author: bot
Created: 2023/12/4
Description:
"""
from app.core.db_connector import async_session
from sqlalchemy import select, and_, or_, func
from app.models.ws_test.ws_plan import WsPlanModel
from typing import List


class WsPlanCrud:
    @staticmethod
    async def get_plan_list(
        page: int = 1,
        page_size: int = 20,
        filter_user: List[int] = None,
        filter_name: str = None,
        filter_status: List[int] = None,
        filter_project: List[int] = None,
    ):
        offset = (page - 1) * page_size
        async with async_session() as session:
            _list = [WsPlanModel.deleted_at == 0]
            if filter_user:
                _list.append(WsPlanModel.create_user.in_(filter_user))
            if filter_name:
                _list.append(WsPlanModel.name.like(f"%{filter_name}%"))
            if filter_status:
                _list.append(WsPlanModel.status.in_(filter_status))
            if filter_project:
                _list.append(WsPlanModel.project_id.in_(filter_project))
            plan_count = await session.execute(select(func.count(WsPlanModel.plan_id)).where(*_list))
            count = plan_count.scalars().first()
            smtm = await session.execute(select(WsPlanModel).where(*_list).offset(offset).limit(page_size))
            result = smtm.scalars().all()
            return result, count
