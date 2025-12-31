# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

import re
import math
from typing import Any, Dict, List, Sequence
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator
from pydantic import BaseModel as PydanticBaseModel
from pydantic.utils import ROOT_KEY
from pydantic.errors import PydanticValueError
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from common.constants import ErrorCode, ErrorNT


class BaseModel(PydanticBaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        if __pydantic_self__.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


class ResponseData(BaseModel):
    response: dict
    responseCde: int
    responseMsg: str
    timestamp: str
    responseTimeInSecs: float


class ResponseDataList(BaseModel):
    response: List[dict]
    responseCde: int
    responseMsg: str
    timestamp: str
    responseTimeInSecs: float


class KeyValuePair(BaseModel):
    __root__: Dict[str, str]


class StepConfig(BaseModel):
    class Config:
        extra = Extra.forbid
    entryPoint: List[str]
    stepArguments: List[str]
    imageUri: str

    @root_validator(pre=True)
    def validate_step_config(cls, values):
        errors = []
        v = values.get('stepArguments')
        if "" in v:
            error = ValidationError(
                ErrorCode.STEP_ARGUMENT_EMPTY_STRING_NOT_ALLOWED)
            errors.append(error)

        v = values.get('imageUri')
        if len(v.strip()) < 1:
            error = ValidationError(
                ErrorCode.IMAGE_URI_EMPTY_STRING_NOT_ALLOWED)
            errors.append(error)

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values


class ComputeDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    type: str
    maxQty: int
    memory: str
    minQty: int

    @root_validator(pre=True)
    def validate(cls, values):
        errors = []

        if values.get('maxQty') < values.get('minQty'):
            error = ValidationError(ErrorCode.MAX_QTY_LESS_THAN_MIN_QTY)
            errors.append(error)

        v = values.get('type')
        ALLOWED_VALUES = ['cpu', 'gpu']
        if v.lower() not in ALLOWED_VALUES:
            error = ValidationError(ErrorCode.COMPUTE_TYPE_VALUES_ALLOWED)
            errors.append(error)

        if v.lower() == 'gpu':
            error = ValidationError(ErrorCode.GPU_NOT_ALLOWED)
            errors.append(error)

        v = values.get('memory')
        pattern = r'^[0-9]+.*GB$'
        if not re.match(pattern, v):
            error = ValidationError(
                ErrorCode.STORAGE_MEMORY)
            errors.append(error)
        if re.match(pattern, v):
            memory_value = int(v.split('GB')[0])
            # 1 GB = 0.93132257461548 GiB
            convert_to_GiB = math.ceil(memory_value * (0.93132257461548))
            values['memory'] = f'{str(convert_to_GiB)}Gi'
            print(values)
        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values


class ResourceConfig(BaseModel):
    class Config:
        extra = Extra.forbid
    computes: List[ComputeDetails]
    volumeSizeinGB: float


class StepDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    type: str
    dependsOn: List[str]
    input: KeyValuePair
    output: KeyValuePair
    stepConfig: StepConfig
    resourceConfig: ResourceConfig


class Step(BaseModel):
    __root__: Dict[str, StepDetails]


class EnvVariable(BaseModel):
    name: str


class InputArtifacts(BaseModel):
    storage_type: str
    uri: str


class OutputArtifacts(BaseModel):
    storage_type: str
    uri: str


class Framework(BaseModel):
    name: str
    version: str


class Storage(BaseModel):
    class Config:
        extra = Extra.forbid
    storageType: str
    name: str
    uri: str

    @root_validator(pre=True)
    def validate_storage(cls, values):
        errors = []
        v = values.get('storageType')
        if len(v.strip()) < 1:
            error = ValidationError(
                ErrorCode.STORAGE_TYPE_EMPTY_NOT_ALLOWED)
            errors.append(error)

        ALLOWED_VALUES = ["MINIO", "NUTANIX"]
        if values.get('storageType').upper() not in ALLOWED_VALUES:
            error = ValidationError(
                ErrorCode.STORAGE_TYPE_VALUES_ALLOWED)
            errors.append(error)

        v = values.get('uri')
        pattern = r'^[a-zA-Z0-9]+://(.*)$'
        if not re.match(pattern, v):
            error = ValidationError(
                ErrorCode.STORAGE_INVALID_URI)
            errors.append(error)

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values


class Pipeline(BaseModel):
    class Config:
        extra = Extra.forbid
    name: str
    operator: str
    runtime: str
    dataStorage: List[Storage]
    flow: Step
    variables: KeyValuePair
    globalVariables: KeyValuePair

    @root_validator(pre=True)
    def validate_pipeline(cls, values):
        errors = []
        v = values.get('name')
        if len(v.strip()) < 1:
            error = ValidationError(
                ErrorCode.PIPELINE_NAME_MANDATORY)
            errors.append(error)

        v = values.get('operator')
        ALLOWED_VALUES = ['kubeflow', 'airflow']
        if v.lower() not in ALLOWED_VALUES:
            error = ValidationError(
                ErrorCode.PIPELINE_OPERATOR_VALUES_ALLOWED)
            errors.append(error)

        v = values.get('runtime')
        ALLOWED_VALUES = ['kubernetes', 'vm']
        if v.lower() not in ALLOWED_VALUES:
            error = ValidationError(
                ErrorCode.PIPELINE_RUNTIME_VALUES_ALLOWED)
            errors.append(error)

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values


class ProjectDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    projectId: str
    version: int
    # name: str
    description: str
    pipeline: Pipeline


class SubmitResData(ResponseData):
    pass


class SubmitPipelineResData(ResponseData):
    pass


class SubmitExecutionResData(ResponseData):
    pass


class SubmitFormDataResData(ResponseData):
    pass


class GetProjectIdResultData(ResponseDataList):
    pass


class GetFormDataResultData(ResponseDataList):
    pass


class GetResultResData(ResponseData):
    pass


class UpdateExecutionDetails(BaseModel):
    executionId: str
    statusCde: int


class PipelineDetails(BaseModel):
    dataStorage: List[Storage]
    variables: KeyValuePair
    globalVariables: KeyValuePair


class RunTimeInput(BaseModel):
    pipeline: PipelineDetails


class ValidationError(PydanticValueError):
    def __init__(self, error_detail: ErrorNT, **ctx: any) -> None:
        super().__init__(**ctx)
        PydanticValueError.code = str(error_detail.value.code)
        PydanticValueError.msg_template = error_detail.value.message
