# coding=utf-8
"""
File: cases_handler.py
Author: bot
Created: 2023/8/8
Description:
"""
from app.crud.api_case.api_case_crud import ApiCaseCrud


class CaseHandler:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id

    @staticmethod
    async def get_env_url(env_id: int) -> str:
        """
        获取环境URL
        """
        return await ApiCaseCrud.query_env_info(env_id)

    async def script_executor(self, script_id: str):
        pass

    async def case_executor(self, env_url: str, case_id: int):
        pass
