# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import urllib
from common.app_config_manager import AppConfigManager
from service.mongo_db_handler import MongoDbHandler

app_config = AppConfigManager().get_app_config()

DATA_ROOT_PATH = app_config['DEFAULT']['DATA_ROOT_PATH']
PIPELINE_FOLDER_PATH = app_config['STORAGE']['local_storage_path']
PIPELINE_COLLECTION = app_config['STORAGE']['pipeline_collection']
PIPELINE_EXECUTION = app_config['STORAGE']['pipeline_execution']
PIPLEINE_FORM_DATA = app_config['STORAGE']['pipeline_form_data']
PIPELINE_OPERATOR = app_config['STORAGE']['pipeline_operator']
JENKIN_RUN_JOB = app_config['STORAGE']['idp_job_details']
PROJECT = app_config['STORAGE']['project']
SHOW_PRIVATE_API = True if app_config['STORAGE']['show_private_api'] == 'True' else False
TRIGGER_JENKIN = True if app_config['JENKIN']['jenkin_trigger'] == 'True' else False
CONFIG_DICT = {
    'db_host': os.environ.get('DB_HOST'),
    'db_port': os.environ.get('DB_PORT'),
    'db_name': os.environ.get('DB_NAME'),
    'db_username': os.environ.get('DB_USERNAME'),
    'db_password': urllib.parse.quote(os.environ.get('DB_PASSWORD'))
}
KUBEFLOW_CONFIG_DICT = {
    'authentication_url': os.environ.get('KFP_AUTHENTICATION_URL'),
    'url': os.environ.get('KFP_URL')
}
PIPELINE_ID = "pipelineId"
EXECUTION_ID = "executionId"
PIPELINE_OPERATOR_ID = "pipelineOperatorId"
PIPELINE_FORM_DATA_ID = "formdataId"
STATUS_DICT = {1: "Triggered", 2: "Running", 3: "Failed", 9: "Success"}
API_RESPONSE_CDE_FAILURE = 999
API_RESPONSE_MSG_FAILURE = "Failure"
API_RESPONSE_CDE_SUCCESS = 0
API_RESPONSE_MSG_SUCCESS = "Success"
MLOPS_SERVICES = ["createPipeline", "executePipeline", "view"]
CREATEPIPELINE = "createPipeline"
EXECUTEPIPELINE = "executePipeline"
VIEW = "view"

# Function to check the access
def hasAccess(userId, projectId, serviceName):
    have_access = False
    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    project_details = mongo_db_handler.get_document(
        PROJECT, {'id': projectId})
    if not project_details:
        return have_access
    if len(serviceName) > 0 and serviceName in MLOPS_SERVICES:
        if project_details['createdBy'] == userId:
            have_access = True
        else:
            user_list = project_details['userLists']
            if user_list:
                for user in user_list:
                    if userId == user['userEmail']:
                        user_permission = user['permissions']
                        if user_permission and (user_permission.get(serviceName, False) == True or
                                                user_permission.get('workspaceAdmin', False) == True):
                            have_access = True
                            break
    return have_access