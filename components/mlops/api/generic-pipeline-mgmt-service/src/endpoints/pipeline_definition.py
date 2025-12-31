# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import calendar
import copy
import datetime
import json
import os
import time
import traceback
import bson
import re
from fastapi import Request
from fastapi import APIRouter, File, UploadFile, Header, FastAPI
from typing import Union
import urllib
from common.common_util import CommonUtil
from common.file_util import FileUtil
from common.app_config_manager import AppConfigManager
from aicloudlibs.schemas.generic_pipeline_mappers import *
from data.api_schema_data import GetResponseData
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException,MLOpsException
from service.mongo_db_handler import MongoDbHandler
from .pipeline_base import *
from pydantic.errors import PydanticValueError
from common.constants import ErrorNT
from service.jenkin_handler import JenkinHandler
from pipeline.exception.exception import *
import pydantic
import pipeline.constants.local_constants as local_errors
from aicloudlibs.db_management.core.db_utils import connect_mongodb, get_db
from pipeline.util.log_formatter import LogFormatter
from pipeline.exception.exception import PipelineException
from fastapi import Depends, Request, APIRouter, HTTPException

app_config = AppConfigManager().get_app_config()
pattern = r"^[a-z0-9-]+$"
log_formatter = LogFormatter('Pipeline Management')

# APIRouter creates path operations for module
router = APIRouter(prefix="/api/v2/pipelines", responses={404: {"description": "Not found"}})

class ValidationError(PydanticValueError):
    def __init__(self, error_detail: ErrorNT, **ctx: any) -> None:
        super().__init__(**ctx)
        PydanticValueError.code = str(error_detail.value.code)
        PydanticValueError.msg_template = error_detail.value.message

# To create a new pipeline for Finetuning task
@router.post("/create", response_model=GetResponseData, tags=["definition"], summary="Creates a new pipeline definition")
async def schema_api( request:Request,input_json: Pipeline,userId: Union[str, None] = Header()):
    date = datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    log = request.app.logger
    # pydantic object to dictionary
    input_data = input_json.dict()
    input_data['inputArtifacts_flag'] = False
    input_doc_data = {}
    po_doc_data = {}
    try:
        json.loads(json.dumps(input_data))
    except ValueError:
        return "Invalid json"

    projectObj = request.app.database["project"].find_one({"id": input_data['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
    try:
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    tenantObj = request.app.database["tenant"].find_one({'id' : projectObj['tenantId']})

    # user validation: start
    has_access = hasAccess(userId, input_data['projectId'], CREATEPIPELINE)
    try:
        if not has_access:
            raise ForbiddenException()
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)

    project_id = input_data['projectId']
    name = input_data['pipeline']['name']
    version = input_data['pipeline']['version']

    try:
        document = request.app.database["pipeline_definition"].find_one({'projectId': project_id, 'pipeline.version': version,'pipeline.name':name})
        if document != None:
            raise PipelineAlreadyExistsError(local_errors.ErrorCode.PIPELINE_EXIST_ERROR)
    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)

    for arg in input_data['pipeline']['flow']:
        if input_data['pipeline']['flow'][arg]['inputArtifacts'] != None:
            input_data['inputArtifacts_flag'] = True
            break
    try:
        if len(input_data['pipeline']['dataStorage'])>1:
            raise InvalidValueError(local_errors.ErrorCode.DATA_STORAGE_ERROR)

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)

    uuid = FileUtil.get_uuid()
    input_doc_data['createdBy'] = userId
    input_doc_data['createdOn'] = date_time_stamp
    input_doc_data['isDeleted'] = False
    input_doc_data['updatedBy'] = "null"
    input_doc_data['modifiedOn'] = "null"
    input_doc_data['tenantName'] = tenantObj['name']
    input_doc_data['projectId'] = input_data['projectId']
    input_doc_data['description'] = input_data['description']
    input_doc_data['pipeline'] = input_data['pipeline']
    input_doc_data['status']= "Created"
    input_doc_data['id'] = uuid

    job_id_in_jenkin = FileUtil.get_hex_uuid()[:24]
    jenkin_data = {}
    jenkin_data['_id'] = bson.objectid.ObjectId(job_id_in_jenkin)
    jenkin_data['jobId'] = job_id_in_jenkin
    jenkin_data['jobName'] = 'Pipeline Definition'
    jenkin_data['status'] = None
    jenkin_data['requestJson'] = {}
    jenkin_data['requestJson']['jobId'] = job_id_in_jenkin
    jenkin_data['requestJson']['tenantName'] = tenantObj['name']
    jenkin_data['requestJson']['inputData'] = input_data
    jenkin_data['isDeleted'] = False

    request.app.database["idp_job_details"].insert_one(jenkin_data)

    #Jenkins Call
    if TRIGGER_JENKIN:
        jen_obj = JenkinHandler(jenkin_data['jobId'])
        jen_obj.invokeJenkinsMultiPipeline()
    time.sleep(30)

    document = request.app.database["idp_job_details"].find_one({'jobId': job_id_in_jenkin})
    try:
        if document['status'] == "SUCCESS":
            request.app.database["pipeline_definition"].insert_one(input_doc_data)
            print("sucessfully inserted")
            output_response = {
                    "response" : input_data,
                    "id": uuid
                }
            response_cde = API_RESPONSE_CDE_SUCCESS
            response_msg = API_RESPONSE_MSG_SUCCESS

        else:
            raise JenkinsJobError("Error Occured while creating pipeline")
    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except MLOpsException as mle:
        raise HTTPException(**mle.__dict__)

    response = GetResponseData(code = response_cde, status = response_msg, data = output_response)
    return response

