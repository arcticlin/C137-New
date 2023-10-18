# coding=utf-8
"""
File: oss_services.py
Author: bot
Created: 2023/10/12
Description:
"""
import aiohttp

from app.exceptions.commom_exception import CustomException
from app.exceptions.oss_exp_510 import GET_TOKEN_FAILED
from base_config import Config
from aiohttp import ClientSession
from fastapi import UploadFile


class OssService:
    @staticmethod
    async def get_tokens():
        async with ClientSession() as session:
            async with session.post(
                f"{Config.IMG_HOST}/tokens", data={"email": Config.IMG_ACCOUNT, "password": Config.IMG_PWD}
            ) as resp:
                code = resp.status
                data = await resp.json()
                if code == 200:
                    if data["status"]:
                        return data["data"]["token"]
                    else:
                        raise CustomException(GET_TOKEN_FAILED, data["message"])

    @staticmethod
    async def upload_file(file: UploadFile):
        # 获取图床授权令牌
        token = await OssService.get_tokens()

        # 构建图床上传请求
        data = aiohttp.FormData()
        data.add_field("file", file.file, filename=file.filename)
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{Config.IMG_HOST}/upload", data=data, headers=headers) as response:
                upload_data = await response.json()
                if upload_data.get("status"):
                    return upload_data["data"]["links"]["url"]
                else:
                    raise CustomException(GET_TOKEN_FAILED, upload_data["message"])
