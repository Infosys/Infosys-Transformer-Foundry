# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import logging
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, status, Header, Response, Query, Path
from typing import Union, List, Any
from mms.service.model_service import *
from mms.service.endpoint_service import *
from aicloudlibs.schemas.global_schema import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.schemas.model_mappers import *
import aicloudlibs.constants.http_status_codes as code
import aicloudlibs.constants.error_constants as status
from mms.exception.exception import *

router = APIRouter()

#To get the list of model associated with the given project as an list.
@router.get('/models',response_model= ApiResponse,status_code=code.HTTP_STATUS_OK)
def listModels(request: Request, response: Response,project_id: str = Query(..., alias='projectId'),user_id: str = Header(..., alias='userId')):

    try:
        logP: dict = {'apiName': '/api/v1/models'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START list_models')
        modelService = ModelService(request.app, customlog, user_id)
        modelList = modelService.getAllModels(project_id)
        apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data={'models':modelList})
        response.status_code = code.HTTP_STATUS_OK
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

#To register a model with its metadata and other details like container image, port details.
@router.post(
    '/models',
    response_model=ModelResponse,
    responses={
        '400': {'model': ApiErrorResponseModel},
        '500': {'model': InternalServerError},
    }
)
def registerModel( request: Request, response: Response, 
    user_id: str = Header(..., alias='userId'), body: ModelDetails = ...
) -> Union[
    ModelResponse, ApiErrorResponseModel, ForbiddenException, NotFoundException, InternalServerError
]:
    """
    Register Model
    """
    logP: dict = {'apiName': '/api/v1/endpoint'}
    customlog = logging.LoggerAdapter(request.app.logger, logP)

    customlog.debug('START registerModel==%s',user_id)
    modelService = ModelService(request.app, customlog, user_id)
    modelData = modelService.registerModel(body)
    modelResp = ModelResponse(data=modelData)
    customlog.debug('END registerModel')
    return modelResp

#To get the model details with its metadata and other details like container image, port details using model ID.
@router.get(
    '/models/{modelId}/versions/{version}',
    response_model=ApiResponse,
    responses={#'404': {'model': NotFoundException}, 
               '500': {'model': InternalServerError}},
    status_code=code.HTTP_STATUS_OK           
)
def getModel(request: Request, response: Response,
    modelId: str = Path(..., alias='modelId'),
    version: int = Path(..., alias='version'),
    userId: str = Header(..., alias='userId'),
) -> Union[ApiResponse, NotFoundException, InternalServerError] :
    
    try:
        logP: dict = { 'apiName': MODEL_URL+'/{modelId}' }
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START getModel')
        modelService = ModelService(request.app, customlog, userId)
        modelObj = modelService.getModelWithAccess(modelId,version)
        # apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data=modelObj)
        apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data={'model':modelObj})
        #print(apiResp)
        response.status_code = code.HTTP_STATUS_OK
        customlog.debug('END getModel')
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



#To update the model metadata using model ID.
@router.patch(
    '/models/metadata/{modelId}/version/{version}',
    response_model=ApiResponse,
    responses={
        '400': {'model': ApiErrorResponseModel},
        '500': {'model': InternalServerError},
    }
)
def updateModelMetadata(request: Request, modelId: str = Path(..., alias='modelId'), version: int = Path(..., alias='version'),
    user_id: str = Header(..., alias='userId'), body: ModelMetaData = ...
) -> Union[ApiResponse,ModelMetaDataResponse,ApiErrorResponseModel,ForbiddenException,NotFoundException,InternalServerError]:
    """
    Update Model Metadata
    """
    try:
        logP: dict = {'apiName': '/models/metadata/'+modelId+'/version/'+str(version)}
        print('/models/metadata/'+modelId+'/version/'+str(version))
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START updateModelMetadata==%s',user_id)
        modelService = ModelService(request.app, customlog, user_id)
        metaData = modelService.updateModelMetadata(modelId,version,body)
        metaResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data={'model':metaData})
        customlog.debug('END updateModelMetadata')
        return metaResp

    except ModelException as modelException:
        logP.error(modelException.__dict__)
        raise HTTPException(**modelException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    
#To get the model metadata Task type.
@router.get(
    '/models/metadata/taskType',
    response_model=ApiResponse,
    responses={#'404': {'model': NotFoundException}, 
               '500': {'model': InternalServerError}},
    status_code=code.HTTP_STATUS_OK           
)
def getModelMetadataTaskType(request: Request, response: Response,
    userId: str = Header(..., alias='userId'),
) -> Union[ApiResponse, NotFoundException, InternalServerError] :
    
    try:
        logP: dict = { 'apiName': '/models/metadata/taskType' }
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START getModelMetadataTaskType')
        modelService = ModelService(request.app, customlog, userId)
        modelObj = modelService.getModelMetadataTaskType(userId)
        apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data=modelObj)
        response.status_code = code.HTTP_STATUS_OK
        customlog.debug('END getModelMetadataTaskType')
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
@router.delete(
    '/models/{modelId}/versions/{version}',
    response_model=ApiResponse,
    responses={#'404': {'model': NotFoundException}, 
               '500': {'model': InternalServerError}},
    status_code=code.HTTP_STATUS_OK           
)
def deleteModel(request: Request, response: Response,project_id:str = Query(..., alias='projectId'),
    modelId: str = Path(..., alias='modelId'),
    version: int = Path(..., alias='version'),
    userId: str = Header(..., alias='userId'),
) -> Union[ApiResponse, NotFoundException, InternalServerError] :
    
    try:
        logP: dict = { 'apiName': MODEL_URL+'/{modelId}' }
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START deleteModel')
        modelService = ModelService(request.app, customlog, userId)
        endpointService = EndpointService(request.app, customlog, userId)
        deploymentId = modelService.deleteModel(project_id,modelId,version)
        
        if deploymentId!=None:
            delete="model"
            endpointService.deleteDeployment(deploymentId,delete)
       
        apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data={'Message': "Model deletion is in progress."})
        
        response.status_code = code.HTTP_STATUS_OK
        customlog.debug('END deleteModel')
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
        
    
    
