# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
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

class DeployFramework(str, Enum) :
    MODEL_CUSTOM = 'CUSTOM'
    MODEL_TRITON = 'TRITON'

#Dict of error codes and its error message.
errorCodeMsgDict = {
    '1001': 'Use case not found',
    '1002': 'Project not found',
    '1010': 'No Model details found',
    '1011': 'Model not found. Model should be registered before deployment',
    '1012': 'Deployment name field required in input payload',
    '1013': 'Deployment Version field required in input payload',
    '1014': 'Input Mode field required in input payload',
    '1015': 'Input Mode Value is Invalid',
    '1016': 'Source Directory field required in input payload',
    '1017': 'Source Directory value should be either Ai cloud S3 URL or Infosys GitHub URL',
    '1018': 'Not able to access Source Directory',
    '1019': 'S3 URL should be AI Cloud S3 URL. Refer Wiki for details',
    '1020': 'Inference Framework field required in input payload',
    '1021': 'Inference Framework value should be either Flask, Fast API, Django, Python, Pytorch, Tensorflow',
    '1022': 'Inference Specification field required in input payload',
    '1023': 'Docker field required in input payload',
    '1024': 'Api detail Specification field required in input payload',
    '1025': 'Deploy config field required in input payload',
    '1026': 'Dockerfile not found',
    '1027': 'Container port field required in input payload',
    '1028': 'Api route path field required in input payload',
    '1029': 'Api route path value should not be root (\'/\').',
    '1030': 'Environment Name field required in input payload',
    '1031': 'Environment value field required in input payload',
    '1032': 'Container Port should be integer value',
    '1033': 'Model name should not be empty.',
    '1034': 'Compute type field required in input payload',
    '1035': 'Compute type should be either CPU or GPU',
    '1036': 'CPU Qty field required in input payload',
    '1037': 'Currently the requested infra not available. Please try later',
    '1038': 'CPU Memory field required in input payload',
    '1039': 'GPU memory field required in input payload',
    '1040': 'GPU memory should be either 5gb or 20gb or 40gb',
    '1041': 'CPU value should be string, example 5m,4',
    '1042': 'Memory value should be string, example 8Gi,4Gi',
    '1043': 'Some error occurred while building the container image. Error details as follows: <Jenkins job error details >',
    '1044': 'Some error occurred while pushing the container image. Error details as follows: <Jenkins job error details >',
    '1045': 'Some error occurred while deploying the model. Error details as follows: PLACEHOLDER_TEXT',
    '1046': 'Model with same name and version already exists. ',
    '1047': 'Model name should not exceed 15 characters.',
    '1048': 'Deployment name should not exceed 16 characters.',
    '1049': 'Model is already Deployed',
    '1050': 'Deployment (PLACEHOLDER_TEXT) Details not Found',
    '1051': 'Dependency Repo Type field required in input payload',
    '1052': 'Dependency Repo Type value is not Valid',
    '1053': 'Model Version field required in input payload',
    '1054': 'GPU Qty field required in input payload',
    '1055': 'Repo Type value is not Valid',
    '1056': 'Repo Path should be valid S3 URL',
    '1057': 'Model Config Type field should have value as Triton or Deepstream',
    '1058': 'Log Level field should have valid values. e.g., warn, info, etc.',
    '1059': 'Triton Config details should be present in case Model config type is Triton',
    '1060': 'Container Image URL entered is not valid',
    '1061': 'Max Batch Size field required in input payload',
    '1062': 'Batch Max Queue Delay field required in input payload',
    '1063': 'Max Batch Size should be integer value',
    '1064': 'Batch Max Queue Delay should be integer value',
    '1065': 'Model name with same version already exists',
    '1066': 'Input type should be either Text or Image',
    '1067': 'CPU value should not exceed Maximum Limit',
    '1068': 'CPU Memory should not exceed Maximum Limit',
    '1069': 'Storage Type field required in input payload',
    '1070': 'Storage Type value is not Valid',
    '1071': 'User Resource Quota exceeded : PLACEHOLDER_TEXT',
    '1072': 'GPU value should not exceed Maximum Limit',
    '1073': 'Inference Config Json field required in input payload',
    '1074': 'Models field required in input payload',
    '1075': 'Deployment Metadata field required in input payload',
    '1076': 'Name field required in Models Object in input payload',
    '1077': 'Model Name field required in Input Payload',
    '1078': 'Model Type field required in Input Payload',
    '1079': 'Model Framework field required in Input Payload',
    '1080': 'Model Framework Version field required in Input Payload',
    '1081': 'Model Architecture field required in Input Payload',
    '1082': 'GPU fields should not be present for Compute Type CPU',
    '1083': 'PLACEHOLDER_TEXT field required in input payload',
    '1084': 'Container Image field required in input payload',
    '1085': 'Model Deployment is in Progress',
    '1086': 'User is not authorized to deply/update/delete the Model',
    '1087': 'User is not authorized to register/view the Model',
    '1088': 'Deployment Id is required in Input Payload',
    '1089': 'No Models Found',
    '1090': 'Request ID Header field value is required in Input Payload',
    '1091': 'Request Timestamp Header field value is required in Input Payload',
    '1092': 'Sender URI Header field value is required in Input Payload',
    '1093': 'Originator URI Header field value is required in Input Payload',
    '1094': 'User ID Header field value is required in Input Payload',
    '1095': 'Provider Header field value is required in Input Payload',
    '1096': 'Operation Header field value is required in Input Payload',
    '1097': 'Model Name Header field value is required in Input Payload',
    '1098': 'Model Version Header field value is required in Input Payload',
    '1099': 'You are not allowed to deploy the model registered in other projects',
    '1100': 'Deployment with same name and version already exists',
    '1101': 'Deployment Id is not Valid',
    '1102': 'API Route Path cannot be empty',
    '1103': 'Log Level cannot be empty',
    '1104': 'Dependency File Repo Type cannot be empty',
    '1105': 'Dependency File Repo Path cannot be empty',
    '1106': 'User Id field not having valid Email Format',
    '1107': 'Model Type should be of permitted values like CUSTOM, TRITON',
    '1108': 'Deployment Framework should be of permitted values like CUSTOM, TRITON',
    '1109': 'Deployment Framework is required in Header Payload',
    '1110': 'Inference Name is required in Input Payload',
    '1111': 'API Endpoint is required in Input Payload',
    '1112': 'Inference Payload cannot be empty',
    '1113': 'Model Deployment cannot be deleted as it was not successfully deployed',
    '1114': 'Environment Variable Name cannot be empty',
    '1115': 'Environment Variable Value cannot be empty',
    'userId.required': 'User Id is required in Request Header',
    '3600': 'Endpoint Details not found',
    '3601': 'Model already deployed on the endpoint',
    '3602': 'maxQty is greater than minQty',
    '3603' : 'minQty and maxQty should not 0',
    '3604' : 'volumeSizeinGB should be include integer with gb or GB eg:4gb,4GB ',
    '3605' : 'Port value must to be an integer',
    '3607' : 'Please provide valid format for contextUri Eg:/abc',
    '3608' : 'Please provide valid format for predictUri Eg:/abc',
    '3609' : 'Please provide valid format for prefixUri Eg:/abc',
    '3610' : 'Project not found',
    '3611' : 'No Model details found',
    '3612' : 'port field should not be empty',
    '3613' : 'Port name contain http or containerport or http-triton',
    '3614' : 'servingSpec is required for Triton Deployment.',
    '3615' : 'logLevel is required for Triton Deployment.',
    '3616' : 'tritonSpec is required for Triton Deployment.',
    '3617' : 'logLevel should be INFO or WARNING or ERROR.',
    '3618' : 'memory format should be like eg:(20GB or 20gb)',
    '3619' : 'Model Deployment is in Progress',
    '3620' : 'Model not found. Model should be registered before deployment',
    '3621' : 'You are not allowed to deploy the model registered in other projects',
    '3622' : 'Deployment details not found',
    '3624' : 'No Endpoint found for this project ID',
    '3625' : 'Provide a Valid TaskType',
    '3626' : 'port name should not contains uppercase.',
    '3627' : 'Deployment details not found or deployment is inprogress / failed',
    '3628' : 'You cannot override name as it is already configured in trail, Please provide the same.',
    '3629' : 'You cannot override version  as it is already configured in trail, Please provide the same.',
    '3630' : 'You cannot override projectId as it already configured in trial, Please provide the same.',
    '3631' : 'You cannot override storage type as it already configured in trial, Please provide the same.',
    '3632' : 'You cannot override uri as it already configured in trial, Please provide the same.',
    '3633' : 'project ID is required'
    }


