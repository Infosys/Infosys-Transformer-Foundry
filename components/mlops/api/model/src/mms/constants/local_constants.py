# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: local_constants.py
description: Local constants for model module
"""
from enum import Enum

DEPLOY_MODEL_URL = '/models/deploy'
MODEL_ENDPOINT_URL = '/models/endpoint'
INFERENCE_URL = '/models/inference'
MODEL_URL = '/models'

HTTP_STATUS_FORBIDDEN = 403

DELTED_SUCCESS_MESSAGE="Successfully deleted the model :"
MODEL_ALREADY_EXISTS= "Model with name PLACEHOLDER_TEXT already exists"
MODEL_LIST_NOT_FOUND = "No Models Found"
MODEL_NOT_FOUND_ERROR="Model not found. Model should be registered before deployment"
MODEL_ALREADY_DEPLOYED_ERROR="Model is already Deployed"
COMPUTE_TYPE_REQUIRED_MSG = '1035'
CPU_MEMORY_FORMAT_INVALID_MSG = '1042'
CPU_QTY_FORMAT_INVALID_MSG = '1041'
CPU_MEMORY_REQD_MSG = '1038'
CPU_QTY_REQD_MSG = '1036'
GPU_MEMORY_FORMAT_INVALID_MSG = '1040'
GPU_MEMORY_REQD_MSG = '1039'
GPU_QTY_REQD_MSG = '1054'
CONTAINER_IMAGE_URL_NOTVALID_MSG = 'Container Image URL entered is not valid'

SPACE_DELIMITER=" "
PLACEHOLDER_TEXT="PLACEHOLDER_TEXT"

PROJECT_NOT_FOUND_ERROR = "Project Not Found"
JENKINS_DEPLOYMENT_JOB_FAILED_ERROR = 'Some error occurred while deploying the model. Error details as follows: PLACEHOLDER_TEXT'
DEPLOYMENT_NOTFOUND_ERROR = '1050'

JENKINS_CUSTOM = 'CUSTOM'
JENKINS_TRITON = 'TRITON'
JENKINS_DJL = 'DJL'

HTTP_HEADER_NAME_USERID = 'KUBEFLOW_USERID'
NOT_AUTHORIZED_ERROR = 'Request Not Authorized'

MODEL_STATUS_CREATED = 'CREATED'
MODEL_STATUS_DEPLOYED = 'Deployed'
MODEL_STATUS_DEPLOY_INPROGRESS = 'DEP_INPROGRESS'
MODEL_STATUS_INPROGRESS = 'INPROGRESS'
MODEL_STATUS_FAILED = 'FAILED'

JOB_STATUS_SUCCESS = 'SUCCESS'
JOB_STATUS_FAILURE = 'FAILURE'
JOB_STATUS_INPROGRESS = 'INPROGRESS'

DEPLOYMENT_STATUS_SUCCESS = 'Deployed'
DEPLOYMENT_STATUS_FAILURE = 'FAILED'
DEPLOYMENT_STATUS_INPROGRESS = 'InProgress'

HTTP_RESPONSE_STATUS_SUCCESS = 'SUCCESS'
HTTP_RESPONSE_STATUS_FAILED = 'FAILURE'

GPU_QUOTA_EXCEED_ERROR_MSG = 'GPU cannot be allocated as your User/Project quota exceeded the limit.'
CPU_QUOTA_EXCEED_ERROR_MSG = 'CPU cannot be allocated as your User/Project quota exceeded the limit.'
CPUMEMORY_QUOTA_EXCEED_ERROR_MSG = 'CPU Memory cannot be allocated as your User/Project quota exceeded the limit.'

USER_PERMISSION_DEPLOYMODEL = 'deployModel'
USER_PERMISSION_VIEW = 'view'

JENKINSJOBERRORCODE = '3623'
DELETE_MODEL = 'delete_model'


#Dict of error codes and its error message.
errorCodeMsgDict = {
    '1002': 'Project not found'
    }


