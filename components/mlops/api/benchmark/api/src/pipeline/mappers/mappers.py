# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#
"""
fileName: mappers.py
description: A Pydantic model object for usecase entity model 
             which maps the data model to the usecase entity schema
"""

from pydantic import BaseModel,Field,root_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from aicloudlibs.schemas.global_schema import ApiResponse
from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ContainerSpec,PyObjectId,ApiResponse,ValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper
from fastapi.exceptions import RequestValidationError
import regex as re
from typing import Optional

arg_name_regex =  r'[a-zA-Z0-9_]+$'
name_regex =  r'[a-zA-Z0-9-]+$'
num_regex = r'[0-9]+$'

class CreateUpdateSchema(BaseModel):
    createdOn: str = datetime
    createdBy: str = None
    modifiedOn: str = datetime
    updatedBy: str = None

class StatusSchema(BaseModel):
    runId: str = None
    status: str = None

#Benchmark
class ArgsSchema(BaseModel):
    name : str
    value : str

class ModelSchema(BaseModel):
    modelName : str
    modelPathorId : Optional[str]
    datatype : str
    quantizeMethod : str
    args : List[ArgsSchema]

class DataSchema(BaseModel):
    name : str
    scope : str
    language : str
    batchSize : int
    limit : int

class DataStorageSchema(BaseModel):
    storageType: str
    uri: str

class ConfigSchema(BaseModel):
    model: List[ModelSchema]
    data : List[DataSchema]
    task: str
    dataStorage : DataStorageSchema

class VolumeSchema(BaseModel):
    name : str
    mountPath : str
    sizeinGB : int

class ResourceConfigSchema(BaseModel):
    gpuQty : int
    gpuMemory : str
    volume : VolumeSchema

