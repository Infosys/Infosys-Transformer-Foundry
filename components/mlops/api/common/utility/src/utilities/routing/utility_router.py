# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: mms_client_router.py
description: Routing details for Deployment CRUD operations

"""

from fastapi import Depends, Request, Response,Body, APIRouter, Cookie, HTTPException, status
from typing import Union, List
from fastapi.encoders import jsonable_encoder
from utilities.config.logger import CustomLogger
from utilities.mappers.idp_job_response import ESBulkData,ResponseData,OpenAIParams
from utilities.service.utility_service import UtilityService
from utilities.exception.util_exception import UtilityServiceException
import requests
from aicloudlibs.db_management.core.db_manager import AsyncIOMotorClient,get_database
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel,ApiResponse
from aicloudlibs.constants.http_status_codes import HTTP_STATUS_OK,HTTP_STATUS_NOT_FOUND,HTTP_STATUS_BAD_REQUEST
from utilities.constants.util_constants import *
import json
import sys
import datetime
import calendar
import time
import os
from requests.auth import HTTPBasicAuth


router = APIRouter()

from pprint import pprint

# Method to push data to elastic search
@router.post('/utilities/elasticsearch/push', status_code=status.HTTP_200_OK)
def pushDatatoES(request: Request, response: Response,body: ESBulkData):
    log=request.app.logger
    try:
        utilService = UtilityService(request.app)
        print(body)
        res=utilService.pushDatatoES(body)
        log.debug('request Payload:' + str(body))
        if res["status"] != None and res["status"].lower() == "success":
           apiResp = ApiResponse(code=status.HTTP_200_OK, status="SUCCESS", data=res)
           response.status_code=status.HTTP_200_OK
           log.debug('response Payload:' + str(apiResp))
           return apiResp
        else:
           apiResp = ApiResponse(code=500, status="FAILURE", data=res)
           response.status_code=HTTP_STATUS_BAD_REQUEST
           log.debug('response Payload:' + str(apiResp))
           return apiResp
    except (UtilityServiceException) as ue:
        raise HTTPException(**ue.__dict__)

# GET Method to call search api in elastic search associated with modelity
@router.get("/utilities/elastic/{modality}/search",  summary="Simple ELK search GET call.")
async def search_elasticsearch(request: Request, response: Response,modality: str):
    log=request.app.logger
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")

    try:
        utilService = UtilityService(request.app)
        body = await request.json()
        res = utilService.searchDataES(modality, "_search", body)
        elapsed_time = round(time.time() - start_time, 3)
        if res["status"] != None and res["status"].lower() == "success":
            return ResponseData(response=res['data'], responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))
        else:
            return ResponseData(response=None, responseCde=API_RESPONSE_CDE_FAILURE, responseMsg=API_RESPONSE_MSG_FAILURE, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))

    except Exception as e:
        #logger.error(e)
        elapsed_time = round(time.time() - start_time, 3)
        return ResponseData(response=None, responseCde=API_RESPONSE_CDE_FAILURE, responseMsg=API_RESPONSE_MSG_FAILURE, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))

# POST Method to call search api in elastic search associated with modelity
@router.post("/utilities/elastic/{modality}/search",  summary="Calls the ELK search api.")#, include_in_schema=SHOW_PRIVATE_API)
async def filter_elasticsearch(request: Request, modality:str):
    return await filter_elasticsearch(request, modality, "_search")

# POST Method to call count api in elastic search associated with modelity
@router.post("/utilities/elastic/{modality}/count",  summary="Calls the ELK count api.")#, include_in_schema=SHOW_PRIVATE_API)
async def filter_elasticsearch(request: Request, modality:str):
    return await filter_elasticsearch(request, modality, "_count")


async def filter_elasticsearch(request: Request, modality, reqType):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")

    try:
        utilService = UtilityService(request.app)
        body = await request.json()
        res = utilService.searchDataES(modality, reqType, body)
        elapsed_time = round(time.time() - start_time, 3)
        if res["status"] != None and res["status"].lower() == "success":
            return ResponseData(response=res['data'], responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))
        else:
            return ResponseData(response=None, responseCde=API_RESPONSE_CDE_FAILURE, responseMsg=API_RESPONSE_MSG_FAILURE, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))

    except Exception as e:
        elapsed_time = round(time.time() - start_time, 3)
        return ResponseData(response=None, responseCde=API_RESPONSE_CDE_FAILURE, responseMsg=API_RESPONSE_MSG_FAILURE, timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))