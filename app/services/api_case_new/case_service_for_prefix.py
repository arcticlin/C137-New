# coding=utf-8
"""
File: case_service_for_prefix.py
Author: bot
Created: 2023/10/31
Description:
"""
from typing import Union

from app.crud.api_case.api_case_crud import ApiCaseCrud
from app.handler.redis.api_redis_new import ApiRedis
from app.services.api_case_new.case.schema.info import OutCaseDetailInfo
from app.services.api_case_new.settings.suffix.schema.info import DebugCaseSuffixInfo, OutCaseSuffixInfo

SuffixInfo = Union[DebugCaseSuffixInfo, OutCaseSuffixInfo]


class CasePrefixService:
    def __init__(self, rds: ApiRedis):
        self.rds = rds

    async def run_prefix_case(self, case_form: OutCaseDetailInfo, prefix_form: SuffixInfo):
        pass
