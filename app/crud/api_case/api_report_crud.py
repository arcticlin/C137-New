# coding=utf-8
"""
File: api_report_crud.py
Author: bot
Created: 2023/9/27
Description:
"""
from sqlalchemy import select, and_

from app.handler.db_tool.db_bulk import DatabaseBulk
from app.models.apicase.api_report import ApiReportModel

from app.models.apicase.api_result import ApiCaseResultModel
from app.core.db_connector import async_session


class ApiReportCrud:
    @staticmethod
    async def init_api_report(report_id: str, total: int):
        async with async_session() as session:
            async with session.begin():
                report = ApiReportModel(report_id, total, 0, 0, 0, 0, 0)
                session.add(report)
                await session.flush()
                return report.id

    @staticmethod
    async def update_api_report(id: str, report_result: dict):
        async with async_session() as session:
            async with session.begin():
                report = await session.execute(select(ApiReportModel).where(and_(ApiReportModel.id == id)))
                report_ = report.scalars().first()
                DatabaseBulk.update_model(report_, report_result)

                await session.flush()


class ApiResultCrud:
    @staticmethod
    async def insert_api_result(report_id: str, case_id: int, result: dict):
        async with async_session() as session:
            async with session.begin():
                report = ApiCaseResultModel(case_id, report_id, result)
                session.add(report)
                await session.flush()
                return report.id
