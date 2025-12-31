# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: trial_router.py
description: Routing details for Pipeline Trial CRUD operations

"""
from fastapi import Depends, Request, APIRouter, HTTPException, Response, status, Header
from pipeline.exception.exception import PipelineException
from pipeline.service.trial_service import PipelineTrialService as service
import json
from bson import json_util
import pipeline.constants.local_constants as constant
from aicloudlibs.schemas.pipeline_mappers import TrialResponse, PipelineTrial, ResponseModel, GetTrialResponse, GetTrialResponseData
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException, \
    MLOpsException
from aicloudlibs.constants.http_status_codes import HTTP_NOT_AUTHORIZED_ERROR, HTTP_STATUS_INTERNAL_SERVER_ERROR, HTTP_STATUS_OK
from aicloudlibs.schemas.global_schema import NotAuthorizedError, InternalServerError, ApiResponse, ApiErrorResponseModel
from fastapi.encoders import jsonable_encoder
from pipeline.util.log_formatter import LogFormatter
from pipeline.mappers.mappers import ErrorResponseModel

router = APIRouter()
log_formatter = LogFormatter('Trail Management')


def _get_encoded_response(data: dict):
    # enconding object id into string
    dumped_data = json_util.dumps(data, indent=4, default=json_util.default)
    page_sanitized = json.loads(dumped_data, object_hook=json_util.object_hook)
    return page_sanitized

# To Trigger the trial for the pipeline based on the pipelineId
@router.post("/pipelines/trial", response_model=TrialResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def trial_pipeline(request: Request, payload: PipelineTrial, userId: str = Header(convert_underscores=False)):
    log_formatter.set_prefixes('Trail Pipeline',  "{senderURI }", "{RequestID }")
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"trial_pipeline - request : {str(PipelineTrial)}"))
        service_obj = service(request.app)
        pipeline_trail = service_obj.trial_pipeline(payload, userId)
        log.debug(log_formatter.get_msg(f"response : {str(pipeline_trail)}"))
        TrialResponse.data = jsonable_encoder(pipeline_trail)
        responseDict = TrialResponse.__dict__
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
    except MLOpsException as mle:
        raise HTTPException(**mle.__dict__)

# To Set the run status to the trail table
@router.post("/pipelines/trial/update", include_in_schema=False)
def set_run_status(request: Request, runId: str = "", status: str = ""):
    '''
    method: Set Run Status
    description: Set the run status to the trail table

    params:
    :runId - runId to get the unique row
    :status - status of the trail run
    returns:
    :message if the run status is suceeded or not

    exceptions:
        :RunStatusException - handles the RunStatus specific exception
        thrown by RunStatus Service
    '''
    log_formatter.set_prefixes('Run Status', "kubeflow", "kubeflow")
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(
            f"Set Run Status - request : runId={str(runId)} and status={status}"))
        status_service = service(request.app)
        pipeline_trail, code = status_service.set_run_status(runId, status)
        page_sanitized = _get_encoded_response(pipeline_trail)
        log.debug(log_formatter.get_msg(f"response : {pipeline_trail}"))
        if code != 200:
            return ErrorResponseModel(code, page_sanitized)
        return ResponseModel(page_sanitized)
    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)

# To Set the run status to the trail table
@router.post("/pipelines/trial/metricUpdate", include_in_schema=False)
def set_metric_output(request: Request, runId: str, metrics: str):
    '''
    method: Set Metric Output
    description: Set the run status to the trail table

    params:
    :runId - runId to get the unique row
    :metrics - metric output of the trail run
    returns:
    :message if the metric output update is suceeded or not

    exceptions:
        :MetricOutput - handles the MetricOutput specific exception
        thrown by MetricOutput Service   
    '''
    log_formatter.set_prefixes('Run Status', "kubeflow", "kubeflow")
    log = request.app.logger
    try:
        log.info(log_formatter.get_msg(f"Set Metric Output - request : runId: {str(runId)} metrics :{metrics}"))
        status_service = service(request.app)
        pipeline_trail, code = status_service.set_metrics_output(runId, metrics)
        page_sanitized = _get_encoded_response(pipeline_trail)
        log.debug(log_formatter.get_msg(f"response : {pipeline_trail}"))
        if code != 200:
            return ErrorResponseModel(code, page_sanitized)
        return ResponseModel(page_sanitized)
    except PipelineException as cie:
        log.error(log_formatter.get_msg(str(cie.__dict__)))
        raise HTTPException(**cie.__dict__)

# To get the trial details based on the trialId and userId
@router.get("/pipelines/trial/trialId", response_model = GetTrialResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def get_trial_status(request: Request, trialId: str, userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Pipeline Management", "trialPipeline" + "{senderURI }" + "{RequestID }", str(userId), str(PipelineTrial))
    log = request.app.logger
    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"get_trial_status - request : " + str(trialId)))
        service_obj = service(request.app)
        trial = service_obj.get_trial_details(trialId, userId)
        log.debug("response : " + str(trial))
        GetTrialResponse.data = jsonable_encoder(trial)
        responseDict = GetTrialResponse.__dict__
        return responseDict

    except PipelineException as pipelineException:
        log.error(pipelineException.__dict__)
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To Terminate the trial details based on the trialId and userId
@router.post("/pipelines/trial/terminate/{trialId}", response_model = ApiErrorResponseModel, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def terminate_pipeline(request: Request, trialId: str, userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Pipeline Management", "trialPipeline" + "{senderURI }" + "{RequestID }", str(userId), str(trialId))
    log = request.app.logger
    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"terminate_pipeline - request : " + str(trialId)))
        service_obj = service(request.app)
        trial = service_obj.terminate_pipeline(trialId, userId)
        log.debug("response : " + str(trial))
        responseDict = ApiErrorResponseModel(code= HTTP_STATUS_OK, status= "SUCCESS", message= trial)
        return responseDict

    except PipelineException as pipelineException:
        log.error(pipelineException.__dict__)
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)