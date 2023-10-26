# coding=utf-8
"""
File: case_crud.py
Author: bot
Created: 2023/10/26
Description:
"""
from typing import List

from app.core.db_connector import async_session
from sqlalchemy import and_, select, text, func

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_480_case import CASE_ADD_FAILED, CASE_DELETE_FAILED
from app.handler.db_tool.db_bulk import DatabaseBulk
from app.handler.serializer.response_serializer import C137Response
from app.models.apicase.api_case import ApiCaseModel
from app.models.apicase.api_path import ApiPathModel
from app.models.apicase.api_headers import ApiHeadersModel
from app.models.api_settings.suffix_settings import SuffixModel
from app.models.api_settings.assert_settings import AssertModel
from app.models.api_settings.extract_settings import ExtractModel
from app.services.api_case_new.case.schema.info import OutCaseDetailInfo, OutCaseBasicInfo, OutCaseUrlInfo, \
    OutCaseBodyInfo
from app.services.api_case_new.case.schema.new import RequestApiCaseNew
from app.services.api_case_new.case_params.headers.schema.info import OutHeaderInfo
from app.services.api_case_new.case_params.query.schema.info import OutParamsInfo
from app.services.api_case_new.settings.asserts.schema.info import OutAssertInfo
from app.services.api_case_new.settings.extract.schema.info import OutExtractInfo
from app.services.api_case_new.settings.suffix.schema.info import OutCaseSuffixInfo


