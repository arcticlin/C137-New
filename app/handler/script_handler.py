# coding=utf-8
"""
File: script_handler.py
Author: bot
Created: 2023/8/7
Description:
"""
# coding=utf-8
"""
@author: linpang
@file: script_handler.py
@time: 2023/3/22 17:10
@description: 
"""
import re, ast, builtins, asyncio, sys

from app.exceptions.commom_exception import CustomException


class ScriptHandler:
    white_module = ["datetime", "json"]
    temp_namespace = {}

    @staticmethod
    def validate_module(script_text: str):
        imports = re.findall(r"import\s+(\w+)|from\s+(\w+)\s+import", script_text)
        valid_check = [c for c in imports if c]
        for result in valid_check:
            for module_name in result:
                if module_name and module_name not in ScriptHandler.white_module:
                    raise CustomException((400, 40900, f"脚本导入的模块: {module_name}不在白名单中, 联系管理员添加"))

    @staticmethod
    def input_checker(script_text: str):
        try:
            ast_node = ast.parse(script_text)
        except SyntaxError as e:
            raise CustomException((400, 40901, f"传入脚本存在语法异常, 无法解析. Detail:{e}"))

    @staticmethod
    def handler_timeout(signum, frame):
        raise CustomException((400, 40902, f"代码执行超时"))

    @staticmethod
    async def python_executor(get_var: str, script_text: str, check_module=True):
        # 代码格式检查
        ScriptHandler.input_checker(script_text)
        # 模块导入检查
        if check_module:
            ScriptHandler.validate_module(script_text)
        # 将传入的字符串编译为函数对象，并执行该函数
        compiled_code = compile(script_text, "<string>", "exec")
        # 将内置变量和函数添加到命名空间中
        ScriptHandler.temp_namespace.update(vars(builtins))

        try:
            # 限制递归层数, 避免出现死循环
            sys.setrecursionlimit(100)
            # 添加超时操作
            await asyncio.wait_for(
                asyncio.to_thread(exec, compiled_code, ScriptHandler.temp_namespace),
                timeout=5,
            )
            result = eval(get_var, ScriptHandler.temp_namespace)
            return {get_var: result}
        except asyncio.TimeoutError:
            raise CustomException((400, 40902, f"代码执行超时, 请检查"))
        except RecursionError:
            raise CustomException((400, 40902, f"代码递归栈溢出(限制100次), 请检查"))
        finally:
            sys.setrecursionlimit(10000)
        # exec(compiled_code, ScriptHandler.temp_namespace)

    @staticmethod
    def unsafe_checker(code_str: str):
        unsafe_modules = [
            "os",
            "sys",
            "subprocess",
            "ftplib",
            "pickle",
            "glob",
            "shutil",
            "tempfile",
        ]
        unsafe_functions = ["exec", "eval"]

        unsafe_pattern = re.compile(
            r"|".join(
                [f"import\s+({m})" for m in unsafe_modules]
                + [f"from\s+({m})\s+import" for m in unsafe_modules]
                + [f"({f})\(" for f in unsafe_functions]
            )
        )
        save_check = unsafe_pattern.search(code_str)
        if save_check:
            raise CustomException((400, 40900, f"脚本存在不可信任的模块或函数: {save_check.group()}"))
