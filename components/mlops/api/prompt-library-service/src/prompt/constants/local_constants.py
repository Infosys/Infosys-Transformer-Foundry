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
from collections import namedtuple

Error = namedtuple('Error', ['code', 'message'])
HTTP_RESPONSE_STATUS_SUCCESS = 'SUCCESS'
HTTP_RESPONSE_STATUS_FAILED = 'FAILURE'
GLOBAL_USER_ID = "xyz@abc.com"
ROLE_LIST = ["user", "system", "assistant"]
MODE_LIST = ["text", "chat"]
MODEL_MAX_LEN = 30

PROJECT_NOT_FOUND = "Invalid Project Id / Project not found"
DEPLOYMENT_NOT_FOUND="No deployments found for this model"
EMPTY_CONVERSATION_CONTENT = "Conversation content should not be empty"
EMPTY_CONVERSATION_ROLE = "Conversation role should not be empty"
ROLE_LIST_INVALID = "conversation role should be user or system or assistant"
MODE_LIST_INVALID = "mode should be text or chat"
PROMPT_NOT_FOUND = "Prompt ID not found / Invalid Prompt ID"
PROMPT_NAME_EMPTY= "name  field should not be empty"
MODEL_NAME_EMPTY = "Model name should not be empty"
PROMPT_NAME_SPECIAL_CHAR = "Name should not contain special characters"
MODE_EMPTY = "Mode should not be empty"
MODEL_NAME_SPECIAL_CHAR = "Model name should not contain special characters"
NAME_MAX_LEN = "Name should not exceed 15 characters"
PARAMETER_REQUIRED = "Parameters is required"
EMPTY_PARAMETER_KEY = "Parameter key should not be empty"
EMPTY_PARAMETER_VALUE = "Parameter value should not be empty"
PROMPT_NAME_UPDATE = "Prompt name updation not allowed"
PROMPT_ID_REQUIRED = "Prompt ID is required"
NAME_MAX_LEN = "Name should not exceed 30 characters"
MODEL_NAME_MAX_LENGTH = "Model name should not exceed 30 characters"
MODEL_ID_REQUIRED = "Model ID is required"
EMPTY_USECASE = "Purpose should not be empty"
EMPTY_DOMAIN = "Domain should not be empty"
DOMAIN_MUST_BE_LIST_OF_STRINGS = "Domain must be a list of strings"


class ErrorMessageCode(Enum):
    PROJECT_NOT_FOUND_ERROR = Error(2500, PROJECT_NOT_FOUND)
    DEPLOYMENT_NOT_FOUND_ERROR = Error(2501, DEPLOYMENT_NOT_FOUND )
    EMPTY_CONVERSATION_CONTENT_ERROR = Error(2502, EMPTY_CONVERSATION_CONTENT)
    EMPTY_CONVERSATION_ROLE_ERROR = Error(2503, EMPTY_CONVERSATION_ROLE)
    ROLE_LIST_INVALID_ERROR = Error(2504, ROLE_LIST_INVALID)
    INVALID_MODE_ERROR = Error(2505, MODE_LIST_INVALID)
    PROMPT_NOT_FOUND_ERROR = Error(2506, PROMPT_NOT_FOUND)
    EMPTY_PROMPT_NAME_ERROR = Error(2507, PROMPT_NAME_EMPTY)
    EMPTY_MODEL_NAME_ERROR = Error(2508, MODEL_NAME_EMPTY)
    PROMPT_NAME_SPECIAL_CHAR_ERROR = Error(2509, PROMPT_NAME_SPECIAL_CHAR)
    MODE_EMPTY_ERROR = Error(2510, MODE_EMPTY)
    MODEL_NAME_SPECIAL_CHAR_ERROR = Error(2511, MODEL_NAME_SPECIAL_CHAR)
    NAME_MAX_LENGTH_ERROR = Error(2512, NAME_MAX_LEN)
    PARAMETER_REQUIRED_ERROR = Error(2513, PARAMETER_REQUIRED)
    EMPTY_PARAMETER_KEY_ERROR = Error(2514, EMPTY_PARAMETER_KEY)
    EMPTY_PARAMETER_VALUE_ERROR = Error(2515, EMPTY_PARAMETER_VALUE)
    PROMPT_NAME_UPDATE_ERROR = Error(2516, PROMPT_NAME_UPDATE)
    PROMPT_ID_REQUIRED_ERROR = Error(2517, PROMPT_ID_REQUIRED)
    NAME_MAX_LENGTH_ERR = Error(2518, NAME_MAX_LEN)
    MODEL_NAME_MAX_LENGTH_ERR = Error(2519, MODEL_NAME_MAX_LENGTH)
    MODEL_ID_REQUIRED_ERROR = Error(2520, MODEL_ID_REQUIRED)
    EMPTY_USECASE_ERROR = Error(2521, EMPTY_USECASE )
    EMPTY_DOMAIN_ERROR = Error(2522, EMPTY_DOMAIN)
    DOMAIN_MUST_BE_LIST_OF_STRINGS_ERROR = Error(2523, DOMAIN_MUST_BE_LIST_OF_STRINGS)