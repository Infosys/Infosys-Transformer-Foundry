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

from pydantic import BaseModel,Field,root_validator,Extra
from bson import ObjectId
from datetime import datetime
from typing import Optional, List,Union,Any, Dict,  Sequence

from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ContainerSpec,PyObjectId,ApiResponse,ValidationError,OperatorEnum,\
    RuntimeEnum,ResourceConfigV2,VolumeScopeEnum
from enum import Enum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper
import regex as re
from aicloudlibs.constants.util_constants import *

arg_name_regex =  r'[a-zA-Z0-9_]+$'
name_regex =  r'[a-z0-9-]+$'
num_regex = r'[0-9]+$'

class Storage(BaseModel):
    class Config:
        extra = Extra.forbid
    storageType: str
    name: str
    uri: str

class VolumeDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    scope : str
    name : str
    mountPath : str
    sizeinGB : Optional[int]

class KeyValuePair(BaseModel):
    __root__: Dict[str, str]

class StepConfig(BaseModel):
    class Config:
        extra = Extra.forbid
    entryPoint: List[str]
    stepArguments: Optional[List[str]]
    imageUri: str

class StepDetails(BaseModel):
    class Config:
        extra = Extra.forbid
    type: str
    dependsOn: List[str]
    inputArtifacts : Optional[Storage]
    input: KeyValuePair
    output: KeyValuePair
    stepConfig: StepConfig
    resourceConfig: ResourceConfigV2

class Step(BaseModel):
    __root__: Dict[str, StepDetails]

class MultiStepPipeline(BaseModel):
    class Config:
        extra = Extra.forbid
    name: str
    version: int
    operator: str
    runtime: str
    dataStorage: List[Storage]
    volume : Optional[VolumeDetails]
    flow: Step
    variables: KeyValuePair
    globalVariables: KeyValuePair

