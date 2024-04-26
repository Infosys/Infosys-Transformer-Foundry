# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
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
VERSION_TYPE_ERROR = "modelVersion must be an digit"

#benchmark
PIPELINE_NAME_ERROR = "Pipeline name should be unique"
INVALID_DATA_MODEL_INPUT_ERROR = "data filed have only one entry"
PIPELINE_NAME = "Pipeline name should not be empty"
BENCHMARK_NOT_FOUND_ERROR = "Benchmark not found"
NAME_SPECIAL_CHAR_ERROR = "name field accepts only alphabets ,hyphen and numbers."
MODEL_DATASET_EMPTY_ERROR = "please enter either modelName or datasetName"

TASK_NOT_FOUND_ERROR="Task not found"
CODE_METRIC_ERROR = "metric name is not applicable for code modality"
TEXT_METRIC_ERROR = "metric name is not applicable for text modality"
EMBEDDING_METRIC_ERROR = "metric name is not applicable for embedding modality"


BENCHMARK_TYPE_REQUIRED = "Type should not be empty"
BENCHMARK_TYPE_VALUE_ERROR="BenchmarkType should be either code, text or embedding"
BENCHMARK_CONFIG_EMPTY_ERROR="Benchmarkconfig should not be empty"
MODEL_EMPTY_ERROR="Model should not be empty"
MODEL_PATH_OR_ID_EMPTY_ERROR="Model Path or Id should not be empty"
QUANTIZEMETHOD_EMPTY_ERROR="Quantized Method should not be empty"
ARGS_EMPTY_ERROR="Args should not be empty"
VALUE_EMPTY_ERROR="Value should not be empty"
DATA_EMPTY_ERROR="Dataset field should not be empty"
SCOPE_EMPTY_ERROR="Scope should not be empty"
LANGUAGE_EMPTY_ERROR="Language should not be empty"
BATCHSIZE_EMPTY_ERROR="Batchsize should not be empty"
LIMIT_EMPTY_ERROR="Limit should not be empty"
TASK_EMPTY_ERROR="Task should not be empty"
DATASTORAGE_EMPTY_ERROR="Datastorage should not be empty"
GPU_QUANTITY_NOT_EMPTY="GPU quantity should not be empty"
MOUNTPATH_EMPTY_ERROR="Mount path should not be empty"
SIZE_NOT_EMPTY_ERROR = "Size should not be empty"
MODEL_NAME_EMPTY_ERROR="Model name should not be empty"
MODEL_PATH_URI_ERROR="model path uri should start with s3://"
BENCHMARK_DATA_TYPE_ERROR="Data type should be int4, int8, fp16"
QUANTIZEMETHOD_VALUES_ERROR = "Quantize method value should be static, dynamic and N"
MODEL_ARGUMENT_NAME_ERROR = "model argument name should not be empty"
MODEL_ARGUMENT_VALUE_ERROR = "model arument value should not be empty"
GPU_MEMORY_ERROR = "GPU memory should be 20GB, 40GB or 80GB"
DATASTORAGE_URI_EMPTY_ERROR = "Data Storage URI should start with s3://"
VOLUMEN_NAME_ERROR = "Volume name should not be empty"
VOLUME_PATH_ERROR="Volume path should be start with /"
BENCHMARK_MODEL_NAME_SPECIAL_CHARS_ERROR = "model name should accepts only alphabets, hyphen and numbers."
SCOPE_VALUE_ERROR="scope should be either public or private"
BATCHSIZE_VALUE_ERROR = "Batchsize value should be between 1 to 50"
LIMIT_VALUE_ERROR = "Limit value should be between 1 to 15000"
SIZEINGB_VALUE_ERROR = "sizeinGB value should be between 1 to 100"
QUANTIZEMETHOD_VALUE_ERROR_FP = "datatype fp16 and fp32 quantizeMethod value should be 'n'."
QUANTIZEMETHOD_VALUE_ERROR_INT = "datatype int4 and int8 quantizeMethod value should be 'static' and 'dynamic'."
BENCHMARK_TYPE_VALUES ="('code','text','embedding')"
BENCHMARK_DATA_TYPE_VALUES ="('fp4','fp8','fp16','fp32')"
QUANTIZEMETHOD_VALUES ="('static','dynamic','na')"
NAME_MAX_LENGTH=40
MODEL_NAME_MAX_LENGTH=15

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
    VERSION_TYPE_ERROR = Error(2832, VERSION_TYPE_ERROR)

    #bechmark
    INVALID_DATA_MODEL_INPUT_ERROR = Error(2833, INVALID_DATA_MODEL_INPUT_ERROR)
    PIPELINE_NAME = Error(2834, PIPELINE_NAME)
    BENCHMARK_NOT_FOUND_ERROR = Error(2835, BENCHMARK_NOT_FOUND_ERROR)
    TASK_NOT_FOUND_ERROR=Error(2836,TASK_NOT_FOUND_ERROR)
    NAME_SPECIAL_CHAR_ERROR = Error(2837,NAME_SPECIAL_CHAR_ERROR)
    PIPELINE_NAME_ERROR = Error(2838, PIPELINE_NAME_ERROR)
    MODEL_DATASET_EMPTY_ERROR = Error(2839,MODEL_DATASET_EMPTY_ERROR)
    CODE_METRIC_ERROR = Error(2840,CODE_METRIC_ERROR)
    TEXT_METRIC_ERROR = Error(2841,TEXT_METRIC_ERROR)
    EMBEDDING_METRIC_ERROR = Error(2842, EMBEDDING_METRIC_ERROR)

    BENCHMARK_TYPE_REQUIRED=Error(2529,BENCHMARK_TYPE_REQUIRED)
    BENCHMARK_TYPE_VALUE_ERROR=Error(2530,BENCHMARK_TYPE_VALUE_ERROR)
    BENCHMARK_CONFIG_EMPTY_ERROR=Error(2531,BENCHMARK_CONFIG_EMPTY_ERROR)
    MODEL_EMPTY_ERROR=Error(2532,MODEL_EMPTY_ERROR)
    MODEL_PATH_OR_ID_EMPTY_ERROR=Error(2533,MODEL_PATH_OR_ID_EMPTY_ERROR)
    QUANTIZEMETHOD_EMPTY_ERROR=Error(2534,QUANTIZEMETHOD_EMPTY_ERROR)
    ARGS_EMPTY_ERROR=Error(2535, ARGS_EMPTY_ERROR)
    VALUE_EMPTY_ERROR=Error(2536, VALUE_EMPTY_ERROR)
    DATA_EMPTY_ERROR=Error(2537,  DATA_EMPTY_ERROR)
    SCOPE_EMPTY_ERROR=Error(2538, SCOPE_EMPTY_ERROR)
    LANGUAGE_EMPTY_ERROR=Error(2539, LANGUAGE_EMPTY_ERROR)
    BATCHSIZE_EMPTY_ERROR=Error(2539, BATCHSIZE_EMPTY_ERROR)
    LIMIT_EMPTY_ERROR=Error(2540, LIMIT_EMPTY_ERROR)
    TASK_EMPTY_ERROR=Error(2541, TASK_EMPTY_ERROR)
    DATASTORAGE_EMPTY_ERROR=Error(2542, DATASTORAGE_EMPTY_ERROR)
    GPU_QUANTITY_NOT_EMPTY=Error(2543,GPU_QUANTITY_NOT_EMPTY)
    MOUNTPATH_EMPTY_ERROR=Error(2544,MOUNTPATH_EMPTY_ERROR)
    SIZE_NOT_EMPTY_ERROR=Error(2545,SIZE_NOT_EMPTY_ERROR)
    MODEL_NAME_EMPTY_ERROR=Error(2546,MODEL_NAME_EMPTY_ERROR)
    MODEL_PATH_URI_ERROR=Error(2547,MODEL_PATH_URI_ERROR)
    BENCHMARK_DATA_TYPE_ERROR=Error(2548,BENCHMARK_DATA_TYPE_ERROR)
    QUANTIZEMETHOD_VALUES_ERROR=Error(2549,QUANTIZEMETHOD_VALUES_ERROR)
    MODEL_ARGUMENT_NAME_ERROR=Error(2550,MODEL_ARGUMENT_NAME_ERROR)
    MODEL_ARGUMENT_VALUE_ERROR=Error(2551,MODEL_ARGUMENT_VALUE_ERROR)
    DATASTORAGE_URI_EMPTY_ERROR=Error(2552,DATASTORAGE_URI_EMPTY_ERROR)
    GPU_MEMORY_ERROR = Error(2553,GPU_MEMORY_ERROR)
    VOLUMEN_NAME_ERROR=Error(2554,VOLUMEN_NAME_ERROR)
    VOLUME_PATH_ERROR=Error(2555,VOLUME_PATH_ERROR)
    BENCHMARK_MODEL_NAME_SPECIAL_CHARS_ERROR = Error(2556,BENCHMARK_MODEL_NAME_SPECIAL_CHARS_ERROR)
    SCOPE_VALUE_ERROR=Error(2557,SCOPE_VALUE_ERROR)
    BATCHSIZE_VALUE_ERROR = Error(2558,BATCHSIZE_VALUE_ERROR)
    LIMIT_VALUE_ERROR = Error(2559,LIMIT_VALUE_ERROR)
    SIZEINGB_VALUE_ERROR = Error(2560,SIZEINGB_VALUE_ERROR)
    QUANTIZEMETHOD_VALUE_ERROR_FP = Error(2561,QUANTIZEMETHOD_VALUE_ERROR_FP)
    QUANTIZEMETHOD_VALUE_ERROR_INT = Error(2562,QUANTIZEMETHOD_VALUE_ERROR_INT)