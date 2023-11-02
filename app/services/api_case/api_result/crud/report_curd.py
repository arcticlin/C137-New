# coding=utf-8
"""
File: report_curd.py
Author: bot
Created: 2023/11/2
Description:
"""
from sqlalchemy import select, and_

from app.handler.db_tool.db_bulk import DatabaseBulk
from app.handler.serializer.response_serializer import C137Response
from app.models.api_case.api_report import ApiReportModel
from app.core.db_connector import async_session
from app.services.api_case.api_result.schema.report.new import UpdateReportData


class ApiReportCrud:
    @staticmethod
    async def init_report(trace_id: str, case_count: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                report = ApiReportModel(
                    report_id=trace_id,
                    total=case_count,
                    create_user=operator,
                )
                session.add(report)
                await session.flush()
                session.expunge(report)
                return report.report_id

    @staticmethod
    async def update_report_status(report_id: str, status: int):
        async with async_session() as session:
            async with session.begin():
                await session.query(ApiReportModel).filter(
                    ApiReportModel.report_id == report_id, ApiReportModel.deleted_at == 0
                ).update({"status": status})

    @staticmethod
    async def update_report_data(report_id: str, data: UpdateReportData):
        async with async_session() as session:
            smtm = await session.execute(
                select(ApiReportModel).where(
                    and_(ApiReportModel.report_id == report_id, ApiReportModel.deleted_at == 0)
                )
            )
            report = smtm.scalars().first()
            DatabaseBulk.update_model(report, data.dict())
            await session.commit()
            await session.flush()
