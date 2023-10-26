# coding=utf-8
"""
File: suffix_settings.py
Author: bot
Created: 2023/8/7
Description:
"""
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class SuffixModel(Base, BaseMixin):
    __tablename__ = "common_suffix"

    suffix_id = Column(Integer, primary_key=True, autoincrement=True)
    suffix_type = Column(Integer, nullable=False, comment="前/后置, 1: 前置 2: 后置", index=True)
    name = Column(String(16), nullable=False, comment="前/后置名称", index=True)
    description = Column(String(64), comment="前/后置描述")
    enable = Column(BOOLEAN, nullable=False, comment="是否启用", index=True)
    sort = Column(Integer, nullable=False, comment="排序", index=True)

    execute_type = Column(
        Integer, nullable=False, comment="执行类型, 1: python 2: sql 3: redis 4: delay 5: global-script", index=True
    )

    case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="绑定用例ID")
    env_id = Column(Integer, ForeignKey("envs.env_id"), comment="绑定环境ID")
    run_each_case = Column(Integer, comment="是否每条用例执行一次, 1: 是 0: 否")

    script_id = Column(Integer, ForeignKey("script.script_id"), comment="脚本ID", index=True)
    sql_id = Column(Integer, ForeignKey("sql_model.sql_id"), comment="SQL ID", index=True)
    redis_id = Column(Integer, ForeignKey("redis_model.redis_id"), comment="Redis ID", index=True)
    run_case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="执行用例ID", index=True)

    run_delay = Column(Integer, comment="execute_type == 4时生效, 延迟时间ms")
    fetch_one = Column(BOOLEAN, comment="execute_type == 2时生效, 是否只取一条数据")
    run_command = Column(TEXT, comment="执行命令")
    run_out_name = Column(String(16), comment="出参名", index=True)

    def __init__(
        self,
        suffix_type: int,
        name: str,
        enable: bool,
        execute_type: int,
        create_user: int,
        sort: int = None,
        env_id: int = None,
        script_id: int = None,
        sql_id: int = None,
        redis_id: int = None,
        run_case_id: int = None,
        run_delay: int = None,
        run_command: str = None,
        run_out_name: str = None,
        case_id: int = None,
        description: str = None,
        run_each_case: int = None,
        fetch_one: bool = None,
    ):
        self.suffix_type = suffix_type
        self.name = name
        self.enable = enable
        self.sort = sort
        self.execute_type = execute_type
        self.case_id = case_id
        self.env_id = env_id
        self.script_id = script_id
        self.sql_id = sql_id
        self.redis_id = redis_id
        self.run_case_id = run_case_id
        self.run_delay = run_delay
        self.run_command = run_command
        self.run_out_name = run_out_name
        self.create_user = create_user
        self.update_user = create_user
        self.description = description
        self.run_each_case = run_each_case
        self.fetch_one = fetch_one
