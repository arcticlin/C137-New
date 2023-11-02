from typing import Union

from app.handler.redis.rds_client import RedisCli


class ApiRedis(RedisCli):
    def __init__(self, trace_id: str = None, user_id: int = None, env_id: int = None, case_id: int = None):
        super().__init__(trace_id)
        self.env_id = env_id
        self.user_id = user_id
        self.case_id = case_id

    def get_env_rk(self):
        if self.case_id is None:
            return f"api:e:e_{self.env_id}_{self.user_id}"
        return f"api:{self.trace_id}:e:e_{self.env_id}"

    def get_case_rk(self):
        """返回case redis key, 格式为: api_{trace_id}:c:c_{case_id}"""
        if self.case_id is None:
            return f"api:{self.trace_id}:c:c_temp"
        return f"api:{self.trace_id}:c:c_{self.case_id}"

    async def init_env_keys(self):
        rk = self.get_env_rk()
        check = await self.get_key_value_as_json(rk)
        if len(check) > 0:
            return
        body = dict(var={}, log=dict(env_prefix=[], env_suffix=[]))
        await self.set_key_as_json(rk, body, expired=7200)

    async def init_case_keys(self):
        rk = self.get_case_rk()
        body = dict(var={}, log=dict())
        await self.set_key_as_json(rk, body, expired=7200)

    async def set_env_var(self, value: dict):
        """设置env变量"""
        rk = self.get_env_rk()
        var = await self.get_key_value_as_json(rk)
        var["var"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_env_log(self, value: dict):
        """设置env日志"""
        rk = self.get_env_rk()
        var = await self.get_key_value_as_json(rk)
        var["log"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_case_var(self, value: dict):
        """设置case变量"""
        rk = self.get_case_rk()
        var = await self.get_key_value_as_json(rk)
        var["var"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def set_case_log(self, value: dict):
        """设置case日志"""
        rk = self.get_case_rk()
        var = await self.get_key_value_as_json(rk)
        var["log"].update(value)
        await self.set_key_as_json(rk, var, expired=7200)

    async def get_var_value(self, var_key: str, is_env: bool = False):
        """
        获取变量值
        :param var_key: 变量的存储key值
        :param env_id: 环境ID和用例ID必须传一个
        :param case_id: 环境ID和用例ID必须传一个
        :param is_env: 是否为环境
        :return:
        """
        if is_env:
            rk = self.get_env_rk()
        else:
            rk = self.get_case_rk()

        get_value_from_redis = await self.get_key_value_as_json(rk)
        return get_value_from_redis.get("var", {}).get(var_key, None)

    async def get_case_log(self):
        """设置case日志"""
        rk = self.get_case_rk()
        log = await self.get_key_value_as_json(rk)
        return log