class BenchmarkPipeline(BaseModel):
    projectId: Optional[str]
    name: str
    description: str
    type: str
    configuration: ConfigSchema
    resourceConfig: ResourceConfigSchema

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
                
            schema["properties"] = props

    @root_validator(pre=True)
    def validateBenchmark(cls,values):
        errors=[]

        name=values.get("name")
        piplnnameEmptyErr=False
        if name == "":
            error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
            piplnnameEmptyErr=True
            errors.append(error) 
        else:
            if (not re.fullmatch(name_regex,name)):
                print("inside alphacheck")
                error= ValidationError(ErrorCode.PIPLN_NAME_SPECIAL_CHARS_ERROR)
                errors.append(error) 
        
        if(not piplnnameEmptyErr and len(name)>int(NAME_MAX_LENGTH)):
            error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
            errors.append(error)
        
        type=values.get("type")
        if (type is None or (type is not None and len(type) == 0)):
            error= ValidationError(ErrorCode.BENCHMARK_TYPE_REQUIRED)
            print(error)
            errors.append(error)
        if(type.lower()) not in ["code","text","embedding"]:
            error= ValidationError(ErrorCode.BENCHMARK_TYPE_VALUE_ERROR)
            print(error)
            errors.append(error)
        
        configuration=values.get("configuration")
        
        configurationEmptyErr=False
        if (configuration is None or (configuration is not None and len(configuration) == 0)):
            error= ValidationError(ErrorCode.BENCHMARK_CONFIG_EMPTY_ERROR)
            print(error)
            errors.append(error)
            configurationEmptyErr=True
        if not configurationEmptyErr:
            modelEmptyErr=False
            dataEmptyErr=False
            
            if(configuration.get('model') is None or len(configuration.get('model'))==0):
                error= ValidationError(ErrorCode.MODEL_EMPTY_ERROR)
                print(error)
                errors.append(error)
                modelEmptyErr=True
            if(not modelEmptyErr):
                model=configuration.get('model')
                for item in model:
                    print("item",item)
                    modelPathorIdEmptyErr =False
                    datatypeEmptyErr = False
                    quantizeMethodEmptyErr = False
                    if (item.get('modelName') is None or (item.get('modelName') is not None and  len(item.get('modelName'))==0)):
                        error= ValidationError(ErrorCode.MODEL_NAME_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                    else:
                        if (not re.fullmatch(name_regex,item.get('modelName'))):
                            print("inside alphacheck")
                            error= ValidationError(ErrorCode.BENCHMARK_MODEL_NAME_SPECIAL_CHARS_ERROR)
                            errors.append(error) 

                       
                    if (item.get('modelPathorId') is None or (item.get('modelPathorId') is not None and  len(item.get('modelPathorId'))==0)):
                        error= ValidationError(ErrorCode.MODEL_PATH_OR_ID_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        modelPathorIdEmptyErr=True
                    else:
                        if (not item.get('modelPathorId').startswith("s3://")):
                            error= ValidationError(ErrorCode.MODEL_PATH_URI_ERROR)
                            print(error)
                            errors.append(error)
                            modelPathorIdEmptyErr=True
                    if (item.get('datatype') is None or (item.get('datatype') is not None and  len(item.get('datatype'))==0)):
                        error= ValidationError(ErrorCode.DATATYPE_NOT_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        datatypeEmptyErr=True
                    else:
                        if(item.get('datatype').lower() not in ["int4","int8","fp16","fp32"]):
                            error= ValidationError(ErrorCode.BENCHMARK_DATA_TYPE_ERROR)
                            print(error)
                            errors.append(error)
                    if (item.get('quantizeMethod') is None or (item.get('quantizeMethod') is not None and  len(item.get('quantizeMethod'))==0)):
                        error= ValidationError(ErrorCode.QUANTIZEMETHOD_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        quantizeMethodEmptyErr=True 
                    else:
                        if(item.get('datatype').lower() in ["int4","int8"] and item.get('quantizeMethod').lower() not in ["static","dynamic"]):
                            print(item.get('quantizeMethod'))
                            error= ValidationError(ErrorCode.QUANTIZEMETHOD_VALUES_ERROR)
                            print(error)
                            errors.append(error)   
                    
                    args=item.get("args")
                    print("args:",args)
                    argsEmptyErr=False
                    if (not argsEmptyErr):
                        args=item.get("args")

                        for arg in args:
                            nameEmptyErr=False
                            valueEmpty=False
                            print("name",arg.get('name'))
                            if (arg.get('name') is None or (arg.get('name') is not None and  len(arg.get('name'))==0)):
                                error= ValidationError(ErrorCode.MODEL_ARGUMENT_NAME_ERROR)
                                print(error)
                                errors.append(error)
                                nameEmptyErr=True    
                            if (arg.get('value') is None or (arg.get('value') is not None and  len(arg.get('value'))==0)):
                                error= ValidationError(ErrorCode.MODEL_ARGUMENT_VALUE_ERROR)
                                print(error)
                                errors.append(error)
                                valueEmptyErr=True                       
            if(configuration.get('data') is None or len(configuration.get('data')) == 0):
                error= ValidationError(ErrorCode.DATA_EMPTY_ERROR)
                print(error)
                errors.append(error)
                dataEmptyErr=True
            if(not dataEmptyErr):
                print("data:",configuration.get('data'))
                data=configuration.get('data')
                for item in data:
                    nameEmptyErr =False
                    scopeEmptyErr =False
                    languageEmptyErr =False
                    batchSizeEmptyErr =False
                    limitEmptyErr =False
                    if (item.get('name') is None or (item.get('name') is not None and  len(item.get('name'))==0)):
                        error= ValidationError(ErrorCode.DATASET_NAME_NOT_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        nameEmptyErr=True
                    if (item.get('scope') is None or (item.get('scope') is not None and  len(item.get('scope'))==0)):
                        error= ValidationError(ErrorCode.SCOPE_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        scopeEmptyErr=True
                    else:
                        if item.get('scope') not in ["public","infosys"]:
                            error= ValidationError(ErrorCode.SCOPE_VALUE_ERROR)
                            print(error)
                            errors.append(error)
                            scopeEmptyErr=True

                    if (item.get('language') is None or (item.get('language') is not None and  len(item.get('language'))==0)):
                        error= ValidationError(ErrorCode.LANGUAGE_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        languageEmptyErrEmptyErr=True
                    if item.get('batchSize') is None:
                        error= ValidationError(ErrorCode.BATCHSIZE_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        batchSizeEmptyErr=True
                    else:
                        if not(item.get('batchSize')<=50 and item.get('batchSize')>=1):
                            error= ValidationError(ErrorCode.BATCHSIZE_VALUE_ERROR)
                            print(error)
                            errors.append(error)
                            batchSizeEmptyErr=True
                   
                    if item.get('limit') is None :
                        error= ValidationError(ErrorCode.LIMIT_EMPTY_ERROR)
                        print(error)
                        errors.append(error)
                        limitEmptyErr=True
                    else:
                        if not(item.get('limit')<=15000 and item.get('limit')>=1):
                            error= ValidationError(ErrorCode.LIMIT_VALUE_ERROR)
                            print(error)
                            errors.append(error)
                            batchSizeEmptyErr=True
            if(configuration.get('task') is None or len(configuration.get('task'))==0):
                error= ValidationError(ErrorCode.TASK_EMPTY_ERROR)
                print(error)
                errors.append(error)
            if(configuration['dataStorage'] is not None and len(configuration['dataStorage'])>0):
                dataStorage=configuration['dataStorage']
                dataStorageError=False
                dataStorageUriError=False
                
                if (dataStorage.get('storageType') is None or (dataStorage.get('storageType') is not None and len(dataStorage.get('storageType'))==0)):
                        error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                        errors.append(error)
                        dataStorageError=True
                if(not dataStorageError and ( not hasattr(StorageTypeEnum,dataStorage.get('storageType')))):
                        error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                        errors.append(error)

                if(not dataStorageError and (dataStorage.get('uri') is None or (dataStorage.get('uri') is not None and len(dataStorage.get('uri'))==0))):
                        error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                        errors.append(error)
                        inputArtifactUriError=True
                if(not dataStorageUriError and (not dataStorage.get('uri').startswith("s3://"))):
                        error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                        errors.append(error)
            else:
                error= ValidationError(ErrorCode.DATASTORAGE_EMPTY_ERROR)
                print(error)
                errors.append(error)

        resourceConfig=values.get("resourceConfig")
        resourceConfigEmptyErr=False
        if (resourceConfig is None or (resourceConfig is not None and len(resourceConfig) == 0)):
            error= ValidationError(ErrorCode.RESOURCECONFIG_EMPTY_ERROR)
            print(error)
            errors.append(error)
            resourceConfigEmptyErr=True
        if not resourceConfigEmptyErr:
             
            print(resourceConfig)
            if(resourceConfig.get('gpuQty') is None ):
                error= ValidationError(ErrorCode.GPU_QUANTITY_NOT_EMPTY)
                print(error)
                errors.append(error)
            if(resourceConfig.get('gpuMemory') is None ):
                error= ValidationError(ErrorCode.GPU_MEMORY_VALUE_ERROR)
                print(error)
                errors.append(error)
            else:
                if( resourceConfig.get('gpuMemory').lower() not in ["20gb","40gb","80gb"]):
                    error= ValidationError(ErrorCode.GPU_MEMORY_ERROR)
                    print(error)
                    errors.append(error) 
            if(resourceConfig.get('volume') is None ):
                  error= ValidationError(ErrorCode.VOLUME_EMPTY_ERROR)
                  print(error)
                  errors.append(error)
            if(resourceConfig.get('volume') is not None and len(resourceConfig.get('volume'))>0):
                volume=resourceConfig.get('volume')
                nameError=False
                mountPathError=False
                
                if (volume.get('name') is None or (volume.get('name') is not None and len(volume.get('name'))==0)):
                        error=ValidationError(ErrorCode.VOLUMEN_NAME_ERROR)
                        errors.append(error)
                        nameError=True
                if (volume.get('mountPath') is None or (volume.get('mountPath') is not None and len(volume.get('mountPath'))==0)):
                        error=ValidationError(ErrorCode.MOUNTPATH_EMPTY_ERROR)
                        errors.append(error)
                        mountPathError=True
                else:
                    if not volume.get('mountPath').startswith("/"):
                        error=ValidationError(ErrorCode.VOLUME_PATH_ERROR)
                        errors.append(error)
                        mountPathError=True
                if (volume.get('sizeinGB')) is None:
                        error=ValidationError(ErrorCode.SIZE_NOT_EMPTY_ERROR)
                        errors.append(error)
                        nameError=True 
                else:
                    if not(volume.get('sizeinGB')<=100 and volume.get('sizeinGB')>=1):
                        error= ValidationError(ErrorCode.SIZEINGB_VALUE_ERROR)
                        print(error)
                        errors.append(error)
                        batchSizeEmptyErr=True  
                    
        if len(errors)>0:
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values

class ResponseMessage(BaseModel):
    code: int 
    status:str
    data:Optional[dict]

class ApiResponse(BaseModel):
      code: int
      status:str
      data:Optional[dict]

class PipelineJobStatusEnum(str,Enum):
    Created="Created"
    Updated="Updated"
    Deleted="Deleted"
    InProgress = "INPROGRESS"
    Success = "Succeeded"
    Failure = "Failure"

class PipelineResponseData(BenchmarkPipeline):
    id: str = None
    status:PipelineJobStatusEnum=Field()
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class PipelineResponse(ApiResponse):
    data: Optional[PipelineResponseData] = None

class GetResponseData(ResponseMessage):
    pass

class BenchmarkStatusEnum(str,Enum): 
    Created="Created"  
    Updated="Updated"
    InProgress="INPROGRESS"
    Success = "Succeeded"
    Failed = "Failed"
    
class GetBenchmarkStatusResponseData(BaseModel):
    id:str = None
    status:BenchmarkStatusEnum=Field(default=BenchmarkStatusEnum.Created)

class GetBenchmarkStatusResponse(ApiResponse):
    data: Optional[GetBenchmarkStatusResponseData] =None

class ListBenchmarkMetadata(BaseModel):
      code: int =Field(default=200)
      status:str=Field(default="SUCCESS")
      data:Optional[dict]
      
class ListBenchmarkResponseData(BaseModel):
    benchmarks: Optional[List[PipelineResponseData]] = None

class ListBenchmarkResponse(ApiResponse):
    data: Optional[ListBenchmarkResponseData] = None

class Benchmarktype(str, Enum):
    code = "code"
    text = "text" 
    embedded="embedding"
    
class Metadatatype(str, Enum):
    task = "task"
    modelGenArgs="modelGenArgs"

def ResponseModel(data):
    return {"code": 200, "status": "SUCCESS", "data": data}

def ErrorResponseModel(code, message):
    return {"code": code, "status": "FAILURE", "message": message}