# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

import calendar
import copy
import datetime
import time
from typing import Union
from fastapi import APIRouter, File, UploadFile, Header
from common.file_util import FileUtil
from common.app_config_manager import AppConfigManager
from data.api_schema_data import SubmitResData, GetFormDataResultData
from data.pipeline_schema_data import PipelineFormData
from service.mongo_db_handler import MongoDbHandler
from .pipeline_base import *

app_config = AppConfigManager().get_app_config()

# APIRouter creates path operations for module
router = APIRouter(prefix="/tfstudioservice/api/v1/pipelines",
                   responses={404: {"description": "Not found"}})

# create a form data for the pipeline
@router.post("/formdata", response_model=SubmitResData, tags=["FormData"],
             summary="Creates formdata of an existing pipeline definition", include_in_schema=SHOW_PRIVATE_API)
async def post_form_data(input_form_data: PipelineFormData, userId: Union[str, None] = Header()):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    doc_data = {}
    form_data = input_form_data.dict()
    doc_data['recordId'] = FileUtil.get_uuid()
    doc_data['recordIdName'] = PIPELINE_FORM_DATA_ID
    doc_data['record'] = form_data
    doc_data['createdDtm'] = date_time_stamp
    doc_data['modifiedDtm'] = date_time_stamp
    doc_data['createdBy'] = userId
    doc_data['modifiedBy'] = None
    doc_data['isDeleted'] = False
    inserted_id = mongo_db_handler.insert_document(
        PIPLEINE_FORM_DATA, doc_data)
    if inserted_id:
        insert_response = {"message": "Successfully inserted"}
    elapsed_time = round(time.time() - start_time, 3)
    response = SubmitResData(response=insert_response,
                             responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS,
                             timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))
    return response

# get the form data of a pipeline
@router.get("/formdata/{pipelineId}", response_model=GetFormDataResultData, tags=["FormData"],
            summary="Return the latest formdata detail associated with the pipeline", include_in_schema=SHOW_PRIVATE_API)
async def get_form_data(pipelineId):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    documents = mongo_db_handler.get_documents(
        PIPLEINE_FORM_DATA, {"record.pipelineId": pipelineId}).sort("createdDtm", -1)
    res_list = []
    document_dup = copy.deepcopy(documents)
    if len([i for i in document_dup]) == 0:
        mongo_db_handler.disconnect()
        return GetFormDataResultData(response=[{"message":  "No data found"}],
                                     responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS,
                                     timestamp=date_time_stamp,
                                     responseTimeInSecs=((time.time()-start_time)/1000))
    for document in documents:
        output_dict = document['record']
        res_list.append(output_dict)
        # break
    elapsed_time = round(time.time() - start_time, 3)
    response = GetFormDataResultData(response=res_list,
                                     responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS,
                                     timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))
    return response
