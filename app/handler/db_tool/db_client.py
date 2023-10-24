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
from app.exceptions.db_exp_460 import SQL_CONNECT_FAIL, SQL_EXECUTE_FAIL
from app.services.common_config.schema.sql.news import RequestSqlPingByForm


class DbClient:
    def __init__(self):
        self.connection = None

    async def __aenter__(self, form: RequestSqlPingByForm):
        self.connection = await self.mysql_connector(form.host, form.db_user, form.db_password, form.db_name, form.port)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()

    @staticmethod
    async def mysql_connector(
        host: str, username: str, password: str = None, db: str = None, port: int = 3306
    ) -> Connection:
        try:
            connection = await aiomysql.connect(host=host, port=port, user=username, password=password, db=db)
            return connection
        except Exception as e:
            raise CustomException(SQL_CONNECT_FAIL, f"{e}")

    @staticmethod
    async def mysql_ping(form: RequestSqlPingByForm):
        c = await DbClient.mysql_connector(form.host, form.db_user, form.db_password, form.db_name, form.port)
        c.close()

    @staticmethod
    async def mysql_execute(connection: Connection, text: str, is_first: bool = False):
        async with connection.cursor() as cursor:
            try:
                await cursor.execute(text)
                if is_first:
                    result = await cursor.fetchone()
                else:
                    result = await cursor.fetchall()
            except Exception as e:
                raise CustomException(SQL_EXECUTE_FAIL, f"{e}")
            return result

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
