# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import calendar
import copy
import datetime
import os
import time
import bson
import traceback
from fastapi import APIRouter, File, UploadFile, Header
from typing import Union
from common.common_util import CommonUtil
from common.file_util import FileUtil
from common.app_config_manager import AppConfigManager
from aicloudlibs.schemas.generic_pipeline_mappers import *
from data.api_schema_data import GetResponseData
from service.mongo_db_handler import MongoDbHandler
from service.jenkin_handler import JenkinHandler
from .pipeline_base import *
import pydantic
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException,MLOpsException
from pydantic.errors import PydanticValueError
from common.constants import ErrorCode, ErrorNT
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from dotenv import dotenv_values, find_dotenv
from aicloudlibs.schemas.generic_pipeline_mappers import *
import pipeline.constants.local_constants as local_errors
from pipeline.exception.exception import PipelineException
from fastapi import Depends, Request, APIRouter, HTTPException
from pipeline.util.log_formatter import LogFormatter
from pipeline.exception.exception import *
from fastapi import Request
import re

pattern = r"^[a-z0-9-]+$"
app_config = AppConfigManager().get_app_config()
log_formatter = LogFormatter('Pipeline Management')

dotenv_path = find_dotenv()

config = dotenv_values(dotenv_path)

class ValidationError(PydanticValueError):
    def __init__(self, error_detail: ErrorNT, **ctx: any) -> None:
        super().__init__(**ctx)
        PydanticValueError.code = str(error_detail.value.code)
        PydanticValueError.msg_template = error_detail.value.message

def resourceDetails(request:Request,pipelineId):
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    document = request.app.database["pipeline_definition"].find_one({'id': pipelineId})
    computeList = [{
                            "type" : "GPU",
                            "maxQty" : 0,
                            "memory" : "20GB",
                            "minQty" : 0
                    },
                    {
                            "type" : "GPU",
                            "maxQty" : 0,
                            "memory" : "80GB",
                            "minQty" : 0
                    },
                    {
                            "type" : "CPU",
                            "maxQty" : 0,
                            "memory" : "0GB",
                            "minQty" : 0
                    }]
    for value in document['pipeline']['flow']:
        for compute in range(len(document['pipeline']['flow'][value]['resourceConfig']['computes'])):
            type = document['pipeline']['flow'][value]['resourceConfig']['computes'][compute]['type']
            maxQty = document['pipeline']['flow'][value]['resourceConfig']['computes'][compute]['maxQty']
            memory = document['pipeline']['flow'][value]['resourceConfig']['computes'][compute]['memory']
            minQty = document['pipeline']['flow'][value]['resourceConfig']['computes'][compute]['minQty']
            if type=="GPU" and memory=="20GB":
                for val in computeList:
                    if val['type']=="GPU" and val['memory']=="20GB":
                        val['maxQty'] = val['maxQty'] + maxQty
                        val['minQty'] = val['minQty'] + minQty
            elif type=="GPU" and memory=="80GB":
                for val in computeList:
                    if val['type']=="GPU" and val['memory']=="80GB":
                        val['maxQty'] = val['maxQty'] + maxQty
                        val['minQty'] = val['minQty'] + minQty
            else:
                for val in computeList:
                    if val['type']=="CPU":
                        memory_value = int(memory.split('GB')[0])
                        memory = int(val['memory'].split('GB')[0])
                        val['maxQty'] = val['maxQty'] + maxQty
                        memory_value = memory_value + memory
                        val['minQty'] = val['minQty'] + minQty
                        val['memory'] = str(memory_value)+"GB"
                        memory = str(memory)+"GB"

    resourceConfiguration = {"computes" :computeList, "volumeSizeinGB" : 0*compute}

    return resourceConfiguration

