# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from enum import Enum
from collections import namedtuple

ErrorNT = namedtuple('Error', ['code', 'message'])


class ErrorCode(Enum):
    MAX_QTY_LESS_THAN_MIN_QTY = ErrorNT(
        1001, 'maxQty must be not be less than minQty')
    COMPUTE_TYPE_VALUES_ALLOWED = ErrorNT(
        1002, 'Computes Type allowed values are CPU,GPU')
    GPU_NOT_ALLOWED = ErrorNT(1003, 'GPU is not supported as of now')
    STEP_ARGUMENT_EMPTY_STRING_NOT_ALLOWED = ErrorNT(
        1004, 'Empty strings not allowed for stepArguments')
    IMAGE_URI_EMPTY_STRING_NOT_ALLOWED = ErrorNT(
        1005, 'Empty strings not allowed for imageUri')
    STORAGE_TYPE_EMPTY_NOT_ALLOWED = ErrorNT(
        1006, 'storageType must not be empty')
    STORAGE_TYPE_VALUES_ALLOWED = ErrorNT(
        1007, 'Storage Type allowed values are MINIO, NUTANIX')
    STORAGE_INVALID_URI = ErrorNT(
        1008, 'Invalid uri')
    STORAGE_MEMORY = ErrorNT(
        1009, 'Storage Memory should be in GB')
    PIPELINE_NAME_MANDATORY = ErrorNT(
        1010, 'Pipeline name is madatory')
    PIPELINE_OPERATOR_VALUES_ALLOWED = ErrorNT(
        1011, 'Operator allowed values are kubeflow,airflow')
    PIPELINE_RUNTIME_VALUES_ALLOWED = ErrorNT(
        1012, 'Runtime allowed values are kubernetes, VM')
