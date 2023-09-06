# coding=utf-8
"""
File: data_factory.py
Author: bot
Created: 2023/9/4
Description:
"""
# coding=utf-8
"""
File: api_case.py
Author: bot
Created: 2023/8/2
Description:
"""
from sqlalchemy import Column, Integer, TEXT, String, JSON
from sqlalchemy.orm import relationship
from app.core.db_connector import Base, BaseMixin


class DataFactoryModel(Base, BaseMixin):
    __tablename__ = "data_factory"

    data_id = Column(Integer, primary_key=True, autoincrement=True)

    # 用例名称
    name = Column(String(32), nullable=False, comment="用例名称")

    # 请求配置
    request_type = Column(Integer, default=1, comment="请求协议类型 1: http 2: grpc")
    url = Column(TEXT, nullable=False, comment="请求url")
    method = Column(String(12), comment="请求方式")
    headers = Column(JSON, comment="请求头")
    path = Column(JSON, comment="请求路径")
    params = Column(JSON, comment="请求参数")
    body_type = Column(Integer, default=1, comment="请求体类型, 0: none, 1: json 2: form 3: x-form 4: binary, 5: GraphQL")
    body = Column(TEXT, comment="请求体")

    def __init__(
        self,
        name: str,
        url: str,
        method: str,
        create_user: int,
        body: str = None,
        headers: list = None,
        path: list = None,
        params: list = None,
        body_type: int = 1,
        request_type: int = 1,
    ):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.url = url
        self.method = method
        self.body = body
        self.body_type = body_type
        self.request_type = request_type
        self.headers = headers
        self.params = params
        self.path = path
