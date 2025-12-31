# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from pydantic import BaseModel,Field,root_validator
from datetime import datetime
from typing import Optional, Union, Any
from aicloudlibs.schemas.global_schema import AuditableColumns, ValidationError
from enum import Enum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from aicloudlibs.constants.error_constants import *
from prompt.constants.local_constants import ErrorMessageCode,  MODEL_MAX_LEN
from pydantic.error_wrappers import ErrorWrapper
import regex as re
import pydantic


name_regex =  r'^[a-zA-Z1-9_]+$'
endpoint_name_regex = r'[a-z0-9]+$'

""" prompt status enum """
class PromptStatusEnum(str, Enum):
    Created = "created"
    Deleted = "deleted"
    Updated = "updated"

""" audit columns for prompt request and response """
class AuditableColumns(BaseModel):
    createdBy: str  =Field(None,hidden=True)
    createdOn: datetime = Field(default_factory=datetime.utcnow,hidden=True)
    isDeleted: bool=Field(default=False,hidden=True)
    updatedBy: Optional[str] =Field(None,hidden=True)
    modifiedOn: Optional[datetime] =Field(default_factory=datetime.utcnow,hidden=True)
    
""" Model Parameters schema """
class ModelParameterMap(BaseModel):
    key: Optional[str] = None
    value: Any = None
    
