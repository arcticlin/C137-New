# coding=utf-8
"""
File: ws_plan_services.py
Author: bot
Created: 2023/12/4
Description:
"""

from typing import List

from app.services.ws_test.crud.ws_plan.ws_plan_crud import WsPlanCrud


class WsPlanService:
    @staticmethod
    async def get_plan_list(
        page: int = 1,
        page_size: int = 20,
        filter_user: List[int] = None,
        filter_name: str = None,
        filter_status: List[int] = None,
        filter_project: List[int] = None,
    ):
        result, total = await WsPlanCrud.get_plan_list(
            page=page,
            page_size=page_size,
            filter_user=filter_user,
            filter_name=filter_name,
            filter_status=filter_status,
            filter_project=filter_project,
        )
        return result, total
