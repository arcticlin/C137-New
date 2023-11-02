# coding=utf-8
"""
File: info.py
Author: bot
Created: 2023/11/2
Description:
"""
from typing import List

from pydantic import BaseModel, Field

from app.handler.case.schemas import AsyncResponseSchema
from app.services.api_case.settings.asserts.schema.info import OutAssertResult


class OutCaseLog(BaseModel):
    var: dict
    log: dict


class OutCaseRun(BaseModel):
    case_id: int
    response: AsyncResponseSchema
    case_log: OutCaseLog
    assert_result: bool
    # case_assert: List[OutAssertResult]
    # env_assert: List[OutAssertResult]
