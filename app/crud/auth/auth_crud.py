# coding=utf-8
"""
File: auth_crud.py
Author: bot
Created: 2023/7/25
Description:
"""

from app.utils.logger import Log
from app.models.auth.user import UserModel
from app.schemas.auth.user import UserRegisterRequest, UserRegisterResponse
from app.core.db_connector import async_session
from sqlalchemy import select, and_


class AuthCrud:
    log = Log("AuthCrud")

    @staticmethod
    async def get_user_by_account(account: str):
        async with async_session() as session:
            smtm = select(UserModel).where(
                and_(UserModel.account == account, UserModel.deleted_at == 0)
            )
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_id(user_id: int):
        async with async_session() as session:
            smtm = select(UserModel).where(
                and_(UserModel.id == user_id, UserModel.deleted_at == 0)
            )
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_nickname(nickname: str):
        async with async_session() as session:
            smtm = select(UserModel).where(
                and_(UserModel.nickname == nickname, UserModel.deleted_at == 0)
            )
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def register_user(register_form: UserRegisterRequest):
        async with async_session() as session:
            async with session.begin():
                user = UserModel(**register_form.model_dump())
                session.add(user)
                await session.flush()
                session.expunge(user)
                return user
