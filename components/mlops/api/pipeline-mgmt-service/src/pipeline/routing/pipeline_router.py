# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: pipeline_router.py
description: Routing details for Pipeline CRUD operations
"""
import json
from bson import json_util, ObjectId
from fastapi import Request, Header
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Request, APIRouter, HTTPException
from aicloudlibs.schemas.pipeline_mappers import PipelineJobDetails, PipelineResponse, ResponseModel, \
    ListPipelineResponse, DeletePipelineResponse, GetPipelineResponse
from aicloudlibs.schemas.global_schema import NotAuthorizedError, InternalServerError
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException
from aicloudlibs.constants.http_status_codes import HTTP_NOT_AUTHORIZED_ERROR, HTTP_STATUS_INTERNAL_SERVER_ERROR
from pipeline.exception.exception import PipelineException
from pipeline.service.pipeline_service import PipelineService as service, BaseService
import pipeline.constants.local_constants as constant
from pipeline.util.log_formatter import LogFormatter
from typing import List

router = APIRouter()
log_formatter = LogFormatter('Pipeline Management')

"""
method: Create Pipeline 
description: Defines the routing path details for create usecase operation
             and invokes the create pipeline

params:
   :payload - A pydantic model object for input payload
   :db_session - invokes the get_db funstion and get the db session object
returns:
   :pipeline - A pydantic model object for output with pipeline id

exceptions:
    :PipelineException - handles the Pipeline specific exception thrown by create pipeline service     
"""

def _get_encoded_response(data: dict):
    dumped_data = json_util.dumps(data, indent=4, default=json_util.default)
    page_sanitized = json.loads(dumped_data, object_hook=json_util.object_hook)
    return page_sanitized

# To Trigger the finetuning Pipeline
@router.post("/pipelines", response_model=PipelineResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def create_pipeline(request: Request, payload: PipelineJobDetails, userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Pipeline Management", "createPipeline " + "{senderURI }" + "{RequestID }", str(userId), str(PipelineJobDetails))
    log = request.app.logger

    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"create_pipeline - request : " + str(PipelineJobDetails)))
        service_obj = service(request.app)
        pipeline_detail = service_obj.create_pipeline(payload, userId)
        log.debug("response : " + str(pipeline_detail))
        PipelineResponse.data = jsonable_encoder(pipeline_detail)
        responseDict = PipelineResponse.__dict__
        return responseDict

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To get all the pipelines creates for the project id and user
@router.get("/pipelines", response_model=ListPipelineResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def list_pipeline(request: Request, projectId: str, userId: str = Header(convert_underscores=False)):
    '''
    method: list Pipeline
    description: get all the pipelines creates for the project id and user

    params:
    :projectId - String, valid project id
    :userId - String, valid user id
    returns:
    :pipeline - list of pydantic model objects for output with pipeline id
    exceptions:
        :PipelineException - handles the Pipeline specific exception thrown by create pipeline service
    '''
    log = request.app.logger
    log_formatter.set_prefixes('list Pipeline', userId, 'NA')
    try:
        log.info(log_formatter.get_msg(f"list_pipeline - request : {str(projectId)} {str(userId)}"))
        service_obj = service(request.app)
        pipeline_list = service_obj.list_pipeline(request, projectId, userId)
        log.debug(log_formatter.get_msg("response : " + str(pipeline_list)))
        ListPipelineResponse.data = jsonable_encoder(pipeline_list)
        responseDict = ListPipelineResponse.__dict__
        return responseDict

    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To get the pipelines based on pipelineId
@router.get("/pipelines/{pipelineId}", response_model=GetPipelineResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def get_pipeline(request: Request, pipelineId: str, userId: str = Header(convert_underscores=False)):
    '''
    method: get Pipeline
    description: get the pipelines based on pipelineId

    params:
    :pipelineId - String, valid pipeline id
    :userId - String, valid user id
    returns:
    :pipeline - list of pydantic model objects for output with pipeline id
    exceptions:
        :PipelineException - handles the Pipeline specific exception thrown by create pipeline service     
    '''
    log_formatter.set_prefixes('Get Pipeline', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"get_pipeline - request : {str(pipelineId)}  {str(userId)}"))
        service_obj = service(request.app)
        get_pipeline_details = service_obj.get_pipeline(request, pipelineId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(get_pipeline_details)}"))
        GetPipelineResponse.data = jsonable_encoder(get_pipeline_details)
        responseDict = GetPipelineResponse.__dict__
        return responseDict

    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To delete the pipeline based on pipelineId and userId
@router.delete("/pipelines/{pipelineId}", response_model=DeletePipelineResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def delete_pipeline(request: Request, pipelineId: str, userId: str = Header(convert_underscores=False)):
    '''
    method: delete Pipeline
    description: delete the pipeline based on pipelineId

    params:
    :pipelineId - String, valid pipeline id
    :userId - String, valid user id
    returns:
    :pipeline - the popped pipeling from the colelction
    exceptions:
        :PipelineException - handles the Pipeline specific exception
        thrown by create pipeline service
    '''
    log_formatter.set_prefixes('Delete Pipeline', userId, 'NA')
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"delete_pipeline - request : {str(pipelineId)}  {str(userId)}"))
        service_obj = service(request.app)
        pipeline_delete = service_obj.delete_pipeline(request, pipelineId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(pipeline_delete)}"))
        DeletePipelineResponse.data = jsonable_encoder(pipeline_delete)
        responseDict = DeletePipelineResponse.__dict__
        return responseDict

    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)