# To get detail of the pipeline using pipelineId
@router.get("/{pipelineId}", response_model=GetResponseData, tags=["definition"],
            summary="Returns the details of an existing pipeline definition")
async def get_result(request:Request,pipelineId,userId):

    date = datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    log = request.app.logger
    date_time_stamp = datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    output_response = {}
    document = request.app.database["pipeline_definition"].find_one({'id': pipelineId},{'_id': 0})
    try:
        if document is None:
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)
    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)

    has_access = hasAccess(
        userId, document['projectId'], CREATEPIPELINE)
    try:
        if not has_access:
            raise ForbiddenException()
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)

    print(document)
    if document:
        output_response = document
    else:
        output_response = {"message":  "No data found"}
    response_msg = API_RESPONSE_MSG_SUCCESS
    response_cde = API_RESPONSE_CDE_SUCCESS
    response = GetResponseData(code = response_cde, status = response_msg, data = output_response)
    return response

# To get the list pipelines triggered using that repective projectId
@router.get("/list/{projectId}", response_model=GetResponseData, tags=["definition"],
            summary="Returns the list of pipeline definition associated with projectId", include_in_schema=False)
async def get_projectId_result_list(projectId, userId):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)

    documents = mongo_db_handler.get_documents_without_id(PIPELINE_COLLECTION, {"projectId": projectId, "isDeleted":"false"})
    documents = CommonUtil.sort_datalist_by_date(documents, 'createdOn')
    output_response = documents

    projectObj = mongo_db_handler.get_document(PROJECT, {'id': projectId})

    if projectId == "":
        output_response = {"Message": "Project Id is required and it should not be empty"}
        response = GetResponseData(code = 999,status = "Failure",data = output_response)
        return response
    else:
        if projectObj == None:
            output_response = {"Message": "Project id is not valid"}
            response = GetResponseData(code = 999,status = "Failure",data = output_response)
            return response

    has_access = hasAccess(userId, projectId, VIEW)
    if not has_access:
        API_RESPONSE_CDE_FAILURE
        output_response = {"Message": "You are not authorized to do this transaction"}
        response = GetResponseData(code = API_RESPONSE_CDE_FAILURE, status = API_RESPONSE_MSG_FAILURE, data = output_response)
    else:
        elapsed_time = round(time.time() - start_time, 3)
        response = GetResponseData(code = API_RESPONSE_CDE_SUCCESS, status = API_RESPONSE_MSG_SUCCESS, data = {'pipelines':output_response})

    return response