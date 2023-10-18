# coding=utf-8
"""
File: oss.py
Author: bot
Created: 2023/10/12
Description:
"""

from fastapi import APIRouter, UploadFile

from app.handler.response_handler import C137Response
from app.services.oss.oss_services import OssService

oss = APIRouter()


@oss.post("/upload", summary="上传文件")
async def upload_file(file: UploadFile):
    img = await OssService.upload_file(file)
    return C137Response.success(data={"image_url": img})
