# coding=utf-8
"""
File: jobs.py
Author: bot
Created: 2023/9/21
Description:
"""
import asyncio
import time
import uuid
from typing import List

from fastapi import APIRouter
from celery import Celery
from celery.result import AsyncResult
from app.handler.response_handler import C137Response
from app.services.api_case.api_case_services import ApiCaseServices

jobs = APIRouter()

celery = Celery("jobs", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
# celery = Celery("jobs", broker="pyamqp://guest@localhost//", backend="redis://localhost:6379/0")


@celery.task
def my_celery_task(env_id: int, case_id: List[int]) -> AsyncResult:
    # 在任务内部执行协程
    async def my_coroutine():
        # 协程的逻辑
        random_uid = str(uuid.uuid4())
        response = await ApiCaseServices.run_case_suite(random_uid, env_id, case_id)
        return random_uid

    # 执行协程并获取结果
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(my_coroutine())
    # 返回结果
    return result


@jobs.get("/run")
async def test_runners():
    result = my_celery_task.delay()
    return {"task_id": result.id, "status": "Task is running"}


@jobs.get("/jobs/apicase/{task_id}/result")
async def get_task_result(task_id: str):
    # 查询 Celery 任务的结果
    result = celery.AsyncResult(task_id)
    if result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    elif result.state == "PENDING":
        return {"status": "pending"}
    else:
        return {"status": "unknown"}