taskTypeJson = {'tasktype':{'Text Classification','Token Classification','Table Question Answering','Question Answering','Zero-Shot Classification','Translation','Summarization','Conversational','Text Generation','Text2text Generation','Fill-Mask','Sentence Similarity','Feature Extraction','Text-to-Image','Image-to-Text','Text-to-Video','Visual Question Answering','Document Question Answering','Graph Machine Answering','Text-to-Speech','Automatic Speech Recognition','Audio-to-Audio','Audio Classification','Voice Activity Detection','Depth Estimation','Image Classification','Object Detction','Image Segmentation'}}

taskTypeJsonVal = {'tasktype':{'Natural Language Processing':{'Text Classification','Token Classification','Table Question Answering','Question Answering','Zero-Shot Classification','Translation','Summarization','Conversational','Text Generation','Text2text Generation','Fill-Mask','Sentence Similarity'},'Multimodel':{'Feature Extraction','Text-to-Image','Image-to-Text','Text-to-Video','Visual Question Answering','Document Question Answering','Graph Machine Answering'},'Audio':{'Text-to-Speech','Automatic Speech Recognition','Audio-to-Audio','Audio Classification','Voice Activity Detection'},'Computer Vision':{'Depth Estimation','Image Classification','Object Detction','Image Segmentation'}}}
