# coding=utf-8
"""
File: db_client.py
Author: bot
Created: 2023/10/24
Description:
"""
import aiomysql
from aiomysql import Connection

from app.exceptions.custom_exception import CustomException
from app.exceptions.exp_460_db import SQL_CONNECT_FAIL, SQL_EXECUTE_FAIL
from app.services.common_config.schema.sql.news import RequestSqlPingByForm


class AsyncDbClient:
    def __init__(self, form: RequestSqlPingByForm):
        self.connection = None
        self.form = form

    async def __aenter__(self):
        self.connection = await self.mysql_connector()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    async def mysql_connector(self) -> Connection:
        try:
            connection = await aiomysql.connect(
                host=self.form.host,
                port=self.form.port,
                user=self.form.db_user,
                password=self.form.db_password,
                db=self.form.db_name,
            )
            return connection
        except Exception as e:
            raise CustomException(SQL_CONNECT_FAIL, f"{e}")

    async def ping(self):
        c = await self.mysql_connector()
        c.close()

    async def execute_command(self, command: str, fetch_one: bool = False):
        c = await self.mysql_connector()
        async with c.cursor() as cursor:
            try:
                await cursor.execute(command)
                if fetch_one:
                    result = await cursor.fetchone()
                else:
                    result = await cursor.fetchall()
                return result
            except Exception as e:
                raise CustomException(SQL_EXECUTE_FAIL, f"{e}")

    @staticmethod
    async def execute_command_with_c(
        connection: Connection, command: str, fetch_one: bool = False, run_out_name: str = None
    ):
        async with connection.cursor() as cursor:
            try:
                await cursor.execute(command)
                if fetch_one:
                    result = await cursor.fetchone()
                else:
                    result = await cursor.fetchall()
                if run_out_name:
                    return {run_out_name: result}
                return result
            except Exception as e:
                raise CustomException(SQL_EXECUTE_FAIL, f"{e}")

    @staticmethod
    async def postgresql_connection(
        host: str,
        username: str,
        password: str = None,
        db: str = None,
        port: int = 5432,
    ):
        pass

    @staticmethod
    async def mongodb_connection(
        host: str,
        username: str = None,
        password: str = None,
        port: int = 27017,
    ):
        pass
