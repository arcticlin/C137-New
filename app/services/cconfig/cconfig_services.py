# coding=utf-8
"""
File: cconfig_services.py
Author: bot
Created: 2023/8/4
Description:
"""
from app.handler.response_handler import C137Response
from app.schemas.cconfig.env_schema import EnvAddRequest, EnvUpdateRequest
from app.utils.new_logger import logger
from app.schemas.cconfig.sql_schema import *
from app.schemas.cconfig.redis_schema import *
from app.schemas.cconfig.script_schema import *
from app.exceptions.cconfig_exp import *
from app.crud.cconfig.cconfig_crud import CommonConfigCrud
from app.exceptions.commom_exception import CustomException
from app.handler.script_handler import ScriptHandler
from app.handler.db_handler import DataBaseConnect
from app.crud.api_case.suffix_crud import SuffixCrud
from app.crud.api_case.assert_crud import AssertCurd
from app.crud.api_case.api_headers_crud import ApiHeadersCrud
from app.crud.api_case.api_path_crud import ApiPathCrud


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
            temp_data.append({"sql_id": sql_id, "name": name, "host": host, "sql_type": sql_type})
        return temp_data

    @staticmethod
    async def query_redis_list():
        result = await CommonConfigCrud.query_redis_list()
        temp_data = []
        for item in result:
            redis_id, name, host = item
            temp_data.append({"redis_id": redis_id, "name": name, "host": host})
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
            temp_data.append(
                {"script_id": script_id, "name": name, "var_key": var_key, "public": public, "create_user": create_user}
            )
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
    async def new_python_script_debug(data: DebugScriptSchema):
        script_runner = await ScriptHandler.python_executor(data.var_key, data.var_script)
        return script_runner

    @staticmethod
    async def ping_sql(sql_id: int):
        check = await CommonConfigCrud.query_sql_detail(sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        await DataBaseConnect.mysql_ping(
            host=check.host, port=check.port, username=check.db_user, password=check.db_password, db=check.db_name
        )

    @staticmethod
    async def execute_sql(data: ExecuteSqlRequest):
        check = await CommonConfigCrud.query_sql_detail(data.sql_id)
        if not check:
            raise CustomException(SQL_NOT_EXISTS)
        c = await DataBaseConnect.mysql_connection(
            host=check.host, port=check.port, username=check.db_user, password=check.db_password, db=check.db_name
        )
        result = await DataBaseConnect.mysql_execute(c, data.text)
        return result

    @staticmethod
    async def ping_redis(redis_id: int):
        check = await CommonConfigCrud.query_redis_id_exists(redis_id)
        if not check:
            raise CustomException(REDIS_NOT_EXISTS)

    @staticmethod
    async def query_env_list(page: int, page_size: int):
        total, result = await CommonConfigCrud.query_env_list(page, page_size)
        temp_data = []
        for item in result:
            env_id, name, url, create_user = item
            temp_data.append({"env_id": env_id, "name": name, "url": url, "create_user": create_user})
        return total, temp_data

    @staticmethod
    async def query_env_detail(env_id: int):
        temp = {}
        check = await CommonConfigCrud.query_env_detail(env_id)
        if check is None:
            raise CustomException(ENV_NOT_EXISTS)
        temp["env_info"] = C137Response.orm_to_dict(check)
        prefix_info = await SuffixCrud.get_prefix(env_id=env_id)
        suffix_info = await SuffixCrud.get_suffix(env_id=env_id)
        assert_info = await AssertCurd.query_assert_detail(env_id=env_id)
        query_info = await ApiPathCrud.query_path_detail_by_env_case(env_id=env_id)
        headers_info = await ApiHeadersCrud.query_headers_detail_by_env_case(env_id=env_id)
        # query_info = await
        temp["prefix_info"] = C137Response.orm_with_list(prefix_info)
        temp["suffix_info"] = C137Response.orm_with_list(suffix_info)
        temp["assert_info"] = C137Response.orm_with_list(assert_info)
        temp["query_info"] = C137Response.orm_with_list(query_info)
        temp["headers_info"] = C137Response.orm_with_list(headers_info)
        return temp

    @staticmethod
    async def add_env(form: EnvAddRequest, create_user: int):
        check = await CommonConfigCrud.query_env_name_exists(form.env_info.name)
        if check:
            raise CustomException(ENV_NAME_EXISTS)
        await CommonConfigCrud.add_env(form, create_user)

    @staticmethod
    async def update_env(env_id: int, form: EnvUpdateRequest, operator: int):
        check = await CommonConfigCrud.query_env_detail(env_id)
        if check is None:
            raise CustomException(ENV_NOT_EXISTS)
        await CommonConfigCrud.update_env(env_id, form, operator)
