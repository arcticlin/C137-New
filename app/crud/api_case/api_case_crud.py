# coding=utf-8
"""
File: api_case_crud.py
Author: bot
Created: 2023/8/2
Description:
"""
from datetime import datetime

from app.core.db_connector import async_session
from app.utils.new_logger import logger
from app.models.apicase.api_case import ApiCaseModel
from app.models.apicase.api_path import ApiPathModel
from app.models.apicase.api_headers import ApiHeadersModel
from app.schemas.api_case.api_path_schema import *
from app.schemas.api_case.api_headers_schema import *
from app.schemas.api_case.api_case_schema import *
from sqlalchemy import text, select


class ApiCaseCrud:
    @staticmethod
    async def get_case_dependencies(case_id: int):
        async with async_session() as session:
            async with session.begin():
                smtm = text(
                    """
                    SELECT
                        c.case_id,
                        IFNULL(GROUP_CONCAT(DISTINCT p.path_id ORDER BY p.path_id), '') AS path_ids,
                        IFNULL(GROUP_CONCAT(DISTINCT h.header_id ORDER BY h.header_id), '') AS header_ids
                    FROM
                        api_case AS c
                    LEFT JOIN
                        (
                            SELECT
                                case_id,
                                path_id
                            FROM
                                api_path
                            WHERE
                                deleted_at = 0
                        ) AS p ON c.case_id = p.case_id
                    LEFT JOIN
                        (
                            SELECT
                                case_id,
                                header_id
                            FROM
                                api_headers
                            WHERE
                                deleted_at = 0
                        ) AS h ON c.case_id = h.case_id
                    WHERE
                        c.case_id = :case_id AND c.deleted_at = 0
                    GROUP BY
                        c.case_id;
                """
                )
                result = await session.execute(smtm, {"case_id": case_id})
                return result.first()

    @staticmethod
    async def add_api_case(data: AddApiCaseRequest, creator: int):
        async with async_session() as session:
            async with session.begin():
                case = ApiCaseModel(**data.dict(), create_user=creator)
                session.add(case)
                await session.flush()
                return case.case_id

    @staticmethod
    async def delete_api_case(case_id: int, operator: int, path_id: List[int] = None, headers_id: List[int] = None):
        async with async_session() as session:
            async with session.begin():
                smtm_case = text(
                    """
                    UPDATE api_case 
                    SET deleted_at = :deleted_at, update_user = :update_user , updated_at = :updated_at
                    WHERE case_id = :case_id;
                """
                )
                smtm_path = text(
                    """
                    UPDATE api_path 
                    SET deleted_at = :deleted_at, update_user = :update_user , updated_at = :updated_at
                    WHERE case_id = :case_id AND deleted_at = 0;
                    """
                )
                smtm_header = text(
                    """
                    UPDATE api_headers 
                    SET deleted_at = :deleted_at, update_user = :update_user 
                    WHERE case_id = :case_id AND deleted_at = 0;
                    """
                )
                await session.execute(
                    smtm_case,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "update_user": operator,
                        "case_id": case_id,
                        "updated_at": datetime.now()
                    },
                )
                if path_id:
                    await session.execute(
                        smtm_path,
                        {
                            "deleted_at": int(datetime.now().timestamp()),
                            "update_user": operator,
                            "case_id": case_id,
                            "updated_at": datetime.now(),
                        },
                    )
                if headers_id:
                    await session.execute(
                        smtm_header,
                        {
                            "deleted_at": int(datetime.now().timestamp()),
                            "update_user": operator,
                            "case_id": case_id,
                            "updated_at": datetime.now(),
                        },
                    )
                await session.commit()
