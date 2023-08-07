# coding=utf-8
"""
File: assert_crud.py
Author: bot
Created: 2023/8/7
Description:
"""
from typing import List

from app.models.api_settings.assert_settings import AssertModel


class AssertCurd:
    @staticmethod
    async def execute_assert_equal(assert_src: str, assert_value: str, is_equal: bool):
        pass

    @staticmethod
    async def execute_assert_ge(assert_src: str, assert_value: str, is_ge: bool):
        pass

    @staticmethod
    async def execute_assert_in_list(assert_src: str, assert_value: List, is_in: bool):
        pass

    @staticmethod
    async def execute_assert_contain(assert_src: str, assert_value: str, is_contain: bool):
        pass

    @staticmethod
    async def execute_assert_start_with(assert_src: str, assert_value: str, is_start_with: bool):
        pass

    @staticmethod
    async def execute_assert_re(assert_src: str, assert_exp: str):
        pass

    @staticmethod
    async def execute_assert_json_path(assert_src: str, assert_exp: str):
        pass
