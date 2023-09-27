# coding=utf-8
"""
File: model_collect.py
Author: bot
Created: 2023/7/25
Description:
"""
from app.models.auth.user import UserModel
from app.models.project.project import ProjectModel
from app.models.project.project_member import ProjectMemberModel
from app.models.project.project_directory import PDirectoryModel

from app.models.apicase.api_case import ApiCaseModel
from app.models.apicase.api_path import ApiPathModel
from app.models.apicase.api_headers import ApiHeadersModel

from app.models.common_config.sql_model import SqlModel
from app.models.common_config.redis_model import RedisModel
from app.models.common_config.script_model import ScriptModel

from app.models.api_settings.assert_settings import AssertModel
from app.models.api_settings.extract_settings import ExtractModel
from app.models.api_settings.suffix_settings import SuffixModel
from app.models.api_settings.env_settings import EnvModel
from app.models.apicase.api_report import ApiReportModel
