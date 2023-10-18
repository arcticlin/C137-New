from fastapi import APIRouter, Depends

from app.middleware.access_permission import Permission
from app.core.basic_schema import CommonResponse
from app.handler.serializer.response_serializer import C137Response

from app.services.auth.crud.auth_crud import UserCrud
from app.services.auth.schema.info import ResponseUserList, ResponseUserInfo
from app.services.auth.schema.register import ResponseRegister, UserRegisterRequest
from app.services.auth.schema.login import ResponseLogin, UserLoginRequest
from app.services.auth.schema.update_info import UserUpdateRequest, UserModifyPasswordRequest, UserResetPasswordRequest
from app.services.auth.auth_service import AuthService


auth = APIRouter()


@auth.post("/register", summary="注册账号", response_model=ResponseRegister)
async def register_user(form: UserRegisterRequest):
    user_id = await AuthService.register_user(form)
    return C137Response.success(data={"user_id": user_id})


@auth.post("/login", summary="登录账号", response_model=ResponseLogin)
async def login_user(form: UserLoginRequest):
    user_info = await AuthService.login_user(form)
    return C137Response.success(data=user_info)


@auth.post("/logout", summary="登出账号", response_model=CommonResponse)
async def logout_user(user_info: dict = Depends(Permission())):
    await AuthService.user_logout(user_info["user_id"])
    return C137Response.success(message="登出成功")


@auth.post("/reset_pwd", summary="重置用户密码")
async def reset_password(data: UserResetPasswordRequest):
    await AuthService.reset_password(data)
    return C137Response.success(message="操作成功")


@auth.post("/refresh_token", summary="刷新token", response_model=ResponseLogin)
async def refresh_token(user_info: dict = Depends(Permission(refresh=True))):
    new_token = await AuthService.refresh_token(user_info["user_id"], user_info["token"])
    return C137Response.success(message="操作成功", data=new_token)
