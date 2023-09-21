# coding=utf-8
"""
File: jobs.py
Author: bot
Created: 2023/9/21
Description:
"""
import time

from fastapi import APIRouter
from celery import Celery

jobs = APIRouter()

celery = Celery("jobs", broker="pyamqp://guest@localhost//", backend="redis://localhost:6379/0")
test_sets = {}


@celery.task
def run_api_case():
    test_sets["1"] = {"status": "Running", "report": None}
    print("这里执行了?")
    time.sleep(10)
    print("这里执行了?")
    test_sets["1"] = {"status": "Success", "report": "跑完了~"}


@jobs.get("/run")
async def test_runner():
    result = run_api_case.apply_async(args=[])
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
