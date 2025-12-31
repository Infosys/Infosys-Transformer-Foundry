# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
from fastapi import APIRouter, File, UploadFile, Header
from fastapi.responses import FileResponse
from common.file_util import FileUtil
from common.app_config_manager import AppConfigManager
from service.mongo_db_handler import MongoDbHandler
from .pipeline_base import *
from common.common_util import CommonUtil

app_config = AppConfigManager().get_app_config()

# APIRouter creates path operations for module
router = APIRouter(prefix="/api/v2/pipelines", responses={404: {"description": "Not found"}})

# To Get the pipeline operator file (e.g., Kubeflow)
@router.get("/operator/file/{pipelineId}", tags=["operator"],
            summary="Get the pipeline operator file (e.g., Kubeflow)", include_in_schema=False)
async def get_result(pipelineId):
    output_response = {}
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    documents = mongo_db_handler.get_documents(
        PIPELINE_OPERATOR, {'record.pipelineId': pipelineId})
    documents = CommonUtil.sort_datalist_by_date(documents, 'createdDtm')
    for document in documents:
        output_response = document['record']
        break
    temp_path = f'{PIPELINE_FOLDER_PATH}/temp'
    FileUtil.create_dirs_if_absent(temp_path)
    file_path = temp_path+'/' + \
        output_response['fileName']+output_response['fileExtension']
    FileUtil.write_to_file(output_response['fileContent'], file_path)
    mongo_db_handler.disconnect()
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))