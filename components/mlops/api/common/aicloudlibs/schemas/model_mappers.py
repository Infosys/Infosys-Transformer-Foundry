# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: model_mappers.py
description: A Pydantic model object for model entity model 
             which maps the data model to the model entity schema
"""

from pydantic import BaseModel,Field,root_validator
from datetime import datetime
from typing import Optional, List,Union

from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ContainerSpec,ApiResponse,ValidationError
from enum import Enum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper
import regex as re
import pydantic

name_regex =  r'[a-z0-9-]+$'
endpoint_name_regex = r'[a-z0-9]+$'

class ModelUris(BaseModel):
    prefixUri: str=None
    predictUri: str=None
    explainUri: Optional[str]= None
    feedbackUri: Optional[str] = None

class ModelContainerSpec(ContainerSpec):
     healthProbeUri: str = None

class Owner(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None

class Versions(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    diff: Optional[str] = None

class Licenses(BaseModel):
    identifier: Optional[str] = None
    customText: Optional[str] = None

class References(BaseModel):
    reference: Optional[str] = None

class Citations(BaseModel):
    style: Optional[str] = None
    citation: Optional[str] = None

class CustomTags(BaseModel):
    tags: Optional[str] = None

class MetadataModelDetails(BaseModel):
     displayName: Optional[str] = None
     tasktype: Optional[str] = None
     customTags: Optional[List[CustomTags]] = None
     overview: Optional[str] = None
     documentation: Optional[str] = None
     owners: Optional[List[Owner]] = None
     versionHistory: Optional[List[Versions]] = None
     licenses: Optional[List[Licenses]] = None
     references: Optional[List[References]] = None
     citations: Optional[List[Citations]] = None
     path: Optional[str] = None

class Sensitive(BaseModel):
    Fields: Optional[List[str]] = None

class GraphicsCollection(BaseModel):
    name: Optional[str] = None
    contentEncoding: Optional[str] = None
    contentMediaType: Optional[str] = None

class Graphics(BaseModel):
    description: Optional[str] = None
    collection: Optional[List[GraphicsCollection]] = None
    
class ClassificationEnum(str,Enum):
    Public="Public"
    Private="Private"

class Data(BaseModel):
    name:  Optional[str] = None
    link:  Optional[str] = None
    sensitive:  Optional[List[Sensitive]] = None
    classification: Optional[ClassificationEnum] = None

class FormatMap(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None

class ModelParameters(BaseModel):
    modelArchitecture: Optional[str] = None
    data: Optional[List[Data]] = None
    inputFormat: Optional[str] = None
    inputFormatMap: Optional[List[FormatMap]] = None
    outputFormat: Optional[str] =None
    outputFormatMap: Optional[List[FormatMap]] = None

class ConfidenceInterval(BaseModel):
    lowerBound: Optional[str] = None
    upperBound: Optional[str] = None

class PerformanceMetrics(BaseModel):
    type: Optional[str] = None
    value: Optional[str] = None
    slice: Optional[str] = None
    confidenceInterval: Optional[ConfidenceInterval]=None

class QuantitativeAnalysis(BaseModel):
    performanceMetrics: Optional[List[PerformanceMetrics]] = None

class Description(BaseModel):
    description: Optional[str] = None

class EthicalConsiderations(BaseModel):
    name: Optional[str] = None
    mitigationStrategy: Optional[str] = None

class EnvironmentalConsiderations(BaseModel):
    hardwareType: Optional[str] = None
    hoursUsed: Optional[str] = None
    cloudProvider: Optional[str] = None
    computeRegion: Optional[str] = None
    carbonEmitted: Optional[str] = None

class MetadataConsiderations(BaseModel):
    users: Optional[List[Description]] =None
    useCases: Optional[List[Description]] =None
    limitations: Optional[List[Description]] =None
    tradeoffs: Optional[List[Description]] =None
    ethicalConsiderations: Optional[List[EthicalConsiderations]] =None
    environmentalConsiderations: Optional[List[EnvironmentalConsiderations]] =None

class ModelMetaData(BaseModel):
     modelDetails: Optional [MetadataModelDetails] =None
     modelParameters: Optional [ModelParameters] = None
     quantitativeAnalysis: Optional[QuantitativeAnalysis] = None
     considerations:Optional[MetadataConsiderations]= None

class ModelMetaDataStatusEnum(str,Enum):
    Created="Created"
    Updated="Updated"

class ModelDetails(AuditableColumns):
    name: str = None
    version: int = None
    description: Optional[str]=None
    projectId: str = None
    container: ModelContainerSpec = None
    artifacts: Optional[Artifacts] = None
    metadata: Optional[ModelMetaData] = None
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
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        name=values.get("name")
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.MODEL_NAME_NOT_EMPTY_ERROR)
            print(error)
            nameEmpErr=True
            errors.append(error) 
        
        if (not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 

        if (not nameEmpErr and len(name) > MODEL_NAME_MAX_LENGTH):
            error= ValidationError(ErrorCode.MODEL_NAME_MAX_LENGTH_ERROR)
            errors.append(error) 

        version=values.get("version")
        if (version is None ):
            error= ValidationError(ErrorCode.MODEL_VERSION_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        containerDet=values.get('container')
        containerEmptyerr=False
        contImageUriEmptyErr=False
        if(containerDet is  None or(containerDet is not None and len(containerDet)==0) ):
            error=ValidationError(ErrorCode.CONTAINER_SPEC_NOT_EMPTY)
            errors.append(error)
            containerEmptyerr=True
        if not containerEmptyerr:
           if(containerDet.get('imageUri') is None or(containerDet.get('imageUri') is not None and (len(containerDet.get('imageUri'))==0))):
                error=ValidationError(ErrorCode.CONTAINER_IMAGE_URI_EMPTY)
                errors.append(error)
                contImageUriEmptyErr=True
           if(not contImageUriEmptyErr and not containerDet.get('imageUri').startswith(INFYARTIFACTORYURI)):
                error=ValidationError(ErrorCode.CONTAINER_IMAGE_URI_VALUE_ERROR)
                errors.append(error)
           if(hasattr(containerDet,'envVariables') and containerDet.get('envVariables') is not None):
                envVar=containerDet.get('envVariables')
                
                for evar in envVar:
                    nameEmptyErr=False
                    valEmptyErr=False
                    if(evar['name'] is None or (evar['name'] is not None and len(evar['name'])==0)):
                        nameEmptyErr=True
                    if(evar['value'] is None or (evar['value'] is not None and len(evar['value'])==0)):
                        valEmptyErr=True
                if nameEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_ENV_NAME_EMPTY)
                    errors.append(error)
                if valEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_ENV_VALUE_EMPTY)
                    errors.append(error)
           if(containerDet.get('ports') is not None):
                ports=containerDet.get('ports')
                portnameEmptyErr=False
                portvalEmptyErr=False
                for port in ports:
                    print(port)
                    if(port.get('name') is None or (port.get('name') is not None and len(port.get('name'))==0)):
                        portnameEmptyErr=True
                    if(port.get('value') is None or (port.get('value') is not None and len(port.get('value'))==0)):
                        portvalEmptyErr=True
                if portnameEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_PORT_NAME_EMPTY)
                    errors.append(error)
                if portvalEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_PORT_VALUE_EMPTY)
                    errors.append(error)
            
           if(containerDet.get('labels') is not None):
                labels=containerDet.get('labels')
                labelnameEmptyErr=False
                labelvalEmptyErr=False
                labelspecialcharErr=False
                for label in labels:
                    
                    if(label.get('name') is None or (label.get('name') is not None and len(label.get('name'))==0)):
                        labelnameEmptyErr=True
                    if (not re.fullmatch(name_regex,label.get('name'))):
                        labelspecialcharErr=True
                        
                    if(label.get('value') is None or (label.get('value') is not None and len(label.get('value'))==0)):
                        labelvalEmptyErr=True
                if labelnameEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_LABEL_NAME_EMPTY)
                    errors.append(error)
                if labelvalEmptyErr:
                    error=ValidationError(ErrorCode.CONTAINER_LABEL_VALUE_EMPTY)
                    errors.append(error)
                if labelspecialcharErr:
                   error= ValidationError(ErrorCode.LABEL_NAME_SPECIAL_CHAR_ERROR)
                   errors.append(error)
           
           artifactsDet=values.get("artifacts")
           if(artifactsDet is not None and len(artifactsDet)>0):
                modelArtifactError=False
                modelArtifactUriError=False
                if (artifactsDet.get('storageType') is None or (artifactsDet.get('storageType') is not None and len(artifactsDet.get('storageType'))==0)):
                        error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                        errors.append(error)
                        modelArtifactError=True
                if(not modelArtifactError and ( not hasattr(StorageTypeEnum,artifactsDet.get('storageType')))):
                        error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                        errors.append(error)
                
                if(not modelArtifactError and (artifactsDet.get('uri') is None or (artifactsDet.get('uri') is not None and len(artifactsDet.get('uri'))==0))):
                        error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                        errors.append(error)
                        modelArtifactUriError=True

                if(not modelArtifactUriError and (not artifactsDet.get('uri').startswith("s3://"))):
                        error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                        errors.append(error)

        if len(errors)>0:
            print(errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values 

class ModelStatusEnum(str,Enum):
    Registered="Registered"
    Updated="Updated"
    Deleted="Deleted"
    Deployed="Deployed"
    Failed="Failed"

class ModelResponseData(ModelDetails):
    id: str = None
    version: int=Field(None)
    status: ModelStatusEnum=Field(default=ModelStatusEnum.Registered,description="Status of the Register Model request")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class ModelResponse(ApiResponse):
    data: Optional[ModelResponseData] = None

class TritonServingConfig(BaseModel):
    dependencyFileRepo: Optional[Artifacts] = None

class ModelConfig(BaseModel):
    modelUris: ModelUris = None
    tritonServingConfig:Optional[TritonServingConfig]=None

class InferenceSpec(BaseModel):
    minReplicaCount:Optional[int]=Field(default=1)
    maxReplicaCount:Optional[int]=Field(default=1)
    containerResourceConfig: ResourceConfig = None
    modelSpec: List[ModelConfig] =None

class ServingFrameworkEnum(str,Enum):
    Custom="Custom"
    Triton="Triton"
    Djl="Djl"

class TritonSpec(BaseModel):
    logLevel: Optional[str] = None

class ServingSpec(BaseModel):
    tritonSpec:Optional[TritonSpec]

class InferenceConfig(BaseModel):
    servingFramework: ServingFrameworkEnum
    inferenceSpec: InferenceSpec = None
    servingSpec: Optional[ServingSpec]

class Deployment(AuditableColumns):
    endpointId: str = None
    modelId: str = None
    version: int = None
    inferenceConfig: InferenceConfig = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props 

    @root_validator(pre=True)
    def validateDeployment(cls,values):
        errors=[]
        endpointId=values.get("endpointId")
        if (endpointId is None or (endpointId is not None and len(endpointId) == 0)):
            error= ValidationError(ErrorCode.ENDPOINT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        modelId=values.get("modelId")
        if (modelId is None or (modelId is not None and len(modelId) == 0)):
            error= ValidationError(ErrorCode.MODEL_ID_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 
        
        version=values.get("version")
        if (version is None ):
            error= ValidationError(ErrorCode.MODEL_VERSION_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        inferenceConfigDet=values.get('inferenceConfig')
        inferenceConfigEmptyerr=False
        if(inferenceConfigDet is  None or(inferenceConfigDet is not None and len(inferenceConfigDet)==0) ):
            error=ValidationError(ErrorCode.INFERENCE_CONFIG_EMPTY)
            errors.append(error)
            inferenceConfigEmptyerr=True
        if not inferenceConfigEmptyerr:
           servingFrameworkEmptyErr=False
           inferenceSpecEmptyerr=False
           if(inferenceConfigDet.get('servingFramework') is None or(inferenceConfigDet.get('servingFramework')  is not None and (len(inferenceConfigDet.get('servingFramework') )==0))):
                error=ValidationError(ErrorCode.SERVING_FRAMEWORK_EMPTY)
                errors.append(error)
                servingFrameworkEmptyErr=True
           if(not servingFrameworkEmptyErr and (not hasattr(ServingFrameworkEnum,inferenceConfigDet.get('servingFramework')))):
                error=ValidationError(ErrorCode.SERVING_FRAMEWORK_VALUE_ERROR)
                errors.append(error)
           if(inferenceConfigDet.get('inferenceSpec') is None or (inferenceConfigDet.get('inferenceSpec')  is not None and (len(inferenceConfigDet.get('inferenceSpec') )==0))):
                error=ValidationError(ErrorCode.INFERENCE_SPEC_EMPTY)
                errors.append(error)
                inferenceSpecEmptyerr=True
           if not inferenceSpecEmptyerr:
               inferenceSpecDet=inferenceConfigDet['inferenceSpec']
               modelSpecEmptyerr=False
               resourceConfigEmptyErr=False
               if(inferenceSpecDet.get('modelSpec') is None or(inferenceSpecDet.get('modelSpec') is not None and len(inferenceSpecDet.get('modelSpec'))==0)):
                   error=ValidationError(ErrorCode.MODEL_SPEC_EMPTY)
                   errors.append(error)
                   modelSpecEmptyerr=True
               if not modelSpecEmptyerr:
                   modelSpecs=inferenceSpecDet.get('modelSpec')
                   for modelspec in modelSpecs:
                       modelURIEmptyerr=False
                       modelUris=modelspec.get('modelUris')
                       tritonserveConfig=modelspec.get('tritonServingConfig')
                       if(modelUris is None or (modelUris is not None and len(modelUris)==0)):
                           error=ValidationError(ErrorCode.MODEL_URI_EMPTY_ERROR)
                           errors.append(error)
                           modelURIEmptyerr=True
                       if not modelURIEmptyerr:
                           if (modelUris.get('predictUri')is None or (modelUris.get('predictUri') is not None and len(modelUris.get('predictUri'))==0 )):
                              error=ValidationError(ErrorCode.PREDICT_URI_EMPTY_ERROR)
                              errors.append(error)
                           
               if(inferenceSpecDet.get('containerResourceConfig') is None or (inferenceSpecDet.get('containerResourceConfig') is not None and len(inferenceSpecDet.get('containerResourceConfig'))==0 )):
                   error=ValidationError(ErrorCode.RESOURCECONFIG_EMPTY_ERROR)
                   errors.append(error)
                   resourceConfigEmptyErr=True
                   
               if not resourceConfigEmptyErr:
                       resourceConfig= inferenceSpecDet.get('containerResourceConfig')
                       computeEmptyErr=False
                       if(resourceConfig.get('volumeSizeinGB') is None ):
                            error= ValidationError(ErrorCode.VOLUME_EMPTY_ERROR)
                            print(error)
                            errors.append(error)
                       if(resourceConfig.get('computes') is None or (resourceConfig.get('computes') is not None and len(resourceConfig.get('computes'))==0)):
                            error= ValidationError(ErrorCode.COMPUTE_LIST_EMPTY_ERROR)
                            print(error)
                            errors.append(error)
                            computeEmptyErr=True
                       if(not computeEmptyErr):
                            computes=resourceConfig.get('computes')
                            for compute in computes:
                                computeTypeEmptyErr=False
                                gpumemryEmptyErr=False
                                computeTypeInstanceErr=False
                                if (compute.get('type') is None or (compute.get('type') is not None and  len(compute.get('type'))==0)):
                                        error= ValidationError(ErrorCode.COMPUTE_TYPE_EMPTY_ERROR)
                                        print(error)
                                        errors.append(error)
                                        computeTypeEmptyErr=True
                                if( not computeTypeEmptyErr and compute.get('type').lower() not in COMPUTE_TYPE_VALUES):
                                        error= ValidationError(ErrorCode.COMPUTE_TYPE_VALUE_ERROR)
                                        print(error)
                                        errors.append(error)
                                if( not computeTypeEmptyErr and compute.get('type').lower() =='gpu' and  (compute.get('memory') is None or (compute.get('memory') is not None and len(compute.get('memory'))==0))):
                                        error= ValidationError(ErrorCode.GPU_MEMORY_NOT_EMPTY)
                                        print(error)
                                        errors.append(error)
                                        gpumemryEmptyErr=True
                                        
                                if(not computeTypeEmptyErr and not gpumemryEmptyErr and compute.get('type').lower() =='gpu' and  compute.get('memory').lower() not in MODEL_GPU_MEMORY_VALUES):
                                        error= ValidationError(ErrorCode.MODEL_GPU_MEMORY_VALUE_ERROR)
                                        print(error)
                                        errors.append(error)
                                
                                if(not computeTypeEmptyErr and not (isinstance(compute.get('maxQty'),int) or isinstance(compute.get('minQty'),int))):
                                        error= ValidationError(ErrorCode.RESOURCE_QTY_INSTANCE_ERROR)
                                        print(error)
                                        errors.append(error)
                                        computeTypeInstanceErr=True
                                
                                if(not computeTypeEmptyErr and not computeTypeInstanceErr and compute.get('maxQty') < compute.get('minQty')):
                                        error= ValidationError(ErrorCode.RESOURCE_QTY_ERROR)
                                        print(error)
                                        errors.append(error)
   
        if len(errors)>0:
            print(errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values 

class DeploymentStatusEnum(str,Enum):
    Created="Initiated"
    Updated="Updated"
    Deleted="Deleted"
    InProgress="InProgress"
    Deployed="Deployed"
    Failed="Failed"
    DeleteInProgress="DeleteInProgress"

class DeploymentResponseData(Deployment):
    id: str = None
    status:DeploymentStatusEnum =None
    devOpsJobId: str = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class DeploymentResponse(ApiResponse):
    data: Optional[DeploymentResponseData]=None

class InferenceDetails(AuditableColumns):
    name:str =None
    endpointId: str = None
    payload:str =None
    inputType:Optional[str] = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props 

    @root_validator(pre=True)
    def validateInferenceDetails(cls,values):
        errors=[]
        endpointId=values.get("endpointId")
        if (endpointId is None or (endpointId is not None and len(endpointId) == 0)):
            error= ValidationError(ErrorCode.ENDPOINT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        name=values.get("name")
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 
        
        payload=values.get("payload")
        if (payload is None or (payload is not None and len(payload) == 0)):
            error= ValidationError(ErrorCode.PAYLOAD_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 
        
        if len(errors)>0:
            print(errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values 

class InferenceResponseData(BaseModel):
    inferenceResponse: str =None

class InferenceResponse(ApiResponse):
    data: Optional[InferenceResponseData]=None

class ModelEndpointConfig(BaseModel):
    endpointUri: List[str]= None
    deploymentId: str = None
    modelId: str = None
    version: Optional[int] = None
    
class Endpoint(AuditableColumns):
    name: str =None
    contextUri: str= None
    projectId: str = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props 

    @root_validator(pre=True)
    def validateEndPoint(cls,values):
        errors=[]
       
        name=values.get("name")
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error)

        if (not re.fullmatch(endpoint_name_regex,name)):
            error= ValidationError(ErrorCode.ENDPOINT_NAME_SPECIAL_CHAR_ERROR)
            errors.append(error)  
        
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 

        contextUri=values.get("contextUri")
        if (contextUri is None or (contextUri is not None and len(contextUri)==0)):
            error= ValidationError(ErrorCode.MODEL_ENDPOINT_BASEURI_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        if len(errors)>0:
            print(errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values 

class EndpointStatuseEnum(str,Enum):
    Created="Created"
    Deleted="Deleted"
    Deployed="Deployed"
    DeleteInProgress="DeleteInProgress"

class EndpointResponseData(Endpoint):
    id: str = None
    status: EndpointStatuseEnum = None
    deployedModels:List[ModelEndpointConfig]=None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class EndpointResponse(ApiResponse):
    data:Optional[EndpointResponseData]= None

class ModelMetaDataResponseData(ModelMetaData):
    id: str = None
    status: ModelMetaDataStatusEnum = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class ModelMetaDataResponse(ApiResponse):
    data:Optional[ModelMetaDataResponseData]= None

class GetModelResponseData(BaseModel):
     model: Optional[ModelResponseData] = None

class GetModelResponse(ApiResponse):
    data: Optional[GetModelResponseData] = None

class ListModelResponseData(BaseModel):
     models: Optional[List[ModelResponseData]] = None

class ListModelResponse(ApiResponse):
    data: Optional[ListModelResponseData] = None

def ResponseModel(data):
    api_response=ApiResponse(code=200, status="SUCCESS",
                data=data)
    return api_response  