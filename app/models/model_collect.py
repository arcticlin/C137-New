# coding=utf-8
"""
File: model_collect.py
Author: bot
Created: 2023/7/25
Description:
"""
from app.models.api_case.api_case import ApiCaseModel
from app.models.api_case.api_path import ApiPathModel
from app.models.api_case.api_plan import ApiPlanModel
from app.models.api_case.api_report import ApiReportModel
from app.models.api_case.api_headers import ApiHeadersModel
from app.models.api_case.api_result import ApiCaseResultModel

from app.models.api_settings.extract_settings import ExtractModel
from app.models.api_settings.assert_settings import AssertModel
from app.models.api_settings.suffix_settings import SuffixModel

from app.models.auth.user import UserModel

from app.models.common_config.env_settings import EnvModel
from app.models.common_config.redis_model import RedisModel
from app.models.common_config.sql_model import SqlModel
from app.models.common_config.script_model import ScriptModel

from app.models.project.project import ProjectModel
from app.models.project.project_member import ProjectMemberModel
from app.models.project.project_directory import PDirectoryModel

from app.models.ws_test.ws_code import WsCodeModel
from app.models.ws_test.ws_case import WsCaseModel
from app.models.ws_test.ws_plan import WsPlanModel
from app.models.ws_test.ws_result import WsResultModel

# 加载所需模块
