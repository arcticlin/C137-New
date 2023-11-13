from datetime import datetime
from typing import Union


from app.handler.db_tool.db_bulk import DatabaseBulk
from app.handler.serializer.response_serializer import C137Response
from app.models.auth.user import UserModel
from app.core.db_connector import async_session
from sqlalchemy import select, and_, or_, text

from app.services.auth.schema.register import UserRegisterRequest
from app.services.auth.schema.update_info import UserUpdateRequest


class UserCrud:
    @staticmethod
    async def user_amount() -> int:
        async with async_session() as session:
            smtm = text("SELECT COUNT(user_id) FROM users WHERE deleted_at = 0")
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def account_is_exists(account: str) -> bool:
        """查询账号是否存在"""
        async with async_session() as session:
            smtm = text(
                """
                SELECT EXISTS (
                    SELECT 1 
                    FROM users 
                    WHERE account = :account AND deleted_at = 0 AND valid = 1
                    ) AS is_exists
                """
            )
            result = await session.execute(smtm, {"account": account})
            return result.scalars().first()

    @staticmethod
    async def get_user_by_account(account: str) -> Union[UserModel, None]:
        """通过账号获取用户信息"""
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.account == account, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_id(user_id: int) -> Union[UserModel, None]:
        """通过账号获取用户信息"""
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def get_user_by_nickname(nickname: str):
        """通过昵称获取用户信息"""
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.nickname == nickname, UserModel.deleted_at == 0))
            result = await session.execute(smtm)
            return result.scalars().first()

    @staticmethod
    async def user_is_admin(user_id: int):
        """检查用户否为管理员"""
        async with async_session() as session:
            smtm = select(UserModel).where(
                and_(UserModel.user_id == user_id, UserModel.deleted_at == 0, UserModel.user_role == 2)
            )
            result = await session.execute(smtm)
            return 2 if result.scalars().first() is not None else None

    @staticmethod
    async def register_user(register_form: UserRegisterRequest, is_admin: bool = False) -> int:
        """注册用户, 首次注册和密码加密放在service层即可"""
        async with async_session() as session:
            async with session.begin():
                user = UserModel(**register_form.dict(), user_role=2 if is_admin else 1)
                session.add(user)
                await session.flush()
                session.expunge(user)
                return user.user_id

    @staticmethod
    async def record_last_login_time(user_id: int) -> datetime:
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                last_time = datetime.now()
                user.last_login = datetime.now()
                await session.flush()
                session.expunge(user)
                return last_time

    @staticmethod
    async def get_user_list():
        async with async_session() as session:
            smtm = select(UserModel).where(and_(UserModel.deleted_at == 0, UserModel.valid == 1))
            result = await session.execute(smtm)
            return result.scalars().all()

    @staticmethod
    async def update_user_info(user_id: int, update_data: UserUpdateRequest):
        """更新用户信息"""
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                DatabaseBulk.update_model(user, update_data.dict(), user_id)
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def re_modify_user_password(user_id: int, password: str):
        """修改密码"""
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.password = password

                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_role(user_id: int, user_role: int, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.user_role = user_role
                user.update_user = operator
                await session.flush()
                session.expunge(user)

    @staticmethod
    async def update_user_ban(user_id: int, valid: bool, operator: int):
        async with async_session() as session:
            async with session.begin():
                smtm = select(UserModel).where(and_(UserModel.user_id == user_id, UserModel.deleted_at == 0))
                result = await session.execute(smtm)
                user = result.scalars().first()
                user.valid = valid
                user.update_user = operator
                await session.flush()
                session.expunge(user)
