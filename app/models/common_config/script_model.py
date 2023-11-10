# coding=utf-8
"""
File: script_model.py
Author: bot
Created: 2023/8/4
Description:
"""

from sqlalchemy import Column, Integer, String, TEXT, ForeignKey, BOOLEAN
from app.core.db_connector import Base, BaseMixin


class ScriptModel(Base, BaseMixin):
    __tablename__ = "script"

    script_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(32), nullable=False, comment="脚本名称")
    description = Column(String(64), comment="脚本描述")

    tag = Column(String(64), comment="标签归类")

    var_key = Column(String(32), nullable=False, comment="调用键")
    var_script = Column(TEXT, nullable=False, comment="脚本")

    public = Column(BOOLEAN, nullable=False, comment="是否公开")

    def __init__(
        self,
        name: str,
        var_key: str,
        var_script: str,
        create_user: int,
        description: str = None,
        tag: str = None,
        public: bool = False,
    ):
        self.create_user = create_user
        self.update_user = create_user
        self.name = name
        self.var_key = var_key
        self.var_script = var_script
        self.public = public
        self.description = description
        self.tag = tag
