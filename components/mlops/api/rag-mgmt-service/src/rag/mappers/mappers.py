# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: mappers.py
description: A Pydantic model object for usecase entity model 
             which maps the data model to the usecase entity schema
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Optional
from aicloudlibs.constants.error_constants import *
from aicloudlibs.schemas.global_schema import ApiResponse,AuditableColumns
from pydantic import BaseModel,Field,root_validator
from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ContainerSpec,PyObjectId,ApiResponse,ValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper
from fastapi.exceptions import RequestValidationError
from rag.constants.local_constants import ErrorCode
import regex as re


arg_name_regex =  r'[a-zA-Z0-9_]+$'
name_regex =  r'[a-zA-Z0-9-]+$'
num_regex = r'[0-9]+$'


class RagJobStatusEnum(str,Enum):
    Created="Created"
    Updated="Updated"
    Deleted="Deleted"
    Deployed="Deployed"
    Failed="Failed"
    Inprogress = "Inprogress"
    Active = "Active"
    Inactive = "Inactive"

class RagIndex(BaseModel):
    projectId : str
    name : str
    dataset : str
    embeddingModel : str
    collectionName : str
    searchSvcInput : str

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
        print(values)
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        
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
        
        dataset=values.get("dataset")
        if (dataset is None or (dataset is not None and len(dataset) == 0)):
            error= ValidationError(ErrorCode.DATASET_REQUIRED)
            errors.append(error)

        embeddingModel = values.get("embeddingModel")
        if (embeddingModel is None or (embeddingModel is not None and len(embeddingModel) == 0)):
            error= ValidationError(ErrorCode.EMBEDDING_MODEL_REQUIRED)
            errors.append(error)
    
        collectionName = values.get("collectionName")
        if (collectionName is None or (collectionName is not None and len(collectionName) == 0)):
            error= ValidationError(ErrorCode.COLLECTION_NAME_REQUIRED)
            errors.append(error)

        searchSvcInput = values.get("searchSvcInput")   
        if (searchSvcInput is None or (searchSvcInput is not None and len(searchSvcInput) == 0)):
            error= ValidationError(ErrorCode.SEARCH_SVC_INPUT_REQUIRED)
            errors.append(error)

        if len(errors)>0:
            #print(len(errors))
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values   

class RagResponseData(RagIndex):
    id: str = None
    status:RagJobStatusEnum=Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class Index(BaseModel):
    indexName : str
    indexId : str


class IndexResponseData(Index):
    id: str = None
    status:RagJobStatusEnum=Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class IndexResponse(ApiResponse):
    data : Optional[IndexResponseData] = None


class RagResponse(ApiResponse):
    data : Optional[RagResponseData] = None

class BenchmarkStatusEnum(str,Enum): 
    Created="Created"  
    Updated="Updated"
    InProgress="Inprogress"
    Success = "Succeeded"
    Failed = "Failed"
    Active = "Active"
    Inactive = "Inactive"

class GetRagIndexStatusResponseData(BaseModel):
    indexName : str
    indexId:Optional[str] = None
    status:BenchmarkStatusEnum=Field(default=BenchmarkStatusEnum.Created)

class GetRagIndexStatusResponse(ApiResponse):
    data: Optional[GetRagIndexStatusResponseData] =None


class RagSave(BaseModel):
    indexName : str
    model : str
    collectionName : str
    RetrivalType : str

class UpdateRagSave(RagSave):
     id: str

class Page(BaseModel):  
    pageEnabled : bool
    #charLimit : int

class MultiColumn(BaseModel):
    zigzag : bool
    leftToRight : bool

class PageCharacter(BaseModel):
    pageCharacterEnabled : bool
    charLimit : int

class Segement(BaseModel):
    segementEnabled : bool
    singleCol : bool
    multiCol : MultiColumn

class ChunkingStratergy(BaseModel):
    page : Page
    segement : Segement
    pageCharacter : PageCharacter


class SetUp(BaseModel):
    projectId : str
    pipelineId : str
    name : str
    indexName : str
    chunkingStratergy : ChunkingStratergy
    embeddingModelName : str
    fileName : str
    filePath : str

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
        print(values)
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        
        pipelineId=values.get("pipelineId")
        if (pipelineId is None or (pipelineId is not None and len(pipelineId) == 0)):
            error= ValidationError(ErrorCode.PIPELINE_ID_REQUIRED)
            errors.append(error)

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

        indexName = values.get("indexName")
        if (indexName is None or (indexName is not None and len(indexName) == 0)):
            error= ValidationError(ErrorCode.INDEX_NAME_REQUIRED)
            errors.append(error)

        fileName = values.get("fileName")
        if (fileName is None or (fileName is not None and len(fileName) == 0)):
            error= ValidationError(ErrorCode.FILE_NAME_REQUIRED)
            errors.append(error)

        filePath = values.get("filePath")
        if (filePath is None or (filePath is not None and len(filePath) == 0)):
            error= ValidationError(ErrorCode.FILE_PATH_REQUIRED)
            errors.append(error)
            
        if len(errors)>0:
            #print(len(errors))
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values

class SetUpResponseData(SetUp):
    id: str = None
    status:RagJobStatusEnum=Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class SetUpResponse(ApiResponse):
    data : Optional[SetUpResponseData] = None


class FileUploadStatusEnum(str,Enum):
    Uploaded = "Uploaded"
    Failed = "Failed"

class FileUploadResponseData(BaseModel):
    path:str = None
    status:FileUploadStatusEnum=Field(default=FileUploadStatusEnum.Uploaded)

class FileUploadResponse(ApiResponse):
    data: Optional[FileUploadResponseData] =None


class MessageMetadata(BaseModel):
    chunkId: str
    pageNo: int
    sequenceNo: int
    docName: str
    documentId: str
    chunkingMethod: str
    charCount: str
    score: float
    content : str
   
class SearchDetails(BaseModel):
    chatId : str
    queryId : str
    messageMetadata : List[MessageMetadata]

class SearchResponseData(SearchDetails):
    id: str = None
    status:RagJobStatusEnum=Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props
    
class SearchResponse(ApiResponse):
    data : Optional[SearchResponseData] = None