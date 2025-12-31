# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import List,Optional
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from aicloudlibs.constants.error_constants import *
from aicloudlibs.schemas.global_schema import ApiResponse,AuditableColumns, ValidationError
import dataset.constants.local_constants as local_errors
import regex as re
from aicloudlibs.constants.util_constants import *
# from dataset.exception.exception import *

arg_name_regex =  r'[a-zA-Z0-9_]+$'
name_regex =  r'[a-zA-Z0-9-]+$'
num_regex = r'[0-9]+$'
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class ScopeType(str, Enum):
    PUBLIC="public"
    RESTRICTED="restricted"

class DataStorageSchema(BaseModel):
    storageType : str
    uri : str


class Dataset(BaseModel):
    name : str
    version : int
    description : Optional[str] = None
    scope : ScopeType
    userlist:Optional[List[str]] = []
    size : int
    task : str
    modality : str
    language : str
    license : Optional[str] = None
    purpose : Optional[str] = None
    usecase : Optional[str] = None
    format : Optional[str] = None
    limitation : Optional[str] = None
    tags: List[str] 
    dataStorage : DataStorageSchema


class DataSchema(AuditableColumns):
    projectId: str
    dataset: Dataset

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
                
            schema["properties"] = props

    @root_validator(pre=True)
    def validateDatasetDetails(cls, values):
        errors=[]

        projectId=values.get("projectId")
        
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            errors.append(error)

        
        datasetData=values.get("dataset")
        datasetEmptyErr=False
        if (datasetData is None or( datasetData is not None and len(datasetData)==0)):
            error=ValidationError(local_errors.ErrorCode.DATASET_DATA_NOT_EMPTY_ERROR) # create a const var
            datasetEmptyErr=True
            errors.append(error)

        if not datasetEmptyErr:      
            
            name= datasetData.get("name")
            datasetnameEmptyErr=False
            if (name is None or (name is not None and len(name) == 0)):
                error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
                datasetnameEmptyErr=True
                errors.append(error)

            if not datasetnameEmptyErr and (not re.fullmatch(name_regex,name)):
                print("inside alphacheck")
                error=ValidationError(ErrorCode.PIPLN_NAME_SPECIAL_CHARS_ERROR)
                errors.append(error)

            if not datasetnameEmptyErr and len(name)>int(NAME_MAX_LENGTH):
                error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
                errors.append(error)

            version=datasetData.get("version")
            if (version is None):
                error= ValidationError(ErrorCode.VERSION_NOT_EMPTY_ERROR)
                print(error)
                errors.append(error)
       
            
            if 'scope' in datasetData and datasetData.get('scope') == ScopeType.PUBLIC:
                datasetData['userlist'] = []

            else:
                userlist = datasetData.get("userlist", [])
                if len(userlist)>0:
                    userEmailEmptyErr=False
                    for user in userlist:
                        if (user is None or (user is not None and len(user)==0)):
                            error= ValidationError(ErrorCode.USER_EMAIL_NOT_EMPTY)
                            print(error)
                            errors.append(error)
                            userEmailEmptyErr=True

                    if (not userEmailEmptyErr and (not re.fullmatch(email_regex, user))): 
                        error= ValidationError(ErrorCode.USER_EMAIL_INVALID)
                        print(error)
                        errors.append(error)
                        
            size=datasetData.get("size")
            if (size is None):
                error= ValidationError(ErrorCode.SIZE_NOT_EMPTY_ERROR) 
                print(error)
                errors.append(error)

            task=datasetData.get("task")
            if (task is None or (task is not None and len(task)==0)): 
                error= ValidationError(ErrorCode.TASK_EMPTY_ERROR) 
                print(error)
                errors.append(error)

            modality=datasetData.get("modality")
            if (modality is None or (modality is not None and len(modality)==0)): 
                error= ValidationError(local_errors.ErrorCode.MODALITY_NOT_EMPTY_ERROR) 
                print(error)
                errors.append(error)

            language=datasetData.get("language")
            if (language is None or (language is not None and len(language)==0)): 
                error= ValidationError(ErrorCode.LANGUAGE_EMPTY_ERROR) 
                print(error)
                errors.append(error)

            tags=datasetData.get("tags")
            if (len(tags)==0): 
                error= ValidationError(local_errors.ErrorCode.TAGS_NOT_EMPTY_ERROR) 
                print(error)
                errors.append(error)

            dataStorage=datasetData.get("dataStorage")
            dataStorageEmptyErr=False
            if (dataStorage is None or( dataStorage is not None and len(dataStorage)==0)):
                error=ValidationError(ErrorCode.DATASTORAGE_EMPTY_ERROR) 
                dataStorageEmptyErr=True
                errors.append(error)

            if not dataStorageEmptyErr:
                storageType=dataStorage.get("storageType")
                uri=dataStorage.get("uri")
                storageTypeErr=False
                uriErr=False
                if (storageType is None or (storageType is not None and len(storageType)==0)):
                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                    errors.append(error)
                    storageTypeErr=True

                if (not storageTypeErr and (storageType not in GPMS_STORAGE_OPTIONS)):
                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                    errors.append(error)

                if (uri is None or (uri is not None and len(uri)==0)):
                    error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                    errors.append(error)
                    uriErr=True

                if (not uriErr and (not uri.startswith("s3://"))):
                    error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
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
    
    
class DatasetJobStatusEnum(str,Enum):
    Registered="Registered"
    Updated="Updated"
    Deleted="Deleted"
    Failed="Failed"

class DatasetResponseData(DataSchema):
    id: str = None
    status:DatasetJobStatusEnum=Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class DatasetResponse(ApiResponse):
    data : Optional[DatasetResponseData] = None

class UserlistResponseData(BaseModel):
    userlist : Optional[List] = None

class UserlistResponse(ApiResponse):
    data : Optional[UserlistResponseData] = None

class ListDatasetResponseData(BaseModel):
    datasets : Optional[List[DatasetResponseData]] = None

class ListDatasetResponse(ApiResponse):
    data : Optional[ListDatasetResponseData] = None

class GetDatasetResponseData(BaseModel):
    dataset:  Optional[DatasetResponseData] = None

class GetDatasetResponse(ApiResponse):
    data : Optional[GetDatasetResponseData] = None

class DeleteDatasetResponse(ApiResponse):
    data : Optional[str] = None