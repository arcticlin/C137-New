from app.core.db_connector import Base, BaseMixin
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean


class ProjectModel(Base, BaseMixin):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(16), nullable=False, comment="项目名称")
    project_desc = Column(String(128), nullable=True, comment="项目描述")
    public = Column(Boolean, nullable=False, default=False, comment="是否公开")
    project_avatar = Column(String(128), nullable=True, comment="项目头像")

    def __init__(self, project_name: str, create_user: int, project_desc: str = None, public: bool = False, project_avatar: str = None):
        self.create_user = create_user
        self.update_user = create_user
        self.project_name = project_name
        self.project_desc = project_desc
        self.public = public
        self.project_avatar = project_avatar
