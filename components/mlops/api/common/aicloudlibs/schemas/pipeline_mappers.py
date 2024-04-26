# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: pipeline_mappers.py
description: A Pydantic model object for pipeline entity model 
             which maps the data model to the pipeline entity schema
"""

from pydantic import BaseModel,Field,root_validator
from bson import ObjectId
from datetime import datetime
from typing import Optional, List,Union

from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ContainerSpec,PyObjectId,ApiResponse,ValidationError
from enum import Enum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper
import regex as re

arg_name_regex =  r'[a-zA-Z0-9_]+$'
name_regex =  r'[a-z0-9-]+$'

class MLFlow(BaseModel):
    name: Optional[str] =None

class Framework(BaseModel):
    name: str = None
    version: str = None

# class TrainingContainerSpec(BaseModel):
#     imageURI:str
#     envVariables: Optional[NameValuePair]=None
#     ports: Optional[NameValuePair]=None
#     labels: Optional[NameValuePair]=None
#     scriptRunCommand: List[str] = None
    

class JobArgument(BaseModel):
    name: str =None
    defaultVal: Optional[str] = None 
    dataType: str =None
    #storageType: str = None

class MetricDetails(BaseModel):
    goal: str = None
    name: str = None
    regex: str = None
    logFileUri: str = None

class MetricOutput(BaseModel):
    name: str = None
    value: str = None 

class PreTrainedModel(BaseModel):
    name: str = None
    version: str = None
    artifacts: Artifacts

class StepArguments(BaseModel):
    jobArgNames:List[str] = None

class TrainingStep(BaseModel):
    name: str=None
    inputArtifacts: Optional[Artifacts]=None
    stepArguments:StepArguments=None
    container: ContainerSpec=None
    framework: Framework=None
    preTrainedModelDetails:Optional[PreTrainedModel]=None
    outputArtifactBaseUri:Optional[str]=None
    metricDetails:Optional[MetricDetails]=None


class StepCollections(BaseModel):
    trainingStep: TrainingStep


class PipelineJobDetails(AuditableColumns):
    projectId: str = None  # Project Object Id
    version: int = None
    name: str = None
    description: str = None
    scope: Optional[str] = Field(hidden=True,default="private")
    jobArguments: List[JobArgument]=None
    steps: List[StepCollections]
    
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
                
            schema["properties"] = props

    @root_validator(pre=True)
    def validatePipelineJob(cls,values):
        errors=[]
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 

        version=values.get("version")
        if (version is None ):
            error= ValidationError(ErrorCode.VERSION_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        name=values.get("name")
        piplnnameEmptyErr=False
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
            piplnnameEmptyErr=True
            errors.append(error) 
        
        
        
        if (not re.fullmatch(name_regex,name)):
            print("inside alphacheck")
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 
        
        if(not piplnnameEmptyErr and len(name)>int(NAME_MAX_LENGTH)):
            error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
            errors.append(error)


        jobArguments=values.get("jobArguments")
        if (jobArguments is None or (jobArguments is not None and len(jobArguments) == 0)):
            error= ValidationError(ErrorCode.PIPELINE_JOBARGLIST_EMPTY_ERROR)
            print(error)
            errors.append(error)

        if (jobArguments is not None and len(jobArguments)>0):
            for arg in jobArguments:
                nameEmptyErr=False
                dataTypeEmptyErr=False
                dataTypeValueErr=False
                maxLengthErr=False
                specialcharcheck=False
                storageTypeErr=False
                print(arg['name'].isalnum())
                print(arg['name'].__contains__("_"))
                print(not (arg['name'].isalnum() or arg['name'].__contains__("_")))
                if (arg['name'] is None or (arg['name'] is not None and len(arg['name']) ==0)) :
                      nameEmptyErr=True
                if(arg['dataType'] is None or (arg['dataType'] is not None and len(arg['dataType'])==0)):
                      dataTypeEmptyErr=True
                if(not dataTypeEmptyErr and arg['dataType'] not in VALIDDATATYPEVALUE):
                      dataTypeValueErr=True
                if(not re.fullmatch(arg_name_regex,arg['name'])):
                       print("inisde name special check ")
                       specialcharcheck=True
                if(not nameEmptyErr and len(arg['name'])>int(NAME_MAX_LENGTH)):
                       maxLengthErr=True
                # if( arg['storageType'] is not None and len(arg['storageType'])>0 and ( not hasattr(StorageTypeEnum,arg['storageType']))):
                #         storageTypeErr=True
                #or storageTypeErr
                if nameEmptyErr or  dataTypeEmptyErr or dataTypeValueErr or specialcharcheck :
                       break
                
            if nameEmptyErr:
                error=ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
                errors.append(error)
            if dataTypeEmptyErr:
                error=ValidationError(ErrorCode.DATATYPE_NOT_EMPTY_ERROR)
                errors.append(error)
            if dataTypeValueErr:
                error=ValidationError(ErrorCode.DATATYPE_VALUE_ERROR)
                errors.append(error)
            if maxLengthErr:
                 error=ValidationError(ErrorCode.JOB_ARGNAME_MAX_LENGTH_ERROR)
                 errors.append(error)
            if specialcharcheck:
                  error=ValidationError(ErrorCode.JOB_ARGNAME_SPECIAL_CHARS_ERROR)
                  errors.append(error)
            # if storageTypeErr:
            #       error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
            #       errors.append(error)
        
        steps=values.get("steps")
        stepsError=False
        if (steps is None or (steps is not None and len(steps) == 0)):
            error= ValidationError(ErrorCode.STEPS_LIST_EMPTY_ERROR)
            stepsError=True
            print(error)
            errors.append(error)
        
        if not stepsError:
            for step in steps:
                  if(step['trainingStep'] is not None and len(step['trainingStep'])>0):
                        trainingStep= step['trainingStep']
                        print(trainingStep)
                        containerEmptyerr=False
                        if(trainingStep['name'] is None or (trainingStep['name'] is not None and len(trainingStep['name'])==0) ):
                            error=ValidationError(ErrorCode.TRAININGSTEP_NAME_NOT_EMPTY_ERROR)
                            errors.append(error)
                        if(trainingStep['inputArtifacts'] is not None and len(trainingStep['inputArtifacts'])>0):
                            inputArtifacts=trainingStep['inputArtifacts']
                            inputArtifactError=False
                            inputArtifactUriError=False
                            
                            if (inputArtifacts.get('storageType') is None or (inputArtifacts.get('storageType') is not None and len(inputArtifacts.get('storageType'))==0)):
                                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                    errors.append(error)
                                    inputArtifactError=True
                            if(not inputArtifactError and ( not hasattr(StorageTypeEnum,inputArtifacts.get('storageType')))):
                                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                    errors.append(error)

                            if(not inputArtifactError and (inputArtifacts.get('uri') is None or (inputArtifacts.get('uri') is not None and len(inputArtifacts.get('uri'))==0))):
                                    error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                                    errors.append(error)
                                    inputArtifactUriError=True
                            if(not inputArtifactUriError and (not inputArtifacts.get('uri').startswith("s3://"))):
                                    error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                                    errors.append(error)

                        if(trainingStep['stepArguments'] is None or (trainingStep['stepArguments'] is not None and trainingStep['stepArguments']['jobArgNames'] is not None and len(trainingStep['stepArguments']['jobArgNames'])==0)):
                                    
                                    error=ValidationError(ErrorCode.STEPS_ARG_LIST_NOT_EMPTY_ERROR)
                                    errors.append(error)
                        
                        if(trainingStep['container']is None or(trainingStep['container']is not None and len(trainingStep['container'])==0) ):
                                    
                                    error=ValidationError(ErrorCode.CONTAINER_SPEC_NOT_EMPTY)
                                    errors.append(error)
                                    containerEmptyerr=True
                            
                        if(not containerEmptyerr ):
                                  
                                  containerDet=trainingStep['container']
                                  
                                  contImageUriEmptyErr=False
                                  if(containerDet.get('imageUri') is None or(containerDet.get('imageUri') is not None and len(containerDet.get('imageUri'))==0)):
                                     error=ValidationError(ErrorCode.CONTAINER_IMAGE_URI_EMPTY)
                                     errors.append(error)
                                     contImageUriEmptyErr=True
                                  if(not contImageUriEmptyErr and not containerDet.get('imageUri').startswith(INFYARTIFACTORYURI)):
                                     error=ValidationError(ErrorCode.CONTAINER_IMAGE_URI_VALUE_ERROR)
                                     errors.append(error)
                                  if(not containerDet.get('command') and containerDet.get('command') is None or (containerDet.get('command')  is not None and len(containerDet.get('command'))==0) ):
                                     error=ValidationError(ErrorCode.CONTAINER_COMMAND_LIST_EMPTY)
                                     errors.append(error)

                        frameworkEmptyErr=False
                        if(trainingStep['framework'] is None or (trainingStep['framework'] is not None and len(trainingStep['framework'])==0)):
                                    error=ValidationError(ErrorCode.FRAMEWORK_NOT_EMPTY)
                                    errors.append(error)
                                    frameworkEmptyErr=True
                        if(not frameworkEmptyErr and (trainingStep['framework']['name'] is None or (trainingStep['framework']['name'] is not None and len(trainingStep['framework']['name'])==0))):
                                    error=ValidationError(ErrorCode.FRAMEWORK_NAME_EMPTY)
                                    errors.append(error)
                        if(not frameworkEmptyErr and (trainingStep['framework']['version'] is None or (trainingStep['framework']['version'] is not None and len(trainingStep['framework']['version'])==0))):
                                    error=ValidationError(ErrorCode.FRAMEWORK_VERSION_EMPTY)
                                    errors.append(error)
                        if((trainingStep['preTrainedModelDetails'] is not None and len(trainingStep['preTrainedModelDetails'])>0)):
                                     preTrainedModelDet=trainingStep['preTrainedModelDetails']
                                     artifactsemptyError=False
                                     if(preTrainedModelDet.get('name') is None or(preTrainedModelDet.get('name') is not None and len(preTrainedModelDet.get('name'))==0)):
                                          error=ValidationError(ErrorCode.PRETRAINED_MODEL_NAME_EMPTY_ERROR)
                                          errors.append(error)
                                     if(preTrainedModelDet.get('version') is None or(preTrainedModelDet.get('version') is not None and len(preTrainedModelDet.get('version'))==0)):
                                          error=ValidationError(ErrorCode.PRETRAINED_MODEL_VERSION_EMPTY)
                                          errors.append(error)

                                     if(preTrainedModelDet.get('artifacts') is None or(preTrainedModelDet.get('artifacts') is not None and len(preTrainedModelDet.get('artifacts'))==0)):
                                          error=ValidationError(ErrorCode.PRETRAINED_ARTIFACTS_EMPTY_ERROR)
                                          errors.append(error)
                                          artifactsemptyError=True

                                     if not artifactsemptyError:
                                            pretraind_artifacts=preTrainedModelDet['artifacts']
                                            pretraind_artifactsErr=False
                                            pretrainedArtifactUriError=False
                                            if (pretraind_artifacts.get('storageType') is None or (pretraind_artifacts.get('storageType') is not None and len(pretraind_artifacts.get('storageType'))==0)):
                                                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                                    errors.append(error)
                                                    pretraind_artifactsErr=True
                                            if(not pretraind_artifactsErr and ( not hasattr(StorageTypeEnum,pretraind_artifacts.get('storageType')))):
                                                    error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                                    errors.append(error)
                                            
                                            if(not pretraind_artifactsErr and (pretraind_artifacts.get('uri') is None or (pretraind_artifacts.get('uri') is not None and len(pretraind_artifacts.get('uri'))==0))):
                                                    error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                                                    errors.append(error)
                                                    pretrainedArtifactUriError=True

                                            if(not pretrainedArtifactUriError and (not pretraind_artifacts.get('uri').startswith("s3://"))):
                                                    error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                                                    errors.append(error)
                        if (hasattr(trainingStep,'metricDetails') and trainingStep['metricDetails'] is not None and len(trainingStep['metricDetails'])>0):
                                    metrcdet=trainingStep['metricDetails']
                                    if(metrcdet.get('goal') is None or (metrcdet.get('goal') is not None and len(metrcdet.get('goal'))==0 )):
                                         error=ValidationError(ErrorCode.METRICDETAILS_GOAL_ERROR)
                                         errors.append(error)
                                    if(metrcdet.get('name') is None or (metrcdet.get('name') is not None and len(metrcdet.get('name'))==0 )):
                                         error=ValidationError(ErrorCode.METRICDETAILS_NAME_EMPTY)
                                         errors.append(error)
                                    if(metrcdet.get('regex') is None or (metrcdet.get('regex') is not None and len(metrcdet.get('regex'))==0 )):
                                         error=ValidationError(ErrorCode.METRICDETAILS_REGEX_EMPTY)
                                         errors.append(error)
                                    if(metrcdet.get('logFileUri') is None or (metrcdet.get('logFileUri') is not None and len(metrcdet.get('logFileUri'))==0 )):
                                         error=ValidationError(ErrorCode.METRICDETAILS_LOG_FILE_URI_EMPTY)
                                         errors.append(error)
                        

                                    
                                    
                                     
        #print(errors)
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
        


    
    

class RunArguments(BaseModel):
    name: str = None
    argValue: str =None

class PipelineTrial(AuditableColumns):
    projectId:str=None
    pipelineId:str=None
    #version:str=None
    name:str=None
    jobId: str=Field(None,hidden=True)
    kubeflowRunId: str=Field(None,hidden=True)
    description:Optional[str]=None
    modelName:str=None
    modelVersion:str=None
    runArguments: List[RunArguments] =None
    resourceConfig: ResourceConfig =None
    experimentConfig: Optional[MLFlow] =None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props
    
    @root_validator(pre=True)
    def validatePipelineTrial(cls,values):
        errors=[]
        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error) 
        
        pipelineId=values.get("pipelineId")
        if (pipelineId is None or (pipelineId is not None and len(pipelineId) == 0)):
            error= ValidationError(ErrorCode.PIPELINE_ID_REQUIRED)
            print(error)
            errors.append(error) 

        modelName=values.get("modelName")
        modelnameEmptyErr=False
        if (modelName is None or (modelName is not None and len(modelName) == 0)):
            error= ValidationError(ErrorCode.MODEL_NAME_NOT_EMPTY_ERROR)
            modelnameEmptyErr=True
            errors.append(error) 
        
        if not modelnameEmptyErr and not re.fullmatch(name_regex,modelName):
            error= ValidationError(ErrorCode.MODEL_NAME_SPECIAL_CHARS_ERROR)
            errors.append(error) 
        
        if(not modelnameEmptyErr and len(modelName)>int(NAME_MAX_LENGTH)):
            error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
            errors.append(error)
        
        modelVersion=values.get("modelVersion")
        if (modelVersion is None or (modelVersion is not None and len(modelVersion) == 0)):
            error= ValidationError(ErrorCode.MODEL_VERSION_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        name=values.get("name")
        runnameEmptyErr=False
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.TRIAL_NAME_NOT_EMPTY_ERROR)
            runnameEmptyErr=True
            errors.append(error) 

        
        if not runnameEmptyErr and not re.fullmatch(name_regex,name):
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 
        
        if(not runnameEmptyErr and len(name)>int(NAME_MAX_LENGTH)):
            error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
            errors.append(error)

        runArguments=values.get("runArguments")
        runArgEmptyErr=False
        if (runArguments is None or (runArguments is not None and len(runArguments) == 0)):
            error= ValidationError(ErrorCode.TRIAL_RUNARGLIST_EMPTY_ERROR)
            print(error)
            errors.append(error)
            runArgEmptyErr=True
        if not runArgEmptyErr:
            
            for runArg in runArguments:
                runArgNameEmptyErr=False
                
                if (runArg.get("name") is None or (runArg.get("name") is not None and len(runArg.get("name"))==0)):
                    error= ValidationError(ErrorCode.RUN_ARG_NAME_EMPTY_ERROR)
                    errors.append(error)
                    runArgNameEmptyErr=True
                    
                
                if (runArg.get("argValue") is None or (runArg.get("argValue") is not None and len(runArg.get("argValue"))==0)):
                    error= ValidationError(ErrorCode.RUN_ARG_VALUE_EMPTY_ERROR)
                    errors.append(error)
                    
                
        
        resourceConfig=values.get("resourceConfig")
        
        resourceConfigEmptyErr=False
        if (resourceConfig is None or (resourceConfig is not None and len(resourceConfig) == 0)):
            error= ValidationError(ErrorCode.RESOURCECONFIG_EMPTY_ERROR)
            print(error)
            errors.append(error)
            resourceConfigEmptyErr=True
        if not resourceConfigEmptyErr:
             computeEmptyErr=False
             
             
             if(resourceConfig.get('volumeSizeinGB') is None ):
                  error= ValidationError(ErrorCode.VOLUME_EMPTY_ERROR)
                  print(error)
                  errors.append(error)
             
             print(resourceConfig)
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
                       
                       if(not computeTypeEmptyErr and not gpumemryEmptyErr and compute.get('type').lower() =='gpu' and  compute.get('memory').lower() not in PIPELINE_GPU_MEMORY_VALUES):
                             error= ValidationError(ErrorCode.PIPELINE_GPU_MEMORY_VALUE_ERROR)
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
        
       
    

class TrialStatusEnum(str,Enum):
    Initiated="Initiated"
    InProgress="InProgress"
    Succeeded="Succeeded"
    Failed="Failed"
    Error="Error"



class PipelineJobStatusEnum(str,Enum):
    Created="Created"
    Updated="Updated"
    Deleted="Deleted"

class PipelineResponseData(PipelineJobDetails):
    id: str = None
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status:PipelineJobStatusEnum=Field(default=PipelineJobStatusEnum.Created)
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

class ListPipelineResponseData(BaseModel):
     pipelines: Optional[List[PipelineResponseData]] = None

class ListPipelineResponse(ApiResponse):
    data: Optional[ListPipelineResponseData] = None

class GetPipelineResponseData(BaseModel):
     pipeline: Optional[PipelineResponseData] = None

class GetPipelineResponse(ApiResponse):
    data: Optional[GetPipelineResponseData] = None

class DeletePipelineResponse(ApiResponse):
     data: Optional[str]=None
    
class TrialResponseData(PipelineTrial):
    id: str = None
    status:TrialStatusEnum=Field(default=TrialStatusEnum.Initiated)
    metricOutput: Optional[MetricOutput]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props


class TrialResponse(ApiResponse):
    data: Optional[TrialResponseData] = None

class GetTrialResponseData(BaseModel):
     trial: Optional[TrialResponseData] = None

class GetTrialResponse(ApiResponse):
    data: Optional[GetTrialResponseData] = None

def ResponseModel(data):
    api_response=ApiResponse(code=200, status="SUCCESS",
                data=data)
    return api_response    