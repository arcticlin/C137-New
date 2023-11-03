import secrets
import string

from app.exceptions.exp_410_auth import *
from app.handler.auth.token_handler import UserToken
from app.handler.redis.cache_redis import CacheRedis
from app.handler.serializer.response_serializer import C137Response
from app.services.auth.schema.admin import AdminBanRequest, AdminAssignNewRoleRequest
from app.services.auth.schema.login import UserLoginRequest
from app.services.auth.schema.register import UserRegisterRequest
from app.services.auth.crud.auth_crud import UserCrud
from loguru import logger
from app.exceptions.custom_exception import CustomException
from app.services.auth.schema.update_info import UserUpdateRequest, UserModifyPasswordRequest, UserResetPasswordRequest
from app.services.ws.ws_service import WsService


class AuthService:
    @staticmethod
    @CacheRedis.delete_keys(keys_list=["u:user_list"])
    async def register_user(form: UserRegisterRequest) -> int:
        logger.debug(f"注册账号: {form.account}")
        is_admin = False
        check_exists = await UserCrud.get_user_by_account(form.account)

        if check_exists:
            logger.error(f"账号: {form.account}已存在~")
            raise CustomException(ACCOUNT_EXISTS)
        check_user_amount = await UserCrud.user_amount()
        if check_user_amount == 0:
            logger.debug(f"服务首次注册,自动设置为管理员")
            is_admin = True
        form.password = UserToken.add_salt(form.password)
        user_id = await UserCrud.register_user(form, is_admin=is_admin)
        print(
            "??",
        )
        await WsService.ws_notify_update_user_list()
        return user_id

    @staticmethod
    @CacheRedis.user_cache(user_id=None)
    async def login_user(form: UserLoginRequest):
        # 检查已注册
        user = await UserCrud.get_user_by_account(form.account)
        if not user:
            raise CustomException(ACCOUNT_NOT_EXISTS)
        # 检查密码
        if user.password != UserToken.add_salt(form.password):
            raise CustomException(PASSWORD_INCORRECT)
            # 检查账户状态
        if user.valid == 0:
            raise CustomException(ACCOUNT_IS_BANNED)
        # 生成token
        user_orm = C137Response.orm_to_dict(
            user,
            "password",
        )
        expired_time, token = UserToken.encode_token(user_orm)
        user_orm["expired_at"] = expired_time
        user_orm["token"] = token
        # 记录最后登录时间
        await UserCrud.record_last_login_time(user.user_id)
        return user_orm

    @staticmethod
    @CacheRedis.cache("u:user_list")
    async def get_user_list() -> list:
        user_list = await UserCrud.get_user_list()
        user_orm = C137Response.orm_with_list(
            user_list, "password", "created_at", "deleted_at", "updated_at", "last_login"
        )
        return user_orm

    @staticmethod
    async def user_logout(user_id: int) -> None:
        await CacheRedis.rds.delete(f"ut:user_token_{user_id}")

    @staticmethod
    @CacheRedis.delete_keys(keys_list=["u:user_list"])
    async def update_user_info(user_id: int, data: UserUpdateRequest) -> None:
        await UserCrud.update_user_info(user_id, data)

    @staticmethod
    async def admin_generate_reset_code(account: str):
        """管理员生成重置密码验证码"""
        if not await UserCrud.account_is_exists(account):
            raise CustomException(ACCOUNT_NOT_EXISTS)
        characters = string.ascii_letters + string.digits
        reset_code = "".join(secrets.choice(characters) for _ in range(6))
        await CacheRedis.rds.set(f"u:reset_code_{account}", reset_code, ex=300)
        return reset_code

    @staticmethod
    async def reset_password(data: UserResetPasswordRequest):
        """重置密码"""
        reset_code = await CacheRedis.rds.get(f"u:reset_code_{data.account}")
        if reset_code != data.reset_code:
            raise CustomException(RESET_CODE_INCORRECT)
        uid = await UserCrud.get_user_by_account(data.account)
        new_pwd = UserToken.add_salt(data.new_password)
        data.new_password = new_pwd
        await UserCrud.re_modify_user_password(uid.user_id, data.new_password)
        # 删除验证码
        await CacheRedis.rds.delete(f"u:reset_code_{data.account}")
        # 删除Redis对应的已登录的token
        uid = await UserCrud.get_user_by_account(data.account)
        await CacheRedis.rds.delete(f"ut:user_token_{uid.user_id}")

    @staticmethod
    async def modify_password(data: UserModifyPasswordRequest, operator: int):
        """修改密码"""
        user = await UserCrud.get_user_by_id(operator)
        if UserToken.add_salt(data.old_password) != user.password:
            raise CustomException(PASSWORD_INCORRECT)
        await UserCrud.re_modify_user_password(user.user_id, UserToken.add_salt(data.new_password))

    @staticmethod
    async def admin_update_user_role(data: AdminAssignNewRoleRequest, operator: int):
        check = await UserCrud.get_user_by_id(user_id=data.user_id)
        if not check:
            raise CustomException(ACCOUNT_NOT_EXISTS)
        await UserCrud.update_user_role(data.user_id, data.user_role, operator)

    @staticmethod
    @CacheRedis.delete_keys(keys_list=["u:user_list"])
    async def admin_ban_user(data: AdminBanRequest, operator: int):
        check = await UserCrud.get_user_by_id(user_id=data.user_id)
        if not check:
            raise CustomException(ACCOUNT_NOT_EXISTS)
        await UserCrud.update_user_ban(data.user_id, data.valid, operator)

    @staticmethod
    async def get_token_in_redis(user_id: int) -> dict:
        keys = f"ut:user_token_{user_id}"
        user_info = await CacheRedis.rds.get_key_value_as_json(keys)
        return user_info

    @staticmethod
    @CacheRedis.user_cache(user_id=None)
    async def refresh_token(user_id: int, old_token: str):
        user_in_redis = await UserService.get_token_in_redis(user_id)
        if user_in_redis is None or user_in_redis.keys() == 0:
            raise CustomException(TOKEN_IS_INVALID)
        if user_in_redis["token"] != old_token:
            raise CustomException(TOKEN_IS_INVALID)
        user_info = await UserCrud.get_user_by_id(user_id)
        user_orm = C137Response.orm_to_dict(
            user_info,
            "password",
            "valid",
        )
        expired_time, token = UserToken.encode_token(user_orm)
        user_orm["expired_at"] = expired_time
        user_orm["token"] = token
        # 记录最后登录时间
        await UserCrud.record_last_login_time(user_info.user_id)
        return user_orm