""" Prompt Request schema """
class PromptRequest(AuditableColumns):
    projectId: str = None
    name: str = None
    domain: list[str] = None
    mode: str = None
    modelName: str = None
    modelId: str = None
    version: int = None
    conversationRole: Optional[str] = None
    conversationContent: str = None
    usecase: str =None
    parameters: list[ModelParameterMap] = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props

    @root_validator(pre=True)
    def validateModelDetails(cls,values):

        errors=[]
        nameEmpErr=False
        modelNameEmpErr=False

        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            errors.append(error)

        name = values.get('name')
        if (name is None  or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_PROMPT_NAME_ERROR)
            nameEmpErr=True
            errors.append(error)

        if (len(name) != 0 and not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorMessageCode.PROMPT_NAME_SPECIAL_CHAR_ERROR)
            errors.append(error)  

        if (not nameEmpErr and len(name) > MODEL_MAX_LEN):
            error= ValidationError(ErrorMessageCode.NAME_MAX_LENGTH_ERR)
            errors.append(error)
        
        domain = values.get('domain')
        if not isinstance(domain, list) or not all(isinstance(item, str) for item in domain or []):
            error = ValidationError(ErrorMessageCode.DOMAIN_MUST_BE_LIST_OF_STRINGS_ERROR)
            errors.append(error)

        if (domain is None or (domain is not None and len(domain) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_DOMAIN_ERROR)
            errors.append(error)

        mode = values.get('mode')
        if (mode is None  or (mode is not None and len(mode) == 0)):
            error= ValidationError(ErrorMessageCode.MODE_EMPTY_ERROR)
            errors.append(error)

        modelName = values.get('modelName')
        if (modelName is None  or (modelName is not None and len(modelName) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_MODEL_NAME_ERROR)
            modelNameEmpErr=True
            errors.append(error)

        if (not modelNameEmpErr and len(modelName) > MODEL_MAX_LEN):
            error= ValidationError(ErrorMessageCode.MODEL_NAME_MAX_LENGTH_ERR)
            errors.append(error)

        modelId = values.get('modelId')
        if (modelId is None  or (modelId is not None and len(modelId) == 0)):
            error= ValidationError(ErrorMessageCode.MODEL_ID_REQUIRED_ERROR)
            errors.append(error)

        convContent = values.get('conversationContent')
        if (convContent is None  or (convContent is not None and len(convContent) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR)
            errors.append(error)

        usecase = values.get('usecase')
        if (usecase is None  or (usecase is not None and len(usecase) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_USECASE_ERROR)
            errors.append(error)

        parameters = values.get('parameters')
        print("PARAMETERS",parameters)
        if len(parameters) != 0:
            for parameter in parameters:
                if parameter.get('key') == "":
                    error= ValidationError(ErrorMessageCode.EMPTY_PARAMETER_KEY_ERROR)
                    errors.append(error)
                if parameter.get('value') == "" or parameter.get('value') == None:
                    error= ValidationError(ErrorMessageCode.EMPTY_PARAMETER_VALUE_ERROR)
                    errors.append(error)
        else:
            error= ValidationError(ErrorMessageCode.PARAMETER_REQUIRED_ERROR)
            errors.append(error)

        if len(errors)>0:
            print("ERRORS",errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values

""" Prompt Response schema """
class PromptResponse(AuditableColumns):
    projectId: str = None
    name: str = None
    domain: list[str] = None
    mode: str = None
    modelName: str = None
    modelId: str = None
    version: int = None
    conversationRole: Optional[str] = None
    conversationContent: str = None
    usecase: str = None
    parameters: list[ModelParameterMap] = None
    id: str = None
    status: str = None


class UpdatePromptRequest(AuditableColumns):
    projectId: str = None
    name: str = None
    domain: list[str] = None
    mode: str = None
    modelName: str = None
    modelId: str = None
    version: int = None
    conversationRole: Optional[str] = None
    conversationContent: str = None
    usecase: str = None
    parameters: list[ModelParameterMap] = None
    id: str = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props

    @root_validator(pre=True)
    def validateModelDetails(cls,values):

        errors=[]
        nameEmpErr=False
        modelNameEmpErr=False

        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error)

        name = values.get('name')
        if (name is None  or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_PROMPT_NAME_ERROR)
            nameEmpErr=True
            errors.append(error)

        if (len(name) != 0 and not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorMessageCode.PROMPT_NAME_SPECIAL_CHAR_ERROR)
            errors.append(error)  

        if (not nameEmpErr and len(name) > NAME_MAX_LENGTH):
            error= ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
            errors.append(error)

        domain = values.get('domain')
        if not isinstance(domain, list) or not all(isinstance(item, str) for item in domain or []):
            error = ValidationError(ErrorMessageCode.DOMAIN_MUST_BE_LIST_OF_STRINGS_ERROR)
            errors.append(error)

        if (domain is None or (domain is not None and len(domain) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_DOMAIN_ERROR)
            errors.append(error)

        mode = values.get('mode')
        if (mode is None  or (mode is not None and len(mode) == 0)):
            error= ValidationError(ErrorMessageCode.MODE_EMPTY_ERROR)
            errors.append(error)

        modelName = values.get('modelName')
        if (modelName is None  or (modelName is not None and len(modelName) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_MODEL_NAME_ERROR)
            modelNameEmpErr=True
            errors.append(error)

        if (not modelNameEmpErr and len(modelName) > MODEL_NAME_MAX_LENGTH):
            error= ValidationError(ErrorCode.MODEL_NAME_MAX_LENGTH_ERROR)
            errors.append(error)

        modelId = values.get('modelId')
        if (modelId is None  or (modelId is not None and len(modelId) == 0)):
            error= ValidationError(ErrorMessageCode.MODEL_ID_REQUIRED_ERROR)
            errors.append(error)

        convContent = values.get('conversationContent')
        if (convContent is None  or (convContent is not None and len(convContent) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR)
            errors.append(error)

        usecase = values.get('usecase')
        if (usecase is None  or (usecase is not None and len(usecase) == 0)):
            error= ValidationError(ErrorMessageCode.EMPTY_USECASE_ERROR)
            errors.append(error)

        parameters = values.get('parameters')
        print("PARAMETERS",parameters)
        if len(parameters) != 0:
            for parameter in parameters:
                if parameter.get('key') == "":
                    error= ValidationError(ErrorMessageCode.EMPTY_PARAMETER_KEY_ERROR)
                    errors.append(error)
                if parameter.get('value') == "" or parameter.get('value') == None:
                    error= ValidationError(ErrorMessageCode.EMPTY_PARAMETER_VALUE_ERROR)
                    errors.append(error)
        else:
            error= ValidationError(ErrorMessageCode.PARAMETER_REQUIRED_ERROR)
            errors.append(error)

        id = values.get('id')
        if (id is None  or (id is not None and len(id) == 0)):
            error= ValidationError(ErrorMessageCode.PROMPT_ID_REQUIRED_ERROR)
            errors.append(error)

        if len(errors)>0:
            print("ERRORS",errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values