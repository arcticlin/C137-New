# coding=utf-8
"""
File: auth_crud.py
Author: bot
Created: 2023/7/25
Description:
"""
from datetime import datetime
from typing import Union

from app.handler.response_handler import C137Response
from app.utils.logger import Log
from app.models.auth.user import UserModel
from app.schemas.auth.user import UserRegisterRequest
from app.core.db_connector import async_session
from sqlalchemy import select, and_, text, column, Integer, Unicode
from app.handler.token_handler import UserToken
from app.handler.db_bulk import DatabaseBulk
from app.enums.enum_user import UserRoleEnum


class AuthCrud:
    log = Log("AuthCrud")

    @staticmethod
    async def get_user_by_account(account: str) -> Union[UserModel, None]:
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.account == account, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_id(user_id: int):
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_nickname(nickname: str):
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.nickname == nickname, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def register_user(register_form: UserRegisterRequest):
        async with async_session() as session:
            async with session.begin():
                user = UserModel(**register_form.dict())
                session.add(user)
                await session.flush()
                session.expunge(user)
                # return user

    @staticmethod
    async def record_last_login_time(user_id: int):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.last_login = datetime.now()
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_info(user_id: int, update_data: dict):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                DatabaseBulk.update_model(user, update_data, user_id)
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_password(user_id: int, password: str):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.password = UserToken.add_salt(password)
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def reset_user_password(account: str, password: str):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.account == account, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.password = UserToken.add_salt(password)
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_role(user_id: int, user_role: UserRoleEnum):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.user_role = UserRoleEnum(user_role)
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_ban(user_id: int, valid: bool):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.valid = valid
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def get_all_user():
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            smtm2 = text(
                """
                SELECT user_id, nickname FROM users WHERE deleted_at = 0
            """
            )
            print("t", type(smtm2))
            smtm2 = smtm2.columns(column("user_id", Integer), column("name", Unicode))
            print("b", type(smtm2))

            # orm_sql = select(UserModel).from_statement(smtm2)
            result1 = await session.execute(smtm2)
            for x in result1:
                print(x)
                print(C137Response.orm_to_dict(x))

            return result.scalars().all()
