# coding=utf-8
"""
File: assert_settings.py
Author: bot
Created: 2023/8/7
Description:
"""

from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN


class AssertModel(Base, BaseMixin):
    __tablename__ = "common_assert"

    assert_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False, comment="断言名称")
    enable = Column(BOOLEAN, default=True, comment="是否启用")
    case_id = Column(Integer, ForeignKey("api_case.case_id"), comment="绑定用例ID")
    env_id = Column(Integer, ForeignKey("envs.env_id"), comment="绑定环境ID")

    assert_from = Column(
        Integer, nullable=False, comment="断言来源 1: res_header 2: res_body 3: res_status_code 4: res_elapsed"
    )
    assert_type = Column(
        Integer,
        nullable=False,
        comment="断言类型 1: equal 2: n-equal 3:GE 4: LE 5:in-list 6: not-in-list 7: contain 8: not-contain 9: start-with 10: end-with 11: Re_Gex 12:Json-Path",
    )
    assert_exp = Column(TEXT, comment="断言表达式")
    assert_value = Column(TEXT, nullable=False, comment="断言值")

    def __init__(
        self,
        name: str,
        assert_from: int,
        assert_type: int,
        assert_value: str,
        create_user: int,
        enable: bool = True,
        assert_exp: str = None,
        case_id: int = None,
        env_id: int = None,
    ):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.assert_from = assert_from
        self.assert_type = assert_type
        self.assert_exp = assert_exp
        self.assert_value = assert_value
        self.case_id = case_id
        self.env_id = env_id
        self.enable = enable
