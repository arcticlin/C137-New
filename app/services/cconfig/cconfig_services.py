# coding=utf-8
"""
File: cconfig_services.py
Author: bot
Created: 2023/8/4
Description:
"""
from app.handler.response_handler import C137Response
from app.utils.new_logger import logger
from app.schemas.cconfig.sql_schema import *
from app.schemas.cconfig.redis_schema import *
from app.schemas.cconfig.script_schema import *
from app.exceptions.cconfig_exp import *
from app.crud.cconfig.cconfig_crud import CommonConfigCrud
from app.exceptions.commom_exception import CustomException
from app.handler.script_handler import ScriptHandler


class CommonConfigServices:

    @staticmethod
    async def add_sql_config(data: AddSqlRequest, create_user: int):
        check = await CommonConfigCrud.query_sql_name_exists(data.name)
        if check:
            raise CustomException(SQL_NAME_EXISTS)
        await CommonConfigCrud.add_sql_config(data, create_user)

    @staticmethod
    async def update_sql_config(data: UpdateSqlRequest, sql_id: int, operator: int):
        check = await CommonConfigCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        await CommonConfigCrud.update_sql_config(data, sql_id, operator)

    @staticmethod
    async def delete_sql_config(sql_id: int, operator: int):
        check = await CommonConfigCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        await CommonConfigCrud.delete_sql_config(sql_id, operator)

    @staticmethod
    async def add_redis_config(data: AddRedisRequest, create_user: int):
        check = await CommonConfigCrud.query_redis_name_exists(data.name)
        if check:
            raise CustomException(REDIS_NAME_EXISTS)
        await CommonConfigCrud.add_redis_config(data, create_user)

    @staticmethod
    async def update_redis_config(data: UpdateRedisRequest, redis_id: int, operator: int):
        check = await CommonConfigCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        await CommonConfigCrud.update_redis_config(data, redis_id, operator)

    @staticmethod
    async def delete_redis_config(redis_id: int, operator: int):
        check = await CommonConfigCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        await CommonConfigCrud.delete_redis_config(redis_id, operator)

    @staticmethod
    async def add_script_config(data: AddScriptRequest, create_user: int):
        if data.public:
            check = await CommonConfigCrud.query_script_name_exists_in_public(data.name)
        else:
            check = await CommonConfigCrud.query_script_name_exists_in_private(data.name, create_user)
        if check:
            raise CustomException(SCRIPT_NAME_EXISTS)
        await CommonConfigCrud.add_script_config(data, create_user)

    @staticmethod
    async def update_script_config(data: UpdateScriptRequest, script_id: int, operator: int):
        check = await CommonConfigCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        await CommonConfigCrud.update_script_config(data, script_id, operator)

    @staticmethod
    async def delete_script_config(script_id: int, operator: int):
        check = await CommonConfigCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        await CommonConfigCrud.delete_script_config(script_id, operator)

    @staticmethod
    async def query_sql_list():
        result = await CommonConfigCrud.query_sql_list()
        temp_data = []
        for item in result:
            sql_id, name, host, sql_type = item
            temp_data.append(
                {
                    "sql_id": sql_id,
                    "name": name,
                    "host": host,
                    "sql_type": sql_type
                }
            )
        return temp_data

    @staticmethod
    async def query_redis_list():
        result = await CommonConfigCrud.query_redis_list()
        temp_data = []
        for item in result:
            redis_id, name, host = item
            temp_data.append({
                "redis_id": redis_id,
                "name": name,
                "host": host
            })
        return temp_data

    @staticmethod
    async def query_script_list(page: int = 1, page_size: int = 20, user_id: int = 0):
        if not user_id or user_id == 0:
            total, result = await CommonConfigCrud.query_script_list_public(page, page_size)
        else:
            total, result = await CommonConfigCrud.query_script_list_myself(user_id, page, page_size)
        temp_data = []
        for item in result:
            script_id, name, var_key, public, create_user = item
            temp_data.append({
                "script_id": script_id,
                "name": name,
                "var_key": var_key,
                "public": public,
                "create_user": create_user
            })
        return total, temp_data

    @staticmethod
    async def query_sql_detail(sql_id: int):
        check = await CommonConfigCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        result = await CommonConfigCrud.query_sql_detail(sql_id)
        return result

    @staticmethod
    async def query_redis_detail(redis_id: int):
        check = await CommonConfigCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
        result = await CommonConfigCrud.query_redis_detail(redis_id)
        return result

    @staticmethod
    async def query_script_detail(script_id: int):
        check = await CommonConfigCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await CommonConfigCrud.query_script_detail(script_id)
        return result

    @staticmethod
    async def python_script_debug(script_id: int):
        check = await CommonConfigCrud.query_script_id_exists(script_id)
        if not check:
            raise CustomException(SCRIPT_NOT_EXISTS)
        result = await CommonConfigCrud.query_script_detail(script_id)
        script_runner = await ScriptHandler.python_executor(result.var_key, result.var_script)
        return script_runner

    @staticmethod
    async def ping_sql(sql_id: int):
        check = await CommonConfigCrud.query_sql_id_exists(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)

    @staticmethod
    async def ping_redis(redis_id: int):
        check = await CommonConfigCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)
