# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import logging
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, status, Header, Response, Query, Path
from typing import Union, List, Any
from aicloudlibs.schemas.model_mappers import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.schemas.global_schema import *
from mms.service.endpoint_service import *

router = APIRouter()

#To create endpoint within the project.
@router.post(
    '/endpoint',
    response_model=EndpointResponse,
)
def createEndpoint ( request: Request, response: Response, 
    user_id: str = Header(..., alias='userId'), body: Endpoint = ...
) -> Union[
    EndpointResponse, ApiErrorResponseModel, ForbiddenException, NotFoundException, InternalServerError
]:
    """
    Create Endpoint
    """
    try:
        logP: dict = {'apiName': '/api/v1/endpoint'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)

        customlog.debug('START createEndpoint==%s',user_id)
        endpointService = EndpointService(request.app, customlog, user_id)
        endpointRespD:EndpointResponseData = endpointService.createEndpoint(body)
        endpointResp = EndpointResponse(data=endpointRespD)
        customlog.debug('END createEndpoint')
        return endpointResp
    
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    
#To get the endpoint details based on the endpoint id.
@router.get(
    '/endpoint/{endpoint_id}',
    response_model=EndpointResponse,
)
def getEndpoint( request: Request, response: Response,
    endpoint_id: str = Path(..., alias='endpoint_id'),
    user_id: str = Header(..., alias='userId'),
) -> Union[EndpointResponse, NotFoundException, InternalServerError,ApiErrorResponseModel]:
    print("endpointId : ",endpoint_id, user_id)

    try:
        logP: dict = {'apiName': '/api/v1/endpoint'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START getEndpoint==%s',user_id)
        endpointService = EndpointService(request.app, customlog, user_id)
        endpointData = endpointService.getEndpoint(endpoint_id)
        endpointResp = EndpointResponse(data=endpointData)
        return endpointResp

    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)


#To create model deployment using provided modelId, model version and endpointId.
@router.post(
    '/endpoint/deploy',
    response_model=DeploymentResponse,
)
async def createModelDeployment( request: Request, response: Response, 
    user_id: str = Header(..., alias='userId'), body: Deployment = ...
) -> Union[
    DeploymentResponse,
    ApiErrorResponseModel,
    ForbiddenException,
    NotFoundException,
    InternalServerError,
]:
    """
    Create Model Deployment
    """
    try:
        logP: dict = {'apiName': DEPLOY_MODEL_URL}
        customlog = logging.LoggerAdapter(request.app.logger, logP)

        customlog.debug('START createModelDeployment')
        
        deployService = EndpointService(request.app, customlog, user_id)
        deployData = deployService.createModelDeployment(body)
        
        apiResp = DeploymentResponse(code=status.HTTP_200_OK, status=HTTP_RESPONSE_STATUS_SUCCESS,
                data=deployData)
        
        customlog.debug('END createModelDeployment')
        return apiResp
    
    except MLOpsException as mle:
        raise HTTPException(**mle.__dict__)



#To get the deployment status based on the deployment id.
@router.get(
    '/endpoint/deploy/{deployment_id}',
    response_model=ApiResponse,
)
def getDeploymentStatus( request: Request, response: Response, 
    deployment_id: str = Path(..., alias='deployment_id'),
    user_id: str = Header(..., alias='userId'),
) -> Union[DeploymentResponse, NotFoundException, InternalServerError]:
    try:
        logP: dict = {'apiName': DEPLOY_MODEL_URL}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START getDeploymentStatus')
        deployService = EndpointService(request.app, customlog, user_id)
        deployStatus = deployService.getDeploymentStatus(deployment_id,user_id)
        apiResp = ApiResponse(code=status.HTTP_200_OK, status=HTTP_RESPONSE_STATUS_SUCCESS,
                data={'deployment':deployStatus})
        customlog.debug('END createModelDeployment')
        return apiResp
    
    except MLOpsException as mle:
        raise HTTPException(**mle.__dict__)
    except ModelAPIJenkinsExceptinon as mje:
        raise HTTPException(**mje.__dict__)
    
#To get the list of endpoints based on the project id.
@router.get(
        '/endpoint',
        response_model= ApiResponse,
        status_code=status.HTTP_200_OK)

def listEndpoint(request: Request, response: Response,project_id: str = Query(..., alias='projectId'),user_id: str = Header(..., alias='userId')):
    try:
        logP: dict = {'apiName': '/api/v1/endpoint'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START ListEndpoint')
        endpointService = EndpointService(request.app, customlog, user_id)
        endpointList = endpointService.getAllEndpoint(project_id)
        apiResp = ApiResponse(code=status.HTTP_200_OK, status=HTTP_RESPONSE_STATUS_SUCCESS,data={'endpoints':endpointList})
        response.status_code =status.HTTP_200_OK
        print(apiResp)
        return apiResp
    
    except ModelException as modelException:
        logP.error(modelException.__dict__)
        raise HTTPException(**modelException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)    


#To delete the deployment based on the deployment id. 
@router.delete(
    '/endpoint/deploy/{deployment_id}',
    response_model=ApiResponse
)
def deleteDeployment(request: Request, response: Response,
    deployment_id: str = Path(..., alias='deployment_id'),
    user_id: str = Header(..., alias='userId'),
) -> Union[EndpointResponse, NotFoundException, InternalServerError]:
    try:
        logP: dict = {'apiName': '/api/v1/endpoint/deletedeployment'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        endpointService = EndpointService(request.app, customlog, user_id)
        delete = "deployment"
        endpointData = endpointService.deleteDeployment(deployment_id,delete)
        apiResp = ApiResponse(code=status.HTTP_200_OK, status=HTTP_RESPONSE_STATUS_SUCCESS,data=endpointData)
        return apiResp

    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)


#To delete the endpoint based on the endpoint id and its associated deployments.
@router.delete(
    '/endpoint/{endpointId}',
    response_model=ApiResponse
)
def deleteEndpoint(request: Request, response: Response,
    endpointId: str = Path(..., alias='endpointId'),
    userId: str = Header(..., alias='userId'),
) -> Union[ApiResponse, NotFoundException, InternalServerError]:
    try:
        logP: dict = {'apiName': '/api/v1/endpoint'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        endpointService = EndpointService(request.app, customlog, userId)
        endpointData = endpointService.deleteEndpoint(endpointId)
        apiResp = ApiResponse(code=status.HTTP_200_OK, status=HTTP_RESPONSE_STATUS_SUCCESS,data=endpointData)
        return apiResp

    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
