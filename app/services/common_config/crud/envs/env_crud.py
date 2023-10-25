# coding=utf-8
"""
File: env_crud.py
Author: bot
Created: 2023/10/23
Description:
"""


from sqlalchemy import text, and_, select

from app.core.db_connector import async_session
from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_430_env import NEW_ENV_FAIL
from app.models.common_config.env_settings import EnvModel
from app.models.apicase.api_path import ApiPathModel
from app.models.apicase.api_headers import ApiHeadersModel
from app.models.api_settings.suffix_settings import SuffixModel
from app.models.api_settings.assert_settings import AssertModel
from app.services.common_config.schema.env.news import RequestEnvNew
from app.handler.db_tool.db_bulk import DatabaseBulk


class EnvCrud:
    @staticmethod
    async def env_exists_by_id(env_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS(SELECT 1 FROM envs WHERE env_id = :env_id AND deleted_at = 0) AS is_exists;
            """
            )
            result = await session.execute(smtm, {"env_id": env_id})
            return result.scalars().first()

    @staticmethod
    async def env_exists_by_name(name: str):
        async with async_session() as session:
            smtm = text(
                """
                    SELECT EXISTS(SELECT 1 FROM envs WHERE name = :name AND deleted_at = 0) AS is_exists;
                """
            )
            result = await session.execute(smtm, {"name": name})
            return result.scalars().first()

    @staticmethod
    async def add_env_form(form: RequestEnvNew, creator: int):
        async with async_session() as session:
            async with session.begin():
                try:
                    env = EnvModel(name=form.name, domain=form.domain, create_user=creator)
                    session.add(env)
                    await session.flush()
                    session.expunge(env)
                    # 添加Query绑定
                    if form.query_info:
                        await DatabaseBulk.bulk_add_data(session, ApiPathModel, form.query_info)
                    if form.headers_info:
                        await DatabaseBulk.bulk_add_data(session, ApiHeadersModel, form.headers_info)
                    if form.suffix_info:
                        await DatabaseBulk.bulk_add_data(session, SuffixModel, form.suffix_info)
                    if form.assert_info:
                        await DatabaseBulk.bulk_add_data(session, AssertModel, form.assert_info)
                    await session.commit()

                except Exception as e:
                    await session.rollback()
                    raise CustomException(NEW_ENV_FAIL, addition_info=str(e))

    @staticmethod
    async def get_env_list(page: int, page_size: int, operator: int):
        offset = (page - 1) * page_size
        async with async_session() as session:
            smtm_total = text(
                """
                SELECT COUNT(*) as total FROM envs WHERE create_user = :operator AND deleted_at = 0;
                """
            )
            total = await session.execute(smtm_total, {"operator": operator})
            smtm = (
                select(EnvModel)
                .where(and_(EnvModel.create_user == operator, EnvModel.deleted_at == 0))
                .limit(page_size)
                .offset(offset)
            )
            result = await session.execute(smtm)
            return result.scalars().all(), total.scalars().first()

    @staticmethod
    async def get_env_detail(env_id: int):
        async with async_session() as session:
            smtm_e = await session.execute(
                select(EnvModel).where(and_(EnvModel.env_id == env_id, EnvModel.deleted_at == 0))
            )
            smtm_q = await session.execute(
                select(ApiPathModel).where(and_(ApiPathModel.env_id == env_id, ApiPathModel.deleted_at == 0))
            )
            smtm_h = await session.execute(
                select(ApiHeadersModel).where(and_(ApiHeadersModel.env_id == env_id, ApiHeadersModel.deleted_at == 0))
            )
            smtm_s = await session.execute(
                select(SuffixModel).where(and_(SuffixModel.env_id == env_id, SuffixModel.deleted_at == 0))
            )
            smtm_a = await session.execute(
                select(AssertModel).where(and_(AssertModel.env_id == env_id, AssertModel.deleted_at == 0))
            )
            return (
                smtm_e.scalars().first(),
                smtm_q.scalars().all(),
                smtm_h.scalars().all(),
                smtm_s.scalars().all(),
                smtm_a.scalars().all(),
            )

    @staticmethod
    async def get_env_dependencies(env_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT
                    e.env_id,
                    IFNULL(GROUP_CONCAT(DISTINCT p.path_id ORDER BY p.path_id), '') AS path_ids,
                    IFNULL(GROUP_CONCAT(DISTINCT h.header_id ORDER BY h.header_id), '') AS header_ids,
                    IFNULL(GROUP_CONCAT(DISTINCT s.suffix_id ORDER BY s.suffix_id), '') AS suffix_ids,
                    IFNULL(GROUP_CONCAT(DISTINCT a.assert_id ORDER BY a.assert_id), '') AS assert_ids
                FROM
                    env AS e
                LEFT JOIN
                    (
                        SELECT
                            env_id,
                            path_id
                        FROM
                            api_path
                        WHERE
                            deleted_at = 0
                    ) AS p ON e.env_id = p.env_id
                LEFT JOIN
                    (
                        SELECT
                            env_id,
                            header_id
                        FROM
                            api_headers
                        WHERE
                            deleted_at = 0
                    ) AS h ON e.env_id = h.env_id
                LEFT JOIN
                    (
                        SELECT
                            env_id,
                            suffix_id
                        FROM
                            common_suffix
                        WHERE
                            deleted_at = 0
                    ) AS s ON e.env_id = s.env_id
                LEFT JOIN
                    (
                        SELECT
                            env_id,
                            assert_id
                        FROM
                            common_assert
                        WHERE
                            deleted_at = 0
                    ) AS a ON e.env_id = a.env_id
                WHERE
                    e.env_id = :env_id AND e.deleted_at = 0
                GROUP BY
                    e.env_id;
            """
            )
            result = await session.execute(smtm, {"env_id": env_id})
            return result.first()
