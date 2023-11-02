# coding=utf-8
"""
File: result_crud.py
Author: bot
Created: 2023/11/2
Description:
"""
from app.handler.case.schemas import AsyncResponseSchema
from app.models.api_case.api_result import ApiCaseResultModel
from app.core.db_connector import async_session
from app.services.api_case.api_result.schema.result.info import OutCaseLog


class ApiResultCrud:
    @staticmethod
    async def add_case_result(
        report_id: str,
        case_id: int,
        result: AsyncResponseSchema,
        run_log: OutCaseLog,
        assert_result: bool,
    ):
        async with async_session() as session:
            async with session.begin():
                result = ApiCaseResultModel(
                    report_id=report_id,
                    case_id=case_id,
                    result=result.dict(),
                    run_log=run_log.dict(),
                    assert_result=assert_result,
                    elapsed=result.elapsed,
                )
                session.add(result)
                await session.flush()
                session.expunge(result)
                return result.id
