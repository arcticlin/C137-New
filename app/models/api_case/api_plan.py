# coding=utf-8
"""
File: api_plan.py
Author: bot
Created: 2023/9/28
Description:
"""
import json

from sqlalchemy import Column, Integer, TEXT, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiPlanModel(Base, BaseMixin):
    __tablename__ = "api_plan"

    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False, comment="计划名称")
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False, comment="绑定项目ID", index=True)
    env_id = Column(Integer, ForeignKey("envs.env_id"), nullable=False, comment="绑定环境ID", index=True)
    cron = Column(String(32), nullable=False, comment="定时任务")
    run_async = Column(Integer, default=0, comment="是否异步执行")
    case_list = Column(JSON, comment="用例列表")
    pass_rate = Column(Integer, comment="通过率")
    retry_time = Column(Integer, comment="重试次数")
    push_way = Column(Integer, comment="推送方式")
    push_user_list = Column(JSON, comment="推送用户列表")

    def __init__(
        self,
        name: str,
        project_id: int,
        env_id: int,
        cron: str,
        run_async: int,
        case_list: list,
        pass_rate: int,
        retry_time: int = None,
        push_way: int = None,
        push_user_list: list = None,
    ):
        self.name = name
        self.project_id = project_id
        self.env_id = env_id
        self.cron = cron
        self.run_async = run_async
        self.case_list = json.dumps(case_list) if isinstance(case_list, list) else case_list
        self.pass_rate = pass_rate
        self.retry_time = retry_time
        self.push_way = push_way
        if push_user_list is None:
            self.push_user_list = "[]"
        else:
            self.push_user_list = json.dumps(push_user_list) if isinstance(push_user_list, list) else push_user_list
