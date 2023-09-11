# coding=utf-8
"""
File: suffix_crud.py
Author: bot
Created: 2023/8/7
Description:
"""
from datetime import datetime
from typing import List, Any, Sequence

from app.handler.db_bulk import DatabaseBulk
from app.models.api_settings.suffix_settings import SuffixModel
from app.core.db_connector import async_session
from sqlalchemy import text, select, and_, or_, Row, RowMapping, func
from app.exceptions.commom_exception import CustomException
from app.schemas.api_settings.suffix_schema import SchemaCaseSuffix


class SuffixCrud:
    @staticmethod
    async def get_prefix(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_or = [SuffixModel.deleted_at == 0, SuffixModel.suffix_type == 1]
            if env_id:
                smtm_or.append(SuffixModel.env_id == env_id)
            if case_id:
                smtm_or.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel).where(and_(*smtm_or)).order_by(SuffixModel.sort))

            return smtm.scalars().all()

    @staticmethod
    async def get_suffix(env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_or = [SuffixModel.deleted_at == 0, SuffixModel.suffix_type == 2]
            if env_id:
                smtm_or.append(SuffixModel.env_id == env_id)
            if case_id:
                smtm_or.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel).where(and_(*smtm_or)).order_by(SuffixModel.sort))

            return smtm.scalars().all()

    @staticmethod
    async def query_suffix_name_exists(suffix_type: int, name: str, env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_list = [SuffixModel.suffix_type == suffix_type, SuffixModel.name == name, SuffixModel.deleted_at == 0]
            if env_id:
                smtm_list.append(SuffixModel.env_id == env_id)
            else:
                smtm_list.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(SuffixModel.suffix_id).where(and_(*smtm_list)))
            return smtm.scalars().first()

    @staticmethod
    async def execute_script(script_id: int):
        pass

    @staticmethod
    async def execute_sql(sql_id: int, command: str, out_name: str):
        pass

    @staticmethod
    async def execute_redis(redis_id: int, command: str, out_name: str):
        pass

    @staticmethod
    async def execute_delay(delay: int):
        pass

    @staticmethod
    async def execute_case(case_id: int):
        pass

    @staticmethod
    async def current_suffix_count(suffix_type: int, env_id: int = None, case_id: int = None):
        async with async_session() as session:
            smtm_list = [SuffixModel.suffix_type == suffix_type, SuffixModel.deleted_at == 0]
            if env_id:
                smtm_list.append(SuffixModel.env_id == env_id)
            else:
                smtm_list.append(SuffixModel.case_id == case_id)
            smtm = await session.execute(select(func.count(SuffixModel.suffix_id)).where(and_(*smtm_list)))
            return smtm.scalars().first()

    @staticmethod
    async def add_suffix(create_user: int, **kwargs):
        async with async_session() as session:
            async with session.begin():
                sort_count = await SuffixCrud.current_suffix_count(
                    kwargs["suffix_type"], kwargs["env_id"], kwargs["case_id"]
                )
                suffix = SuffixModel(**kwargs, create_user=create_user)
                suffix.sort = sort_count + 1
                session.add(suffix)
                await session.flush()
                session.expunge(suffix)

    @staticmethod
    async def delete_suffix(suffix_id: int, suffix_type: int, operator: int, case_id: int = None, env_id: int = None):
        async with async_session() as session:
            async with session.begin():
                smtm_suffix_id = text(
                    "SELECT suffix_id, sort FROM common_suffix WHERE suffix_id = :suffix_id  AND deleted_at = 0"
                )
                smtm_suffix_id = await session.execute(smtm_suffix_id, {"suffix_id": suffix_id})
                s_id, s_sort = smtm_suffix_id.first()
                print(s_sort)
                # 删除当前数据
                smtm_delete = text(
                    "UPDATE common_suffix SET deleted_at = :deleted_at,  update_user= :update_user WHERE suffix_id = :suffix_id"
                )
                await session.execute(
                    smtm_delete,
                    {"deleted_at": int(datetime.now().timestamp()), "update_user": operator, "suffix_id": s_id},
                )
                # 更新其他数据排序
                if case_id is None:
                    smtm_update = text(
                        "UPDATE common_suffix SET sort = sort - 1, update_user= :update_user WHERE sort > :sort AND suffix_type = :suffix_type AND env_id = :env_id AND deleted_at = 0"
                    )
                    await session.execute(
                        smtm_update,
                        {
                            "update_user": operator,
                            "sort": s_sort,
                            "suffix_type": suffix_type,
                            "env_id": env_id,
                        },
                    )
                if env_id is None:
                    smtm_update = text(
                        "UPDATE common_suffix SET sort = sort - 1, update_user= :update_user WHERE sort > :sort AND suffix_type = :suffix_type AND case_id = :case_id AND deleted_at = 0"
                    )
                    await session.execute(
                        smtm_update,
                        {
                            "update_user": operator,
                            "sort": s_sort,
                            "suffix_type": suffix_type,
                            "case_id": case_id,
                        },
                    )
                await session.flush()

    @staticmethod
    async def enable_suffix(suffix_id: int, enable: bool, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = await session.execute(
                    select(SuffixModel).where(and_(SuffixModel.suffix_id == suffix_id, SuffixModel.deleted_at == 0))
                )
                result = smtm.scalars().first()
                result.enable = enable
                result.update_user = operator
                await session.flush()

    @staticmethod
    async def add_suffix_form(form: list[SchemaCaseSuffix], creator: int, case_id: int = None, env_id: int = None):
        async with async_session() as session:
            async with session.begin():
                await DatabaseBulk.bulk_add_data(
                    session,
                    SuffixModel,
                    form,
                    create_user=creator,
                    case_id=case_id,
                    env_id=env_id,
                    update_user=creator,
                )
                await session.flush()

    @staticmethod
    async def add_suffix_form_with_session(
        session, form: list[SchemaCaseSuffix], creator: int, case_id: int = None, env_id: int = None
    ):
        await DatabaseBulk.bulk_add_data(
            session,
            SuffixModel,
            form,
            create_user=creator,
            case_id=case_id,
            env_id=env_id,
            update_user=creator,
        )
        await session.flush()
