from app.crud.project.project_crud import ProjectCrud
from app.exceptions.commom_exception import CustomException
from app.schemas.project.project_schema import AddProjectRequest, UpdateProjectRequest
from app.utils.logger import Log
from app.exceptions.project_exp import *


class ProjectService:

    log = Log("ProjectService")

    @staticmethod
    async def add_project(data: AddProjectRequest, creator: int):
        if await ProjectCrud.query_project_by_name(data.project_name):
            raise CustomException(PROJECT_NAME_EXISTS)
        await ProjectCrud.add_project(data, creator)

    @staticmethod
    async def delete_project(project_id: int, operator: int):
        project = await ProjectCrud.query_project(project_id)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.delete_project(project_id, operator)

    @staticmethod
    async def update_project(project_id: int, data: UpdateProjectRequest, operator: int):
        project = await ProjectCrud.query_project(project_id)
        print("Here", project)
        if not project:
            raise CustomException(PROJECT_NOT_EXISTS)
        if project.create_user != operator:
            raise CustomException(PROJECT_NOT_CREATOR)
        await ProjectCrud.update_project(project_id, data, operator)