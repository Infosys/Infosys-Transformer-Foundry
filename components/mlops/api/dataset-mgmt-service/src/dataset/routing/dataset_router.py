# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import logging
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, status, Header, Response, Query, Path
from typing import Union, List, Any
from bson import json_util
import json
from dataset.mappers.dataset_mappers import *
from dataset.service.dataset_service import *
from aicloudlibs.schemas.global_schema import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.schemas.model_mappers import *
import aicloudlibs.constants.http_status_codes as code
import aicloudlibs.constants.error_constants as status
import dataset.constants.local_constants as constant
from dataset.service.dataset_service import DatasetService as service, BaseService
from dataset.util.log_formatter import LogFormatter

def _get_encoded_response(data: dict):
    dumped_data = json_util.dumps(data, indent=4, default=json_util.default)
    page_sanitized = json.loads(dumped_data, object_hook=json_util.object_hook)
    return page_sanitized

router = APIRouter()
log_formatter = LogFormatter('Dataset Management')

# Register Dataset API
@router.post("/datasets",response_model=DatasetResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def register_dataset(request: Request, payload: DataSchema, userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Dataset Management", "registerDataset " + "{senderURI }" + "{RequestID }", str(userId), str(DataSchema))
    log = request.app.logger
    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"register_dataset - request : " + str(DataSchema)))
        service_obj = service(request.app)
        dataset_detail = service_obj.register_dataset(payload, userId)
        log.debug("response : " + str(dataset_detail))
        DatasetResponse.code = 200
        DatasetResponse.status = "Success"
        DatasetResponse.data = jsonable_encoder(dataset_detail)
        responseDict = DatasetResponse.__dict__
        return responseDict

    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    
# Get Userlist API
@router.get("/datasets/projectId",response_model=UserlistResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def get_userlist(request: Request, projectId: str,userId: str = Header(convert_underscores=False)):
    log_formatter.set_prefixes('Get Userlist', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"get_userlist - request : {str(projectId)}  {str(userId)}"))
        service_obj = service(request.app)
        user_list = service_obj.get_userlist(projectId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(user_list)}"))
        UserlistResponse.code = 200
        UserlistResponse.status = "Success"
        UserlistResponse.data = jsonable_encoder(user_list)
        responseDict = UserlistResponse.__dict__
        return responseDict
    
    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# List Dataset API
@router.get("/datasets",response_model=ListDatasetResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def list_dataset(request : Request, projectId: str, userId:str =Header(convert_underscores=False)):
    log_formatter.set_prefixes('List Dataset', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"list_dataset - request : {str(projectId)}  {str(userId)}"))
        service_obj = service(request.app)
        dataset_list = service_obj.list_dataset(projectId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(dataset_list)}"))
        ListDatasetResponse.code= 200
        ListDatasetResponse.status = "Success"
        ListDatasetResponse.data = jsonable_encoder(dataset_list)
        responseDict = ListDatasetResponse.__dict__
        return responseDict
    
    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# List Dataset by Scope API
@router.get("/datasets/scope",response_model=ListDatasetResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def list_datasset_by_scope(request : Request,scope: ScopeType, userId: str=Header(convert_underscores=False)):
    log_formatter.set_prefixes('List Dataset by Scope', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"list_dataset_by_scope - request : {str(scope)}  {str(userId)}"))
        service_obj = service(request.app)
        dataset_list = service_obj.list_dataset_by_scope(scope, userId)
        log.debug(log_formatter.get_msg(f"response : {str(dataset_list)}"))
        ListDatasetResponse.code= 200
        ListDatasetResponse.status = "Success"
        ListDatasetResponse.data = jsonable_encoder(dataset_list)
        responseDict = ListDatasetResponse.__dict__
        return responseDict
    
    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    

# Get Dataset API By ID
@router.get("/datasets/datasetId",response_model=GetDatasetResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def get_dataset(request : Request, datasetId:str, userId:str=Header(convert_underscores=False) ):
    log_formatter.set_prefixes('Get Dataset', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"get_dataset - request : {str(datasetId)}  {str(userId)}"))
        service_obj = service(request.app)
        dataset = service_obj.get_dataset(datasetId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(dataset)}"))
        GetDatasetResponse.code= 200
        GetDatasetResponse.status = "Success"
        GetDatasetResponse.data = jsonable_encoder(dataset)
        responseDict = GetDatasetResponse.__dict__
        return responseDict

    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    

# Delete Dataset API By ID
@router.delete("/datasets/datasetId",response_model=DeleteDatasetResponse,responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def delete_dataset(request : Request, datasetId:str, userId:str=Header(convert_underscores=False) ):
    log_formatter.set_prefixes('Delete Dataset', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"delete_dataset - request : {str(datasetId)}  {str(userId)}"))
        service_obj = service(request.app)
        dataset = service_obj.delete_dataset(datasetId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(dataset)}"))
        DeleteDatasetResponse.code= 200
        DeleteDatasetResponse.status = "Success"
        DeleteDatasetResponse.data = jsonable_encoder(dataset)
        responseDict = DeleteDatasetResponse.__dict__
        return responseDict

    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    

# Update Dataset API By ID
@router.patch("/datasets/datasetId",response_model=DatasetResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def update_dataset(request : Request,payload: DataSchema, datasetId:str, userId:str=Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Dataset Management", "updateDataset " + "{senderURI }" + "{RequestID }", str(userId), str(DataSchema))
    log = request.app.logger
    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"update_dataset - request : " + str(DataSchema)))
        service_obj = service(request.app)
        dataset_detail = service_obj.update_dataset(payload,datasetId, userId)
        log.debug("response : " + str(dataset_detail))
        DatasetResponse.code = 200
        DatasetResponse.status = "Success"
        DatasetResponse.data = jsonable_encoder(dataset_detail)
        responseDict = DatasetResponse.__dict__
        return responseDict

    except DatasetException as datasetException:
        log.error(log_formatter.get_msg(str(datasetException.__dict__)))
        raise HTTPException(**datasetException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)