class Pipeline(BaseModel):
 
    projectId: str
    description: str
    pipeline: MultiStepPipeline

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
                
            schema["properties"] = props

    @root_validator(pre=True)
    def validatePipeline(cls, values):
        errors = []

        projectId=values.get("projectId")
        if (projectId is None or (projectId is not None and len(projectId) == 0)):
            error= ValidationError(ErrorCode.PROJECT_ID_REQUIRED)
            print(error)
            errors.append(error)
        
        pipelineData=values.get("pipeline")
        pipeineDataError=False
        if (pipelineData is None or (pipelineData is not None and len(pipelineData) == 0)):
            error= ValidationError(ErrorCode.PIPLINE_DATA_NOT_EMPTY_ERROR)
            pipeineDataError=True
            print(error)
            errors.append(error)
            

        if not pipeineDataError:
            version=pipelineData.get("version")
            if (version is None ):
                error= ValidationError(ErrorCode.VERSION_NOT_EMPTY_ERROR)
                print(error)
                errors.append(error) 

            name=pipelineData.get("name")
            piplnnameEmptyErr=False
            if (name is None or (name is not None and len(name) == 0)):
                error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
                piplnnameEmptyErr=True
                errors.append(error) 
            
            if not piplnnameEmptyErr and (not re.fullmatch(name_regex,name)):
                print("inside alphacheck")
                error= ValidationError(ErrorCode.PIPLN_NAME_SPECIAL_CHARS_ERROR)
                errors.append(error) 
            
            if(not piplnnameEmptyErr and len(name)>int(NAME_MAX_LENGTH)):
                error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
                errors.append(error)

            operator=pipelineData.get("operator")
            operatorEmptyErr=False
            if operator is None or(operator is not None and len(operator)==0):
                error= ValidationError(ErrorCode.OPERATOR_NOT_EMPTY_ERROR)
                operatorEmptyErr=True
                errors.append(error)
                operatorEmptyErr=True
            
            if not operatorEmptyErr and (operator.lower() not in GPMS_OPERATOR_OPTIONS):
                  error=ValidationError(ErrorCode.OPERATOR_OPTIONS_ERROR)
                  errors.append(error)
            if not operatorEmptyErr and operator==OperatorEnum.AIRFLOW:
                    error = ValidationError(ErrorCode.AIRFLOW_ERROR)
                    errors.append(error)
               
            runtime=pipelineData.get("runtime")
            runtimeEmptyErr=False
            if runtime is None or (runtime is not None and len(runtime)==0):
                error= ValidationError(ErrorCode.RUNTIME_NOT_EMPTY_ERROR)
                runtimeEmptyErr=True
                errors.append(error)
                runtimeEmptyErr=True
            if not runtimeEmptyErr and (runtime.lower() not in GPMS_RUNTIME_OPTIONS):
                  error=ValidationError(ErrorCode.RUNTIME_OPTIONS_ERROR)
                  errors.append(error)
            if not runtimeEmptyErr and runtime==RuntimeEnum.VM:
                  error = ValidationError(ErrorCode.VM_ERROR)
                  errors.append(error)

            dataStorage=pipelineData.get("dataStorage")
            if dataStorage is not None and len(dataStorage) >0 :
                for storageitem in dataStorage:
                      storageitemError=False
                      storageitemUriError=False
                      if (storageitem.get('storageType') is None or (storageitem.get('storageType') is not None and len(storageitem.get('storageType'))==0)):
                            error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                            errors.append(error)
                            storageitemError=True
                      if(not storageitemError and (storageitem.get('storageType') not in GPMS_STORAGE_OPTIONS)):
                             error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                             errors.append(error)
                      if (storageitem.get('name') is None or (storageitem.get('name') is not None and len(storageitem.get('name'))==0)):
                             error=ValidationError(ErrorCode.DATASTORAGE_NAME)
                             print(error)
                             errors.append(error)

                      if(not storageitemError and (storageitem.get('uri') is None or (storageitem.get('uri') is not None and len(storageitem.get('uri'))==0))):
                              error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                              errors.append(error)
                              storageitemUriError=True
                      if(not storageitemUriError and (not storageitem.get('uri').startswith("s3://"))):
                               error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                               errors.append(error)
            if 'volume' in pipelineData:
                volnotEmptyErr=False
                if not bool(pipelineData.get('volume')):
                    volnotEmptyErr=True
                    error = ValidationError( ErrorCode.VOLUME_EMPTY_ERROR)
                    errors.append(error)
                if not volnotEmptyErr:
                    volumeData=pipelineData.get("volume")
                    scope=volumeData.get("scope")
                    scopeEmptyErr=False
                    if scope is None or (scope is not None and len(scope)==0):
                        error= ValidationError(ErrorCode.VOLUME_SCOPE_EMPTY_ERROR)
                        print(error)
                        scopeEmptyErr=True
                        errors.append(error) 
                    if not scopeEmptyErr and (scope.lower() not in GPMS_VOLUME_OPTIONS):
                        error=ValidationError(ErrorCode.VOLUME_SCOPE_OPTIONS_ERROR)
                        errors.append(error)
                    vaolname=volumeData.get("name")
                    vaolnameEmptyErr=False
                    if (vaolname is None or (vaolname is not None and len(vaolname) == 0)):
                        error= ValidationError(ErrorCode.NAME_NOT_EMPTY_ERROR)
                        vaolnameEmptyErr=True
                        errors.append(error) 
                    
                    if not vaolnameEmptyErr and (not re.fullmatch(name_regex,name)):
                        print("inside alphacheck")
                        error= ValidationError(ErrorCode.VOLUME_NAME_SPECIAL_CHARS_ERROR)
                        errors.append(error) 
                    
                    if(not vaolnameEmptyErr and len(vaolname)>int(NAME_MAX_LENGTH)):
                        error=ValidationError(ErrorCode.NAME_MAX_LENGTH_ERROR)
                        errors.append(error)
                    
                    mountPath=volumeData.get("mountPath")
                    if (mountPath is None or (mountPath is not None and len(mountPath) == 0)):
                        error= ValidationError(ErrorCode.MOUNTPATH_NOT_EMPTY_ERROR)
                        errors.append(error)
                    
                    sizeinGB=volumeData.get("sizeinGB")
                    if (not scopeEmptyErr and scope.lower()=="pipeline" and sizeinGB == 0):
                        error= ValidationError(ErrorCode.VOLUME_SIZE_EMPTY_ERROR)
                        errors.append(error)
                     
            stepData=pipelineData.get("flow")
            stepDataEmptyErr=False
            if (stepData is None or (stepData is not None and len(stepData) == 0)):
                error= ValidationError(ErrorCode.STEPS_LIST_EMPTY_ERROR)
                stepDataEmptyErr=True
                print(error)
                errors.append(error)
            if not stepDataEmptyErr:
                 step_name_list = list(stepData.keys())
                 umatched_steps = [
                 x for x in step_name_list if not re.match(name_regex, x)]
                 flowstepnameerr=False
                 for i in umatched_steps:
                        if len(i) == 0:
                            flowstepnameerr=True
                            error = ValidationError(
                                ErrorCode.FLOW_STEP_NAME_ERROR)
                            errors.append(error)
                            break
                        else:
                            if len(umatched_steps) > 0:
                                flowstepnameerr=True
                                error = ValidationError(ErrorCode.FLOW_STEP_NAME_VALUE_ERROR)
                                errors.append(error)
                                break
                                
                 if not flowstepnameerr:               
                    for stepdet in stepData:
                        currentStep=stepdet
                        currentStepData=stepData[currentStep]
                        step_type=currentStepData.get("type")
                        if step_type is None or (step_type is not None and len(step_type)==0):
                            error=ValidationError(ErrorCode.STEP_TYPE_NOT_EMPTY_ERROR)
                            errors.append(error)
                        dependsOn=currentStepData.get("dependsOn")
                        if step_type is not None and len(step_type)>0:
                            for dependsOnStep in dependsOn:
                                found=False
                                for stepName in step_name_list:
                                   if dependsOnStep == currentStep:
                                        break
                                   elif dependsOnStep == stepName:
                                         found=True
                                         break
                                if found:
                                    continue
                                else:
                                    error=ValidationError(ErrorCode.DEPENDS_ON)
                                    errors.append(error)
                                    break
                        
                        if 'inputArtifacts' in currentStepData:
                             inputArifactsnotEmptyErr=False
                             if not bool(currentStepData.get('inputArtifacts')):
                                    inputArifactsnotEmptyErr=True
                                    error = ValidationError( ErrorCode.PIPELINE_INPUTARTIFACTS)
                                    errors.append(error)
                             if not inputArifactsnotEmptyErr:
                                    inputArifacts=currentStepData.get('inputArtifacts')
                                    inpArtStorageURIError=False
                                    inpArtStorageError=False
                                    if (inputArifacts.get('storageType') is None or (inputArifacts.get('storageType') is not None and len(inputArifacts.get('storageType'))==0)):
                                            error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                            errors.append(error)
                                            inpArtStorageError=True
                                    if(not inpArtStorageError and (inputArifacts.get('storageType') not in GPMS_STORAGE_OPTIONS)):
                                            error=ValidationError(ErrorCode.STORAGE_TYPE_OPTIONS_ERROR)
                                            errors.append(error)

                                    if(not inpArtStorageError and (inputArifacts.get('uri') is None or (inputArifacts.get('uri') is not None and len(inputArifacts.get('uri'))==0))):
                                                error=ValidationError(ErrorCode.ARTIFACT_URI_EMPTY)
                                                errors.append(error)
                                                inpArtStorageURIError=True
                                    if(not inpArtStorageURIError and (not inputArifacts.get('uri').startswith("s3://"))):
                                                error=ValidationError(ErrorCode.ARTIFACTS_URI_VALUE_ERROR)
                                                errors.append(error)

                        stepConfigData=currentStepData.get("stepConfig")
                        stepConfigDataError=False
                        if stepConfigData is None or len(stepConfigData)==0:
                            error=ValidationError(ErrorCode.STEP_CONFIG_EMPTY_ERROR)
                            errors.append(error)
                            stepConfigDataError=True 
                        if not stepConfigDataError:
                             entrypointFieldErr=False
                             if "entryPoint" not in stepConfigData:
                                  entrypointFieldErr=True
                                  error = ValidationError( ErrorCode.ENTRYPOINT_ATTR_ERROR)
                                  errors.append(error)
                             if not entrypointFieldErr:
                                step_entrypoint=stepConfigData.get("entryPoint")
                                if not step_entrypoint and step_entrypoint is not None and len(step_entrypoint)==0:
                                     error = ValidationError( ErrorCode.ENTRYPOINT_EMPTY_LIST_ERROR)
                                     errors.append(error)
                                     
                             imageUriData = stepConfigData.get('imageUri')
                             contImageUriEmptyErr=False
                             if imageUriData is None or (imageUriData is not None and len(imageUriData)==0):
                                error = ValidationError(ErrorCode.CONTAINER_IMAGE_URI_EMPTY)
                                errors.append(error)
                                contImageUriEmptyErr=True
                             if(not contImageUriEmptyErr and not imageUriData.startswith(INFYARTIFACTORYURI)):
                                     error=ValidationError(ErrorCode.CONTAINER_IMAGE_URI_VALUE_ERROR)
                                     errors.append(error)
                        resourceConfig=currentStepData.get("resourceConfig")
        
                        resourceConfigEmptyErr=False
                        if (resourceConfig is None or (resourceConfig is not None and len(resourceConfig) == 0)):
                            error= ValidationError(ErrorCode.RESOURCECONFIG_EMPTY_ERROR)
                            print(error)
                            errors.append(error)
                            resourceConfigEmptyErr=True
                        if not resourceConfigEmptyErr:
                            computeEmptyErr=False
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
                                    
                                    if(not computeTypeEmptyErr and not gpumemryEmptyErr and compute.get('type').lower() =='gpu' and  compute.get('memory').lower() not in PIPELINE_GPU_MEMORY_VALUE_ERROR):
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
        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    exc=error,
                    loc=('body', 'root'),
                ),])
        else:
            return values
        
class ExceutionDetails(BaseModel):
    dataStorage: List[Storage]
    variables: KeyValuePair
    globalVariables: KeyValuePair

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
                
            schema["properties"] = props

class PipelineExecution(BaseModel):
    pipeline:ExceutionDetails

class UpdatePipeline(Pipeline):
     id: str