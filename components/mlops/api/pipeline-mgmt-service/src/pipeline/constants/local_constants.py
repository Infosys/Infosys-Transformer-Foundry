# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: local_constants.py
description: Local constants for usecase  module
"""
from collections import namedtuple
from enum import Enum

LOG_PREFIX = "[ {} ] [ {} ] [ {} ] [ {} ]"
LOG_FORMAT = "{} {}"

Error = namedtuple('Error', ['code', 'message'])
PIPELINSCOPE_ERROR = "Pipeline Scope should be Public/Private"
INPUTMODE_ERROR = "Input Mode should be INFY_AICLD_MINIO/INFY_ALCLD_NUTANIX"
PIPELINE_EXIST_ERROR = "Pipeline with same name and version already exists"
STEPARGUMENTSNOTINJOBARGUEMENT_ERROR = "Step Argument is not in Job Argument"
INVALIDJOBARGUMENTDATATYPE = "Data Type should be of bool/string/int/float only"
JOBSTEPARGUMENTMISMATCH = "Job Argument & Step argument count doesn't match"
PIPELINE_NOT_EXIST = "Pipeline doesn't exist"
RUNARG_LIST_EMPTY = "Run arguments list is empty"
SPECIAL_CHARACTER_FOUND = "Special character found in runArgument name"
RUNARG_MISMATCH = "runArguments are not matching with stepArguments"
INVALID_RUNARG_VALUE = "runArgument argValue is not align with jobArguments dataType"
COMPUTE_TYPE_VALUE = "Type value should be either CPU/GPU"
MAXQTY_VALUE = "maxQty value should be less than 20"
MEMORY_VALUE = "memory value should be between 0 to 16Gi"
MINQTY_VALUE = "minQty value should be more than 1"
INVALID_EXPERIMENTNAME = "experimentConfig name should not contain special character"
TRIAL_ALREADY_EXISTS = "Trial with same name and version already exists"
JENKINS_TRIGGER = "jenkins Trigger got an error"
TRIAL_ID_EMPTY = "Trial Id is empty"
TRIAL_DETAILS_NOT_FOUND = "Trial details not found"
PROJECT_NOT_FOUND = "Project not found"
PIPELINE_NOT_FOUND = "Pipeline not found"
MEMORY_EXCEED = "Input memory is exceeding the quota limits"
MEMORY_NOT_AVAILABLE = "Requested memory configuration is not available"
CURRENTRESOURCEUSAGE = "CurrentResourceUsage is not available"
JENKINSJOBERRORCODE = 2824
MINMAX_QTY = "minQty is more than maxQty"
JOBARGUMENT_SPECIAL_CHARACTER = "Special character found in jobArgument name"
INVALID_VALUE = "Invalid value for memory"
USER_PERMISSION = "user doesn't have permission"
INVALID_VALUE_ARTIFACT = "Invalid value for the Input Artifacts uri"
INVALID_VALUE_OUTPUT_ARTIFACT = "Invalid value for the Output Artifacts uri"
INVALID_VALUE_LOGFILEURI = "Invalid value for Log File Uri"
INVALID_JOBARG_DEFAULTVALUE = "Job Argument Default Value not align with jobArguments dataType"
ERROR_OCCURED = "Some Error occurred, Please try again later"

class ErrorCode(Enum):
    PIPELINSCOPE_ERROR = Error(2800, PIPELINSCOPE_ERROR)
    PIPELINE_EXIST_ERROR = Error(2801, PIPELINE_EXIST_ERROR)
    INVALIDJOBARGUMENTDATATYPE_ERROR = Error(2802, INVALIDJOBARGUMENTDATATYPE)
    INPUTMODE_ERROR = Error(2803, INPUTMODE_ERROR)
    STEPARGUMENTSNOTINJOBARGUEMENT = Error(2804, STEPARGUMENTSNOTINJOBARGUEMENT_ERROR)
    JOBSTEPARGUMENTMISMATCH_ERROR = Error(2805, JOBSTEPARGUMENTMISMATCH)
    PIPELINE_NOT_EXIST_ERROR = Error(2806, PIPELINE_NOT_EXIST)
    RUNARG_LIST_EMPTY_ERROR = Error(2807, RUNARG_LIST_EMPTY)
    SPECIAL_CHARACTER_FOUND_ERROR = Error(2808, SPECIAL_CHARACTER_FOUND)
    RUNARG_MISMATCH_ERROR = Error(2809, RUNARG_MISMATCH)
    INVALID_RUNARG_VALUE_ERROR = Error(2810, INVALID_RUNARG_VALUE)
    COMPUTE_TYPE_VALUE_ERROR = Error(2811, COMPUTE_TYPE_VALUE)
    MAXQTY_VALUE_ERROR = Error(2812, MAXQTY_VALUE)
    MEMORY_VALUE_ERROR = Error(2813, MEMORY_VALUE)
    MINQTY_VALUE_ERROR = Error(2814, MINQTY_VALUE)
    INVALID_EXPERIMENTNAME_ERROR = Error(2815, INVALID_EXPERIMENTNAME)
    TRIAL_ALREADY_EXISTS_ERROR = Error(2816, TRIAL_ALREADY_EXISTS)
    JENKINS_TRIGGER_ERROR = Error(2817, JENKINS_TRIGGER)
    TRIAL_ID_EMPTY_ERROR = Error(2818, TRIAL_ID_EMPTY)
    TRIAL_DETAILS_NOT_FOUND_ERROR = Error(2819, TRIAL_DETAILS_NOT_FOUND)
    PROJECT_NOT_FOUND_ERROR = Error(2820, PROJECT_NOT_FOUND)
    MEMORY_EXCEED_ERROR = Error(2821, MEMORY_EXCEED)
    MEMORY_NOT_AVAILABLE_ERROR = Error(2822, MEMORY_NOT_AVAILABLE)
    CURRENTRESOURCEUSAGE_ERROR = Error(2823, CURRENTRESOURCEUSAGE)
    MINMAX_QTY_ERROR = Error(2825, MINMAX_QTY)
    JOBARGUMENT_SPECIAL_CHARACTER_ERROR = Error(2826, JOBARGUMENT_SPECIAL_CHARACTER)
    PIPELINE_NOT_FOUND_ERROR = Error(2826, PIPELINE_NOT_FOUND)
    USER_PERMISSION_ERROR = Error(2827, USER_PERMISSION)
    INVALID_VALUE_ERROR = Error(2827, INVALID_VALUE)
    INVALID_VALUE_ARTIFACT_ERROR = Error(2828, INVALID_VALUE_ARTIFACT)
    INVALID_VALUE_OUTPUT_ARTIFACT_ERROR = Error(2829, INVALID_VALUE_OUTPUT_ARTIFACT)
    INVALID_VALUE_LOGFILEURI_ERROR = Error(2830, INVALID_VALUE_LOGFILEURI)
    INVALID_JOBARG_DEFAULTVALUE_ERROR = Error(2831, INVALID_JOBARG_DEFAULTVALUE)
    ERROR_OCCURED = Error(2832, ERROR_OCCURED)