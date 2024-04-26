# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: global_schema.py
description: A Pydantic model object for global entity model 
             which maps the data model to the difeernt entity schema
"""

from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional, List,Union
from enum import Enum
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from pydantic.errors import PydanticValueError,PydanticTypeError
from aicloudlibs.constants.error_constants import ErrorCode,SUCCESS_CODE

not_authorized_error=ErrorCode.NOT_AUTHORIZED_ERROR
internal_server_error= ErrorCode.INTERBAL_SERVER_ERROR

class Compute(BaseModel):
    type:str = None
    maxQty:int =Field(default=1)
    memory:str = Field(default="10GB")
    minQty:Optional[int] = Field(default=1)
    
    

class ResourceConfig(BaseModel):
     computes: List[Compute] = None
     volumeSizeinGB:int = None

class StorageTypeEnum(str,Enum):
     INFY_AICLD_MINIO="INFY_AICLD_MINIO"
     INFY_AICLD_NUTANIX="INFY_AICLD_NUTANIX"

class Artifacts(BaseModel):
    storageType: StorageTypeEnum
    uri:str = None

class NameValuePair(BaseModel):
    name: str = None
    value: str = None

class ContainerSpec(BaseModel):
    imageUri:str
    envVariables: Optional[List[NameValuePair]]=None
    ports: Optional[List[NameValuePair]]=None
    labels: Optional[List[NameValuePair]]=None
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None

class AuditableColumns(BaseModel):
    createdBy: str  =Field(None,hidden=True)
    createdOn: datetime = Field(default_factory=datetime.utcnow,hidden=True)
    isDeleted: bool=Field(default=False,hidden=True)
    updatedBy: Optional[str] =Field(None,hidden=True)
    modifiedOn: Optional[datetime] =Field(default_factory=datetime.utcnow,hidden=True)

class ApiResponse(BaseModel):
      code: int =Field(default=200)
      status:str=Field(default="SUCCESS")
      data:Optional[dict]

class ApiErrorResponseModel(BaseModel):
    code: int
    status: str
    message: Optional[str]


class OperatorEnum(str,Enum):
    KUBEFLOW="kubeflow"
    AIRFLOW="airflow"

class VolumeScopeEnum(str,Enum):
    PIPELINE="pipeline"
    PLATFORM="platform"

class RuntimeEnum(str,Enum):
    KUBERNETES='kubernetes'
    VM='vm'

class ResourceConfigV2(BaseModel):
     computes: List[Compute] = None
     

class ValidationError(PydanticValueError):
    def __init__(self, error_detail, **ctx: any ) -> None:
          super().__init__(**ctx)
          PydanticValueError.code=str(error_detail.value.code)
          PydanticValueError.msg_template=error_detail.value.message

class ValidationTypeError(PydanticTypeError):
    def __init__(self, error_detail, **ctx: any ) -> None:
          super().__init__(**ctx)
          PydanticTypeError.code=str(error_detail.value.code)
          PydanticTypeError.msg_template=error_detail.value.message

class NotAuthorizedError(BaseModel):
    code: int =Field(default=not_authorized_error.value.code)
    status: str=Field(default="FAILED")
    message: Optional[str] = Field(default=not_authorized_error.value.message)

class InternalServerError(BaseModel):
    code: int =Field(default=internal_server_error.value.code)
    status: str=Field(default="FAILED")
    message: Optional[str] = Field(default=internal_server_error.value.message)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")