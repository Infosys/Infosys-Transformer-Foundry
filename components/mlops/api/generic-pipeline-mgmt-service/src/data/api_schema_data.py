# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
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
from typing import Optional
from common.constants import ErrorCode, ErrorNT

class ResponseData(BaseModel):
    response: dict
    responseCde: int
    responseMsg: str
    timestamp: str
    responseTimeInSecs: float

class ResponseMessage(BaseModel):
    code: int
    status:str
    data:Optional[dict]

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

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values

class VolumeDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    scope : str
    name : str
    mountPath : str
    sizeinGB : Optional[int]

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

        if v == "GPU":
            if values.get('memory') != "20GB" and values.get('memory') != "80GB" and values.get('memory') != "40GB":
                error = ValidationError(ErrorCode.GPU_MEMORY)
                errors.append(error)
            if values.get('maxQty') != 1:
                error = ValidationError(ErrorCode.GPU_MAXQTY)
                errors.append(error)
            if values.get('minQty') != 1:
                error = ValidationError(ErrorCode.GPU_MINQTY)
                errors.append(error)

        v = values.get('memory')
        pattern = r'^[0-9]+.*GB$'
        if not re.match(pattern, v):
            error = ValidationError(
                ErrorCode.STORAGE_MEMORY)
            errors.append(error)

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),
            ])
        else:
            return values

class ResourceConfig(BaseModel):
    class Config:
        extra = Extra.forbid
    computes: List[ComputeDetails]

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

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values

class StepDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    type: str
    dependsOn: List[str]
    inputArtifacts : Optional[Storage]
    input: KeyValuePair
    output: KeyValuePair
    stepConfig: StepConfig
    resourceConfig: ResourceConfig

class Step(BaseModel):
    __root__: Dict[str, StepDetails]

    @root_validator(pre=True)
    def validate_storage(cls, values):
        errors = []
        v = values.get('__root__')
        step_name_list = list(v.keys())
        pattern = r"^[a-z0-9-]+$"
        umatched_steps = [
            x for x in step_name_list if not re.match(pattern, x)]
        for i in umatched_steps:
            if len(i) == 0:
                error = ValidationError(
                    ErrorCode.FLOW_STEP_NAME_ERROR)
                errors.append(error)
            else:
                if len(umatched_steps) > 0:
                    error = ValidationError(ErrorCode.FLOW_STEP_NAME)
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

class Pipeline(BaseModel):
    class Config:
        extra = Extra.forbid
    name: str
    operator: str
    runtime: str
    dataStorage: List[Storage]
    volume : Optional[VolumeDetails]
    flow: Step
    variables: KeyValuePair
    globalVariables: KeyValuePair

    @root_validator(pre=True)
    def validate_pipeline(cls, values):
        errors = []
        if 'inputArtifacts' in values:
            if not bool(values.get('inputArtifacts')):
                error = ValidationError(
                    ErrorCode.PIPELINE_INPUTARTIFACTS)
                errors.append(error)
        v = values.get('name')
        if len(v.strip()) < 1:
            error = ValidationError(
                ErrorCode.PIPELINE_NAME_MANDATORY)
            errors.append(error)
        else:
            pattern = r"^[a-z0-9-]+$"
            if not (re.match(pattern, v)):
                error = ValidationError(
                    ErrorCode.PIPELINE_NAME_ACCEPTS)
                errors.append(error)

        v = values.get('operator')
        ALLOWED_VALUES = ['kubeflow', 'airflow']
        if v != "":
            if v.lower() not in ALLOWED_VALUES:
                error = ValidationError(
                    ErrorCode.PIPELINE_OPERATOR_VALUES_ALLOWED)
                errors.append(error)
            if v.lower()=='airflow':
                error = ValidationError(
                    ErrorCode.AIRFLOW_ERROR)
                errors.append(error)

        v = values.get('runtime')
        ALLOWED_VALUES = ['kubernetes', 'vm']
        if v != "":
            if v.lower() not in ALLOWED_VALUES:
                error = ValidationError(
                    ErrorCode.PIPELINE_RUNTIME_VALUES_ALLOWED)
                errors.append(error)
            if v.lower()=='vm':
                error = ValidationError(
                    ErrorCode.VM_ERROR)
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
    description: str
    pipeline: Pipeline

class PipelineUpdateDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    projectId: str
    version: int
    description: str
    pipeline: Pipeline
    id:str

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

class GetFormDataResultData(ResponseData):
    pass

class GetResultResData(ResponseData):
    pass

class GetResponseData(ResponseMessage):
    pass

class UpdateExecutionDetails(BaseModel):
    executionId: str
    statusCde: int

class FormDataDetails(BaseModel):
    nodes: List
    edges: List
    pipelineId: str
    projectId: str

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