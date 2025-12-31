# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from enum import Enum
from collections import namedtuple

ErrorNT = namedtuple('Error', ['code', 'message'])

class ErrorCode(Enum):
    MAX_QTY_LESS_THAN_MIN_QTY = ErrorNT(1001, 'maxQty must be not be less than minQty')
    COMPUTE_TYPE_VALUES_ALLOWED = ErrorNT(1002, 'Computes Type allowed values are CPU,GPU')
    GPU_NOT_ALLOWED = ErrorNT(1003, 'GPU is not supported as of now')
    STEP_ARGUMENT_EMPTY_STRING_NOT_ALLOWED = ErrorNT(1004, 'Empty strings not allowed for stepArguments')
    IMAGE_URI_EMPTY_STRING_NOT_ALLOWED = ErrorNT(1005, 'Empty strings not allowed for imageUri')
    STORAGE_TYPE_EMPTY_NOT_ALLOWED = ErrorNT(1006, 'storageType must not be empty')
    STORAGE_TYPE_VALUES_ALLOWED = ErrorNT(1007, 'Storage Type allowed values are INFY_AICLD_MINIO, INFY_AICLD_NUTANIX')
    STORAGE_INVALID_URI = ErrorNT(1008, 'Invalid uri')
    STORAGE_MEMORY = ErrorNT(1009, 'Storage Memory should be in GB')
    PIPELINE_NAME_MANDATORY = ErrorNT(1010, 'Pipeline name is madatory')
    PIPELINE_OPERATOR_VALUES_ALLOWED = ErrorNT(1011, 'Operator allowed value is only kubeflow and airflow')
    PIPELINE_RUNTIME_VALUES_ALLOWED = ErrorNT(1012, 'Runtime allowed values are kubernetes, VM')
    FLOW_STEP_NAME = ErrorNT(1014, 'step names should be alphanumeric and -(hypen)')
    PIPELINE_NAME_ACCEPTS = ErrorNT(1016, 'Pipeline name should be in smaller case and can accept only a-z, -, numbers e.g my-pipeline-testing-001')
    PIPELINE_INPUTARTIFACTS = ErrorNT(1017, 'Input Artifacts should not be empty')
    GPU_MEMORY = ErrorNT(1018, 'GPU memory should be 20GB')
    GPU_MAXQTY = ErrorNT(1019, 'GPU maxqty should be 1')
    GPU_MINQTY = ErrorNT(1019, 'GPU minqty should be 1')
    DEPENDS_ON = ErrorNT(1020, 'Task is not available. Please enter valid task')
    PIPELINE_VOLUMESIZEINGB = ErrorNT(1021, 'VolumeSizeinGB should be integer')
    VOLUME_SCOPE = ErrorNT(1022, 'SizeinGB is mandatory field for pipeline')
    PROJECT_ID_ERROR = ErrorNT(1023, 'Project Id should not be empty')
    NAME_VERSION = ErrorNT(1024, 'Pipeline name or version should be unique')
    VOLUME_SCOPE_ERROR = ErrorNT(1025, 'volume.scope should be pipeline or platform')
    PROJECT_NOT_FOUND = ErrorNT(1026,'Project Details Not Found')
    TENANT_NOT_FOUND = ErrorNT(1027,'Tenant not found')
    INVALID_COMPUTE_TYPE = ErrorNT(1028,'Invalid ComputeType')
    VOLUME_QUOTA_EXCEEDED = ErrorNT(1029,'Volume quota exceeded')
    GPU_QUOTA_EXCEEDED = ErrorNT(1030,'GPU quota exceeded')
    CPU_QUOTA_EXCEEDED = ErrorNT(1031,'CPU quota exceeded')
    MEMORY_QUOTA_EXCEEDED = ErrorNT(1032,'Memory quota exceeded')
    SUCCESS = ErrorNT(1033,'Success')
    AIRFLOW_ERROR =  ErrorNT(1034,"Airflow currently not supported")
    VM_ERROR = ErrorNT(1035, "vm currently not supported")
    FLOW_STEP_NAME_ERROR = ErrorNT(1036, 'step names should not be empty')