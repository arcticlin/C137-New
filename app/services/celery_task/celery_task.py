# coding=utf-8
"""
File: celery_task.py
Author: bot
Created: 2023/9/22
Description:
"""
from celery import Celery

from app.services.api_case.api_case_services import ApiCaseServices
from base_config import Config
import asyncio

# 实例化Celery

celery = Celery("jobs", broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
celery.conf.result_backend = Config.SQLALCHEMY_URI


@celery.task
def run_case_suite(case_list: list[int]):
    async def query_case():
        r = await ApiCaseServices.query_case_details(1)
