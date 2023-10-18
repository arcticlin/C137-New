from typing import Union

from app.handler.redis.rds_client import RedisCli


class ApiRedis(RedisCli):
    def __init__(self, trace_id: int = None):
        super().__init__(trace_id)

    def get_env_rk(self, env_id: int):
        """返回env redis key, 格式为: api_{trace_id}:e:e_{env_id}"""
        return f"api:{self.trace_id}:e:e_{env_id}"

    def get_case_rk(self, case_id: int):
        """返回case redis key, 格式为: api_{trace_id}:c:c_{case_id}"""
        return f"api:{self.trace_id}:c:c_{case_id}"

    async def init_env_key(self, env_id: int):
        """初始化env key"""
        rk = self.get_env_rk(env_id)
        body = dict(var={}, log=dict(env_prefix=[], env_suffix=[]))
        await self.set_key_as_json(rk, body, expired=7200)

    async def init_case_key(self, case_id: int):
        """初始化case key"""
        rk = self.get_case_rk(case_id)
        body = dict(var={}, log=dict())
        await self.set_key_as_json(rk, body, expired=7200)

    async def set_env_var(self, env_id: int, value: dict):
        """设置env变量"""
        rk = self.get_env_rk(env_id)
        var = await self.get_key_value_as_json(rk)
        var["var"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_env_log(self, env_id: int, value: dict):
        """设置env日志"""
        rk = self.get_env_rk(env_id)
        var = await self.get_key_value_as_json(rk)
        var["log"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_case_var(self, case_id: int, value: dict):
        """设置case变量"""
        rk = self.get_case_rk(case_id)
        var = await self.get_key_value_as_json(rk)
        var["var"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_case_log(self, case_id: int, value: dict):
        """设置case日志"""
        rk = self.get_case_rk(case_id)
        var = await self.get_key_value_as_json(rk)
        var["log"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def get_var_value(
        self, var_key: str, env_id: int = None, case_id: Union[str, int] = None, is_env: bool = True
    ):
        """
        获取变量值
        :param var_key: 变量的存储key值
        :param env_id: 环境ID和用例ID必须传一个
        :param case_id: 环境ID和用例ID必须传一个
        :param is_env: 是否为环境
        :return:
        """
        if is_env:
            rk = self.get_env_rk(env_id)
        else:
            rk = self.get_case_rk(case_id)

        get_value_from_redis = await self.get_key_value_as_json(rk)
        return get_value_from_redis.get("var", {}).get(var_key, None)
