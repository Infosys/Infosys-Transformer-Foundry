# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: idp_job_response.py
description: A Pydantic model object for Deployment entity model
             which maps the data model to the Deployment entity schema
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional,List

class KnativeJobResponse(BaseModel):
    jobId: Optional[str]
    jobStatus: str
    modelEndpoint:str
    errorMsg: Optional[str]

class TritonJobResponse(BaseModel):
    jobId: Optional[str]
    jobStatus: str
    modelEndpoint:str
    errorMsg: Optional[str]

class IdpJobDetailsModelUpdate(BaseModel):
    id: Optional[str]
    status: str
    responseJson: KnativeJobResponse

class IdpJobDetailsModel(BaseModel):
    _id: Optional[str]
    jobName: Optional[str]
    status: str
    requestJson: Optional[dict]
    responseJson:Optional[dict]
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None
    createdOn: Optional[datetime] = None 
    modifiedOn: Optional[datetime] = None 
    isDeleted: bool = False

class PipelineJobResponse(BaseModel):
    jobId: Optional[str]
    jobStatus: str
    runId:str
    errorMsg: Optional[str]

class DeleteDeploymentJobResponse(BaseModel):
    jobId: Optional[str]
    jobStatus: str
    message:str
    errorMsg: Optional[str]

class DeleteEndpointJobResponse(BaseModel):
    enpointId: Optional[str]
    jobId: Optional[str]
    jobStatus: str
    message:str
    errorMsg: Optional[str]
    
class ESBulkData(BaseModel):
    data: List[dict]
    esindex: str

class ResponseData(BaseModel):
    response: Optional[dict]
    responseCde: int
    responseMsg: str
    timestamp: str
    responseTimeInSecs: float