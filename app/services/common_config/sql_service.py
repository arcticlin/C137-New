# coding=utf-8
"""
File: sql_service.py
Author: bot
Created: 2023/10/24
Description:
"""
from app.exceptions.custom_exception import CustomException
from app.services.auth.crud.auth_crud import UserCrud
from app.services.common_config.crud.sql.sql_crud import SqlCrud
from app.services.common_config.schema.sql.news import RequestSqlAdd, RequestSqlPingByForm, RequestSqlCommandDebug
from app.exceptions.db_exp_460 import *
from app.services.common_config.schema.sql.update import RequestSqlUpdate


class SqlService:
    @staticmethod
    async def create_sql_config(form: RequestSqlAdd, creator: int):
        check = await SqlCrud.query_sql_name_exists(form.name)
        if check:
            raise CustomException(SQL_NAME_EXISTS)
        sql_id = await SqlCrud.create_sql_config(form, creator)
        return sql_id

    @staticmethod
    async def update_sql_config(sql_id: int, form: RequestSqlUpdate, operator: int):
        check = await SqlCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        if form.name:
            check = await SqlCrud.query_sql_name_exists(form.name)
            print(check)
            if check:
                raise CustomException(SQL_NAME_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await SqlCrud.operator_is_creator(sql_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_MODIFY_SQL)
        await SqlCrud.update_sql_config(sql_id, form, operator)

    @staticmethod
    async def delete_sql_config(sql_id: int, operator: int):
        check = await SqlCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        user_role_in_system = await UserCrud.user_is_admin(operator)
        user_identical = await SqlCrud.operator_is_creator(sql_id, operator)
        if not user_identical and user_role_in_system is None:
            raise CustomException(NO_ALLOW_TO_DELETE_SQL)
        await SqlCrud.delete_sql_config(sql_id, operator)

    @staticmethod
    async def query_sql_list(page: int, page_size: int):
        result, total = await SqlCrud.query_sql_list(page, page_size)
        return result, total

    @staticmethod
    async def query_sql_by_id(sql_id: int):
        check = await SqlCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        result = await SqlCrud.query_sql_detail(sql_id)
        return result

    @staticmethod
    async def ping_sql_by_form(form: RequestSqlPingByForm):
        await SqlCrud.ping_by_form(form)

    @staticmethod
    async def ping_sql_by_id(sql_id: int):
        check = await SqlCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        await SqlCrud.ping_by_id(sql_id)

    @staticmethod
    async def debug_sql_command(form: RequestSqlCommandDebug):
        check = await SqlCrud.query_sql_detail(form.sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        new_form = SqlCrud.convert_model_to_sql_form(check)

        await SqlCrud.execute_sql_command(form)
