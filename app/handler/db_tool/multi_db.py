# coding=utf-8
"""
File: db_tool.py
Author: bot
Created: 2023/8/7
Description:
"""
import aiopg, aiomysql, motor
from app.exceptions.custom_exception import CustomException
from aiomysql import Connection


class MultiDbConnector:
    @staticmethod
    async def mysql_connection(
        host: str,
        username: str,
        password: str = None,
        db: str = None,
        port: int = 3306,
    ) -> Connection:
        try:
            connection = await aiomysql.connect(host=host, port=port, user=username, password=password, db=db)
            return connection
        except Exception as e:
            raise CustomException((400, 40801, f"数据库连接失败, {e}"))

    @staticmethod
    async def mysql_ping(host: str, username: str, password: str = None, db: str = None, port: int = 3306):
        connection = await MultiDbConnector.mysql_connection(host, username, password, db, port)
        connection.close()

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
                raise CustomException((400, 40802, f"SQL执行失败, {e}"))
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