def updateResourceUsage(userId,projectId,resourceQuotaReq,flag):
        projectDet=APIDBUtils.findOneById("project",projectId)

        errors = []
        if projectDet is None:
            error = ValidationError(ErrorCode.PROJECT_NOT_FOUND)
            errors.append(error)
        tenantId=projectDet['tenantId']

        if tenantId is None or tenantId=="":
            error = ValidationError(ErrorCode.TENANT_NOT_FOUND)
            errors.append(error)
        tenantDetails=APIDBUtils.findOneById("tenant",tenantId)
        if tenantDetails is None:
            error = ValidationError(ErrorCode.TENANT_NOT_FOUND)
            errors.append(error)
        currentResourceUsage=tenantDetails['currentResourceUsage']
        print(currentResourceUsage)
        quotaConfig=tenantDetails['quotaConfig']
        newCurrentResUsage=updateCurrentResourceUsage(currentResourceUsage,resourceQuotaReq,quotaConfig,flag)
        print(newCurrentResUsage)
        if newCurrentResUsage == "Invalid Compute":
            error = ValidationError(ErrorCode.INVALID_COMPUTE_TYPE)
            errors.append(error)
        elif newCurrentResUsage == "VolumeQuotaExceed":
            error = ValidationError(ErrorCode.VOLUME_QUOTA_EXCEEDED)
            errors.append(error)
        elif newCurrentResUsage == "GPUQuotaExceed":
            error = ValidationError(ErrorCode.GPU_QUOTA_EXCEEDED)
            errors.append(error)
        elif newCurrentResUsage == "CPUQuotaExceed":
            error = ValidationError(ErrorCode.CPU_QUOTA_EXCEEDED)
            errors.append(error)
        elif newCurrentResUsage == "MemoryQuotaExceed":
            error = ValidationError(ErrorCode.MEMORY_QUOTA_EXCEEDED)
            errors.append(error)
        else:
            filter={"id": tenantId,"isDeleted": pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.datetime.utcnow()
            newValues={'$set': {'currentResourceUsage': newCurrentResUsage,'modifiedOn': last_modified_at, 'updatedBy': userId}}
            tenant_update_obj = APIDBUtils.updateEntity("tenant",filter,newValues)

        if len(errors) > 0:
            print(errors)
            raise RequestValidationError(errors=[
                ErrorWrapper(exc=error, loc=('body', 'root'),),])
        else:
            return "Success"

def getGPUQuotaDetails(reqMemory,computes,reqType):
       minQty=0
       maxQty=0
       for compute in computes:
         if compute['memory']== reqMemory and compute['type'].lower()==reqType.lower() :
           minQty=minQty+compute['minQty']
           maxQty=maxQty+compute['maxQty']
       return minQty,maxQty

def getCPUQuotaDetails(computes):
       minQty=0
       maxQty=0
       memoryVal=0
       for compute in computes:
         if compute['type'].lower() == 'cpu':
           minQty=minQty+compute['minQty']
           maxQty=maxQty+compute['maxQty']
           memory=compute['memory']
           memory=memory.lower().replace("gb","")
           memoryVal=memoryVal+int(memory)
       return minQty,maxQty,memoryVal

def updateCurrentResourceUsage(currentResourceUsage,resourceQuotaReq,quotaConfig,flag):
    newCurrentResUsage=""
    updateDict=currentResourceUsage
    reqValue=resourceQuotaReq['volumeSizeinGB']
    oldValue=currentResourceUsage['volumeSizeinGB']
    maxValue=quotaConfig['volumeSizeinGB']
    if flag=="allocate":
      newValue=oldValue+reqValue
      if newValue > maxValue :
          newCurrentResUsage="VolumeQuotaExceed"
    else:
      newValue=oldValue-reqValue
      if newValue < 0:
          newValue=0
    if newCurrentResUsage != "VolumeQuotaExceed" :
        updateDict['volumeSizeinGB']=newValue
        computes=resourceQuotaReq['computes']
        currComputes=updateDict['computes']
        for compute in computes:
              if compute['type'].lower() == "gpu":
                reqMinQty= int(compute['minQty'])
                reqMaxQty= int(compute['maxQty'])
                reqGPUMemory=compute['memory']
                for currentCompute in currComputes:
                    if currentCompute['type'].lower()== "gpu" and currentCompute['memory'].lower()==reqGPUMemory.lower():
                        oldMinValue=currentCompute['minQty']
                        oldMaxValue=currentCompute['maxQty']
                        totalMinVal,totalMaxValue=getGPUQuotaDetails(reqGPUMemory,quotaConfig['computes'],"gpu")
                        if flag=="allocate":
                          newMinValue=oldMinValue+reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue+reqMaxQty
                          if newMaxValue > totalMaxValue:
                              newCurrentResUsage = "GPUQuotaExceed"
                        else:
                          newMinValue=oldMinValue-reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue-reqMaxQty
                          if newMaxValue < 0:
                              newMaxValue=0
                        if newCurrentResUsage == "":
                            currentCompute['minQty']=newMinValue
                            currentCompute['maxQty']=newMaxValue

              elif compute['type'].lower() == "cpu":
                reqMinQty= int(compute['minQty'])
                reqMaxQty= int(compute['maxQty'])
                reqCPUMemory=compute['memory']
                reqCPUMemVal=reqCPUMemory.lower().replace("gb","")
                totalMinVal,totalMaxVal,totalMemory=getCPUQuotaDetails(quotaConfig['computes'])

                for currentCompute in currComputes:
                    if currentCompute['type'].lower()== "cpu":
                      oldMinValue=currentCompute['minQty']
                      oldMaxValue=currentCompute['maxQty']
                      oldMem=currentCompute['memory']
                      oldMemValue=oldMem.lower().replace("gb","")
                      if flag=="allocate":
                          newMinValue=oldMinValue+reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue+reqMaxQty
                          if newMaxValue>totalMaxVal:
                              newCurrentResUsage = "CPUQuotaExceed"
                          if newCurrentResUsage !="CPUQuotaExceed":
                              newMemValue=int(oldMemValue)+int(reqCPUMemVal)
                              if newMemValue > totalMemory:
                                  newCurrentResUsage = "MemoryQuotaExceed"
                      else:
                          newMinValue=oldMinValue-reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue-reqMaxQty
                          if newMaxValue < 0:
                              newMaxValue=0

                          if newCurrentResUsage !="CPUQuotaExceed":
                              newMemValue=int(oldMemValue)-int(reqCPUMemVal)
                              if newMemValue < 0:
                                  newMemValue=0

                      if newCurrentResUsage =="":
                          currentCompute['minQty']=newMinValue
                          currentCompute['maxQty']=newMaxValue
                          currentCompute['memory']=str(newMemValue)+"GB"
              else:
                    newCurrentResUsage="Invalid Compute"
    if newCurrentResUsage == "" :
        newCurrentResUsage=updateDict
        print(currentResourceUsage)
    print(newCurrentResUsage)
    return newCurrentResUsage

# APIRouter creates path operations for module
router = APIRouter(prefix="/api/v2/pipelines", responses={404: {"description": "Not found"}})

# To trigger pipeline using that repective pipelineId
@router.post("/execute/{pipelineId}", response_model=GetResponseData, tags=["execution"],
             summary="Executes a new instance of an existing pipeline definition")
async def execution_create(request:Request,input_json: PipelineExecution, pipelineId, userId: Union[str, None] = Header()):
    start_time = time.time()
    log = request.app.logger
    date = datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    doc_data = {}
    po_doc_data = {}
    execution_record_id = FileUtil.get_uuid()
    # mongo db accepts with 24 hex string
    job_id_in_jenkin = FileUtil.get_hex_uuid()[:24]
    document = request.app.database["pipeline_definition"].find_one({'id': pipelineId})
    try:
        if document is None:
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)
    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)

    input_data = input_json.dict()

    has_access = hasAccess(
        userId, document['projectId'], EXECUTEPIPELINE)
    try:
        if not has_access:
            raise ForbiddenException()
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)

    existing_data = {'pipeline':document['pipeline']}
    updated_data = copy.deepcopy(existing_data)

    try:
        if len(input_data['pipeline']['dataStorage'])>1:
            raise InvalidValueError(local_errors.ErrorCode.DATA_STORAGE_ERROR)

        if len(input_data['pipeline']['variables']) == 0:
            raise InvalidValueError(local_errors.ErrorCode.VARIABLE_EMPTY_ERROR)

        for key in input_data['pipeline']['variables'].keys():
            if not key in existing_data['pipeline']['variables']:
                raise InvalidValueError(local_errors.ErrorCode.VARIABLE_KEY_ERROR)

        for key in input_data['pipeline']['globalVariables'].keys():
            if not key in existing_data['pipeline']['globalVariables']:
                raise InvalidValueError(local_errors.ErrorCode.GLOBALVARIABLE_KEY_ERROR)

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    # validation of run time variable end
    updated_data['pipeline'].update({'dataStorage': input_data['pipeline']['dataStorage'],
                                     'variables': input_data['pipeline']['variables'],
                                     'globalVariables': input_data['pipeline']['globalVariables']})
    jenkin_data = {}
    run_arguments_list = []
    for key, value in updated_data['pipeline']['variables'].items():
        run_arg = {
            "name": key,
            "argValue": value
        }
        run_arguments_list.append(run_arg)

    projectObj = request.app.database['project'].find_one({'id': document['projectId']})
    tenantObj = request.app.database['tenant'].find_one({'id' : projectObj['tenantId']})
    tenantId = projectObj['tenantId']

    j_input_data = {
        "pipeline" : document['pipeline'],
        "runName": f"{updated_data['pipeline']['name']}-run-{execution_record_id[:8]}",
        "runArguments": run_arguments_list,
        "pipelineId" : document['id'],
        "executionId": execution_record_id,
        "projectId" : document['projectId'],
        "description" : document['description'],
        "version" : document['pipeline']['version'],
        "tenantName" : tenantObj['name']
    }
    j_request_json = {
        "jobId": job_id_in_jenkin,
        "inputData": j_input_data
    }
    jenkin_data['_id'] = bson.objectid.ObjectId(job_id_in_jenkin)
    jenkin_data['jobName'] = 'Pipeline execution'
    jenkin_data['status'] = 'INITIATED'
    jenkin_data['requestJson'] = j_request_json
    jenkin_data['isDeleted'] = False
    request.app.database["idp_job_details"].insert_one(jenkin_data)

    # calling the jenkin to see if it has been trigger or not:start
    if TRIGGER_JENKIN:
        jen_obj = JenkinHandler(j_request_json['jobId'])
        jen_obj.invokeJenkinsPipeline()

    execution_data = {
        "projectId": document['projectId'],
        "pipelineId": pipelineId,
        "pipeline": input_data['pipeline'],
        "jobId": job_id_in_jenkin,
        "runId": "",
        "status": None,
        "errorMsg": None
    }
    doc_data['createdBy'] = userId
    doc_data['createdOn'] = date_time_stamp
    doc_data['isDeleted'] = False
    doc_data['updatedBy'] = "null"
    doc_data['modifiedOn'] = "null"
    doc_data['projectId'] = execution_data['projectId']
    doc_data['pipelineId'] = execution_data['pipelineId']
    doc_data['pipeline'] = execution_data['pipeline']
    doc_data['jobId'] = job_id_in_jenkin
    doc_data['runId'] = ""
    doc_data['status'] = None
    doc_data['erroMsg'] = None
    doc_data['status']= "Created"
    doc_data['id'] = execution_record_id
    output_dict = {
        "executionId": doc_data['id']
    }
    request.app.database["pipeline_execution"].insert_one(doc_data)
    mongo_db_handler.disconnect()
    response = GetResponseData(code = 0, status = "Success", data = output_dict)
    return response