class ApiCaseCrud:
    @staticmethod
    async def query_name_exists_in_directory(name: str, method: str, directory_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM api_case WHERE name=:name AND method=:method AND directory_id=:directory_id AND deleted_at=0)
            """
            )
            result = await session.execute(smtm, {"name": name, "method": method, "directory_id": directory_id})
            return result.scalars().first()

    @staticmethod
    async def query_case_exists_by_id(case_id: int):
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (SELECT 1 FROM api_case WHERE case_id=:case_id AND deleted_at=0)
                """
            )
            result = await session.execute(smtm, {"case_id": case_id})
            return result.scalars().first()

    @staticmethod
    async def user_has_permission_delete(operator: int):
        pass

    @staticmethod
    async def add_case(form: RequestApiCaseNew, creator: int):
        async with async_session() as session:
            async with session.begin():
                try:
                    case = ApiCaseModel(
                        name=form.basic_info.name,
                        url=form.url_info.url,
                        method=form.url_info.method,
                        directory_id=form.directory_id,
                        create_user=creator,
                        status=form.basic_info.status,
                        priority=form.basic_info.priority,
                        case_type=form.basic_info.case_type,
                        body_type=form.body_info.body_type,
                        body=form.body_info.body,
                        request_type=form.basic_info.request_type,
                    )
                    session.add(case)
                    await session.flush()
                    session.expunge(case)
                    case_id = case.case_id
                    await DatabaseBulk.bulk_add_data(
                        session,
                        ApiPathModel,
                        form.path_info + form.query_info,
                        create_user=creator,
                        case_id=case_id,
                    )

                    await DatabaseBulk.bulk_add_data(
                        session, ApiHeadersModel, form.header_info, create_user=creator, case_id=case_id
                    )
                    await DatabaseBulk.bulk_add_data(
                        session, SuffixModel, form.prefix_info + form.suffix_info, create_user=creator, case_id=case_id
                    )

                    await DatabaseBulk.bulk_add_data(
                        session, AssertModel, form.assert_info, create_user=creator, case_id=case_id
                    )
                    await DatabaseBulk.bulk_add_data(
                        session, ExtractModel, form.extract_info, create_user=creator, case_id=case_id
                    )

                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise CustomException(CASE_ADD_FAILED, f"{e}")
            return case_id

    @staticmethod
    async def delete_case(case_id: int, operator: int):
        case_ids, path_ids, header_ids, suffix_ids, assert_ids, extract_ids = await ApiCaseCrud.get_case_dependencies(case_id)
        async with async_session() as session:
            try:
                await DatabaseBulk.deleted_model_with_session(session, ApiCaseModel, case_ids, operator)
                await DatabaseBulk.deleted_model_with_session(session, ApiPathModel, path_ids, operator)
                await DatabaseBulk.deleted_model_with_session(session, ApiHeadersModel, header_ids, operator)
                await DatabaseBulk.deleted_model_with_session(session, SuffixModel, suffix_ids, operator)
                await DatabaseBulk.deleted_model_with_session(session, AssertModel, assert_ids, operator)
                await DatabaseBulk.deleted_model_with_session(session, ExtractModel, extract_ids, operator)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise CustomException(CASE_DELETE_FAILED, f"{e}")

    @staticmethod
    async def get_case_dependencies(case_id: int) -> List[List[int]]:
        """
        获取用例的依赖数据, 用于删除用例时, 删除依赖数据
        1. 用例表.case_id = case_id
        2. 路径表.case_id = case_id
        3. 请求头表.case_id = case_id
        4. 前置后置表.case_id = case_id
        5. 断言表.case_id = case_id
        6. 提取表.case_id = case_id
        """
        async with async_session() as session:
            async with session.begin():
                smtm = text(
                    """
                    SELECT
                        c.case_id,
                        IFNULL(GROUP_CONCAT(DISTINCT p.path_id), '') AS path_ids,
                        IFNULL(GROUP_CONCAT(DISTINCT h.header_id), '') AS header_ids,
                        IFNULL(GROUP_CONCAT(DISTINCT s.suffix_id), '') AS suffix_ids,
                        IFNULL(GROUP_CONCAT(DISTINCT a.assert_id), '') AS assert_ids,
                        IFNULL(GROUP_CONCAT(DISTINCT e.extract_id), '') AS extract_ids
                        
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
                    LEFT JOIN
                        (
                            SELECT
                                case_id,
                                suffix_id
                            FROM
                                common_suffix
                            WHERE
                                deleted_at = 0
                        ) AS s ON c.case_id = s.case_id
                    LEFT JOIN
                        (
                            SELECT
                                case_id,
                                assert_id
                            FROM
                                common_assert
                            WHERE
                                deleted_at = 0
                        ) AS a ON c.case_id = a.assert_id
                    LEFT JOIN
                        (
                            SELECT
                                case_id,
                                extract_id
                            FROM
                                common_extract
                            WHERE
                                deleted_at = 0
                        ) AS e ON c.case_id = e.extract_id
                    WHERE
                        c.case_id = :case_id AND c.deleted_at = 0
                    GROUP BY
                        c.case_id;
                """
                )
                execute = await session.execute(smtm, {"case_id": case_id})
                result = execute.first()
                coverts = []
                for ele in result:
                    if ele:
                        if isinstance(ele, int):
                            coverts.append([ele])
                        else:
                            if "," in ele:
                                coverts.append([int(x) for x in ele.split(",")])
                            else:
                                coverts.append([int(ele)])
                    else:
                        coverts.append([])
                return coverts

    @staticmethod
    async def query_case_detail(case_id: int) -> OutCaseDetailInfo:
        async with async_session() as session:
            smtm_case = await session.execute(
                select(ApiCaseModel).where(and_(ApiCaseModel.case_id == case_id, ApiCaseModel.deleted_at == 0))
            )
            smtm_params = await session.execute(
                select(ApiPathModel).where(and_(ApiPathModel.case_id == case_id, ApiPathModel.deleted_at == 0))
            )
            smtm_headers = await session.execute(
                select(ApiHeadersModel).where(and_(ApiHeadersModel.case_id == case_id, ApiHeadersModel.deleted_at == 0))
            )
            smtm_suffix = await session.execute(
                select(SuffixModel).where(and_(SuffixModel.case_id == case_id, SuffixModel.deleted_at == 0))
            )
            smtm_assert = await session.execute(
                select(AssertModel).where(and_(AssertModel.case_id == case_id, AssertModel.deleted_at == 0))
            )
            smtm_extract = await session.execute(
                select(ExtractModel).where(and_(ExtractModel.case_id == case_id, ExtractModel.deleted_at == 0))
            )
            result_case = smtm_case.scalars().first()
            result_params = smtm_params.scalars().all()
            result_headers = smtm_headers.scalars().all()
            result_suffix = smtm_suffix.scalars().all()
            result_assert = smtm_assert.scalars().all()
            result_extract = smtm_extract.scalars().all()

            orm_basic_info = C137Response.orm_to_pydantic(result_case, OutCaseBasicInfo)
            orm_url_info = C137Response.orm_to_pydantic(result_case, OutCaseUrlInfo)
            orm_body_info = C137Response.orm_to_pydantic(result_case, OutCaseBodyInfo)

            orm_query_info = [C137Response.orm_to_pydantic(x, OutParamsInfo) for x in result_params if x.types == 2]
            orm_path_info = [C137Response.orm_to_pydantic(x, OutParamsInfo) for x in result_params if x.types == 1]
            orm_header_info = [C137Response.orm_to_pydantic(x, OutHeaderInfo) for x in result_headers]
            orm_prefix_info = [C137Response.orm_to_pydantic(x, OutCaseSuffixInfo) for x in result_suffix if x.suffix_type == 1]
            orm_suffix_info = [C137Response.orm_to_pydantic(x, OutCaseSuffixInfo) for x in result_suffix if x.suffix_type == 2]
            orm_assert_info = [C137Response.orm_to_pydantic(x, OutAssertInfo) for x in result_assert]
            orm_extract_info = [C137Response.orm_to_pydantic(x, OutExtractInfo) for x in result_extract]

            return OutCaseDetailInfo(
                case_id=result_case.case_id,
                directory_id=result_case.directory_id,
                basic_info=orm_basic_info,
                url_info=orm_url_info,
                body_info=orm_body_info,
                query_info=orm_query_info,
                path_info=orm_path_info,
                header_info=orm_header_info,
                prefix_info=orm_prefix_info,
                suffix_info=orm_suffix_info,
                assert_info=orm_assert_info,
                extract_info=orm_extract_info,
            )
