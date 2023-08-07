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
from sqlalchemy import text, select, and_
from app.models.api_settings.env_settings import EnvModel


class ApiCaseCrud:
    @staticmethod
    async def check_case_exists(directory_id: int, case_name: str, case_method: str) -> bool:
        async with async_session() as session:
            smtm = text(
                """
                SELECT
                    CASE
                        WHEN EXISTS (
                            SELECT 
                                1 
                            FROM 
                                api_case as ac
                            WHERE 
                                ac.directory_id = :directory_id 
                            AND 
                                ac.name = :case_name 
                            AND 
                                ac.method = :case_method 
                            AND 
                                ac.deleted_at = 0
                            ) 
                        THEN 1
                        ELSE 0
                    END AS result
            """
            )
            result = await session.execute(
                smtm, {"directory_id": directory_id, "case_name": case_name, "case_method": case_method}
            )
            return bool(result.scalars().first())

    @staticmethod
    async def query_case_detail(case_id: int):
        async with async_session() as session:
            smtm_c = await session.execute(
                select(ApiCaseModel).where(and_(ApiCaseModel.case_id == case_id, ApiCaseModel.deleted_at == 0))
            )
            smtm_p = await session.execute(
                select(ApiPathModel).where(and_(ApiPathModel.case_id == case_id, ApiPathModel.deleted_at == 0))
            )
            smtm_h = await session.execute(
                select(ApiHeadersModel).where(and_(ApiHeadersModel.case_id == case_id, ApiHeadersModel.deleted_at == 0))
            )

            return smtm_c.scalars().first(), smtm_p.scalars().all(), smtm_h.scalars().all()

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
                    SET deleted_at = :deleted_at, update_user = :update_user , updated_at = :updated_at
                    WHERE case_id = :case_id AND deleted_at = 0;
                    """
                )
                await session.execute(
                    smtm_case,
                    {
                        "deleted_at": int(datetime.now().timestamp()),
                        "update_user": operator,
                        "case_id": case_id,
                        "updated_at": datetime.now(),
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

    @staticmethod
    async def query_env_info(env_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT url FROM env WHERE env_id = :env_id AND deleted_at = 0;
                """
            )
            result = await session.execute(smtm, {"env_id": env_id})
            return result.scalars().first()