# To get the details of the repective executionId
@router.get("/execution/{executionId}", response_model=GetResponseData, tags=["execution"],
            summary="Returns the status of a pipeline in execution or that has completed execution")
async def get_execution_detail(request:Request,executionId, userId):
    log = request.app.logger
    start_time = time.time()
    date = datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)

    document = request.app.database['pipeline_execution'].find_one({'id': executionId},{'_id': 0})
    try:
        if document is None:
            raise InvalidValueError(local_errors.ErrorCode.EXECUTION_NOT_FOUND_ERROR)
    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    has_access = hasAccess(
        userId, document['projectId'], EXECUTEPIPELINE)
    try:
        if not has_access:
            raise ForbiddenException()
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)

    get_execution_data = request.app.database['pipeline_execution'].find_one({'id': executionId},{'_id': 0})
    get_execution_data=dict(get_execution_data)
    if not get_execution_data:
        mongo_db_handler.disconnect()
        return GetResponseData(responseMsg= current_jenkin_error)

    get_jenkin_data = request.app.database["idp_job_details"].find_one({'requestJson.jobId': get_execution_data['jobId']})

    if get_jenkin_data['status'] is not None and get_jenkin_data['status'].upper() == "FAILURE":
        current_jenkin_error = get_jenkin_data.get('responseJson').get('errorMsg')

        return GetResponseData(code = 2343, status = "Failure", data = {"Message": current_jenkin_error})
    else:
        response_dict = {"data":get_execution_data}
        return GetResponseData(code = 200, status = "Success", data = {"response": response_dict})

# To get the list of execution of the repective pipelineId
@router.get("/list/{pipelineId}/execution", response_model=GetResponseData, tags=["execution"], summary= "Return the list of execution ids associated with the pipeline",include_in_schema=False)

async def get_execution_list(request:Request,pipelineId, userId):
    start_time = time.time()
    date = datetime.utcnow()
    log = request.app.logger
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    output_response = []
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)

    doc = request.app.database['pipeline_definition'].find_one({'id': pipelineId})
    try:
        if doc is None:
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)
    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    projectId = doc['projectId']

    documents = list(request.app.database['pipeline_execution'].find({"pipelineId": pipelineId},{'_id': 0}))

    output_response = documents

    has_access = hasAccess(userId, projectId, VIEW)
    try:
        if not has_access:
            raise ForbiddenException()
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    else:
        elapsed_time = round(time.time() - start_time, 3)
        response = GetResponseData(code = API_RESPONSE_CDE_SUCCESS, status = API_RESPONSE_MSG_SUCCESS, data = {'executions':output_response})
    return response