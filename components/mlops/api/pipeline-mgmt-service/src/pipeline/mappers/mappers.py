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

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Header Input Model
class HeaderInputModel(BaseModel):
    conversationID: Optional[str] = None  # Unique id of the request
    requestId: str = None  # id of the request
    requestTimestamp: str = None  # requestTimestamp
    senderURI: str = None  # The name of the system / application sending the message
    originatorURI: str = None  # The originator of the Business Process
    userId: str = None  # Id of the user
    security: Optional[str] = None  # Credential information used to secure message processing
    securityType: Optional[str] = None  # Identifies the type of credential in the security element

class HeaderInputModelCreateTrial(BaseModel):
    conversationID: Optional[str] = None  # Unique id of the request
    requestId: str = None  # id of the request
    requestTimestamp: str = None  # requestTimestamp
    senderURI: str = None  # The name of the system / application sending the message
    originatorURI: str = None  # The originator of the Business Process
    userId: str = None  # Id of the user
    security: Optional[str] = None  # Credential information used to secure message processing
    securityType: Optional[str] = None  # Identifies the type of credential in the security element
    runtimeEnvironment: Optional[str] = None

class PythonLangSchema(BaseModel):
    version: str = None
    dependencyFilePath: str = None

class DockerContainerSchema(BaseModel):
    baseDockerfile: Optional[str] = None
    baseImage: str = None
    shmSize: Optional[str] = None
    runCmd: str = None

class EnviornmentVarSchema(BaseModel):
    name: str = None
    value: str = None

class OsDependancySchema(BaseModel):
    name: str = None
    version: str = None

class EnvironmentSchema(BaseModel):
    python: PythonLangSchema
    docker: DockerContainerSchema

class StepResourceConfigSchema(BaseModel):
    computeType: str = None
    cpu: int = None
    memory: str = None
    gpuMemory: str = None
    gpuQty: str = None

class JobArgumentSchema(BaseModel):
    name: str = None
    defaultValue: Optional[str] = None
    dataType: str = None
    inputMode: str = None

class StepArgumentSchema(BaseModel):
    jobArgumentName: str = None

class MetricDetailSchema(BaseModel):
    name: str = None
    regex: str = None
    logFilePath: str = None

class StepSchema(BaseModel):
    sourceStorageType: str = None
    sourceDirectory: str = None
    mainScriptFile: str = None
    stepResourceConfig: StepResourceConfigSchema

class PreTrainedModelSchema(BaseModel):
    name: str = None
    version: str = None
    storageType: str = None
    storagePath: str = None

class FrameworkSchema(BaseModel):
    name: str = None
    version: str = None

class TrainingStepSchema(BaseModel):
    name: str = None
    artificatStorageType: str = None
    inputArtifacts: str = None
    stepDetails: StepSchema
    stepArguments: List[StepArgumentSchema]
    environment: EnvironmentSchema
    framework: FrameworkSchema
    preTrainedModelPath: Optional[PreTrainedModelSchema]
    outputArtifacts: str = None
    metricDetails: MetricDetailSchema

class StepCollectionSchema(BaseModel):
    trainingStep: TrainingStepSchema

class CreateUpdateSchema(BaseModel):
    createdOn: str = datetime
    createdBy: str = None
    modifiedOn: str = datetime
    updatedBy: str = None

class PipelineJobSchema(BaseModel):
    projectId: str = None  # Project Object Id
    version: str = None
    name: str = None
    description: str = None
    scope: str = None
    jobArguments: List[JobArgumentSchema] = None
    steps: List[StepCollectionSchema]

class RequestSchema(BaseModel):
    header: HeaderInputModel
    body: PipelineJobSchema

class RunConfigSchema(BaseModel):
    computeType: str = None
    cpu: str = None
    memory: str = None
    gpuMemory: str = None
    gpuQty: str = None

class RunArgumentSchema(BaseModel):
    name: str = None
    argValue: str = None

class MetricOutputSchema(BaseModel):
    runId: str = None
    name: str = None
    value: str = None

class ExperimentConfigSchema(BaseModel):
    name: str = None
    trackingType: str = None  # Accept only 2 value Auto/Manual

class PipelineTrialSchema(BaseModel):
    projectId: str = None
    pipelineId: str = None
    status: Optional[str] = None
    version: str = None
    name: str = None
    description: str = None
    modelName: str = None
    modelVersion: str = None
    runArguments: List[RunArgumentSchema] = None
    resourceConfig: RunConfigSchema = None
    experimentConfig: Optional[ExperimentConfigSchema]
    metricOutput: Optional[MetricOutputSchema]
    jobId: Optional[str] = None
    kubeflowRunID: Optional[str] = None

class StatusSchema(BaseModel):
    runId: str = None
    status: str = None

def ResponseModel(data):
    return {"code": 200, "status": "SUCCESS", "data": data}

def ErrorResponseModel(code, message):
    return {"code": code, "status": "FAILURE", "message": message}