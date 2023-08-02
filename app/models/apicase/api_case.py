# coding=utf-8
"""
File: api_case.py
Author: bot
Created: 2023/8/2
Description:
"""
from sqlalchemy import Column, Integer, TEXT, String
from sqlalchemy.orm import relationship

from app.core.db_connector import Base, BaseMixin


class ApiCaseModel(Base, BaseMixin):
    __tablename__ = "api_case"

    case_id = Column(Integer, primary_key=True, autoincrement=True)

    # 用例名称
    name = Column(String(32), nullable=False, comment="用例名称")

    # 请求配置
    request_type = Column(Integer, default=1, comment="请求协议类型 1: http 2: grpc")
    url = Column(TEXT, nullable=False, comment="请求url")
    method = Column(String(12), comment="请求方式")
    headers = relationship("ApiHeadersModel", backref="api_case")
    path = relationship("ApiPathModel", backref="api_case")
    body_type = Column(Integer, default=1, comment="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body = Column(TEXT, comment="请求体")

    # 用例属性
    directory_id = Column(Integer, index=True)

    tag = Column(String(32), comment="标签")
    status = Column(
        Integer,
        default=1,
        comment="用例状态 1: debug 2: close 3: normal",
    )
    priority = Column(String(3), comment="用例优先级: P0-P4")
    case_type = Column(Integer, comment="用例类型: 1. 正常用例 2. 前置用例 3. 数据构造")

    def __init__(
        self,
        name: str,
        url: str,
        method: str,
        directory_id: int,
        create_user: int,
        tag: str = None,
        status: int = 1,
        priority: str = "P1",
        case_type: int = 1,
        body: str = None,
        body_type: int = 1,
        request_type: int = 1,
    ):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.url = url
        self.method = method
        self.directory_id = directory_id
        self.tag = tag
        self.status = status
        self.priority = priority
        self.case_type = case_type
        self.body = body
        self.body_type = body_type
        self.request_type = request_type
