import json
from typing import Union, List, Optional

from pydantic import BaseModel, Field, validator

from app.services.api_case.case.schema.info import OutCaseUrlInfo, OutCaseBodyInfo, OutCaseBasicInfo
from app.services.api_case.case_params.headers.schema.info import DebugHeaderInfo
from app.services.api_case.case_params.query.schema.info import DebugParamsInfo
from app.services.api_case.settings.asserts.schema.info import DebugAssertInfo
from app.services.api_case.settings.extract.schema.info import DebugExtractInfo
from app.services.api_case.settings.suffix.schema.info import DebugCaseSuffixInfo


class OutDebugResponse(BaseModel):
    status_code: int
    request_headers: dict = Field({}, description="请求头")
    request_data: Optional[dict] = Field(None, description="请求数据")
    response_headers: dict = Field({}, description="响应数据")
    response: Optional[Union[dict, str]] = Field(None, description="响应数据")
    elapsed: str = Field(None, description="响应时间")
    cookie: str = Field(None, description="cookie")
    json_format: bool = Field(False, description="是否格式化json")
    url: str = Field(..., description="请求地址")
    method: str = Field(..., description="请求方法")
    extract_result: List[dict] = Field([], description="提取结果")
    assert_result: List[dict] = Field([], description="断言结果")
    env_assert: List[dict] = Field([], description="环境断言结果")
    case_assert: List[dict] = Field([], description="用例断言结果")
    final_result: bool = Field(False, description="最终结果")


class RequestDebugForm(BaseModel):
    env_id: int = Field(..., title="环境id")
    url_info: OutCaseUrlInfo = Field(..., title="请求地址信息")
    basic_info: OutCaseBasicInfo = Field(None)
    body_info: OutCaseBodyInfo = Field(..., title="请求体信息")
    query_info: List[DebugParamsInfo] = Field([], title="请求参数信息")
    path_info: List[DebugParamsInfo] = Field([], title="路径参数信息")
    header_info: List[DebugHeaderInfo] = Field([], title="请求头信息")
    prefix_info: List[DebugCaseSuffixInfo] = Field([], title="前置信息")
    suffix_info: List[DebugCaseSuffixInfo] = Field([], title="后置信息")
    assert_info: List[DebugAssertInfo] = Field([], title="断言信息")
    extract_info: List[DebugExtractInfo] = Field([], title="提取信息")
