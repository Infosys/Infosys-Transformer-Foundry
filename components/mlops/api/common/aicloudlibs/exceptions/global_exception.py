# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import sys, traceback


from abc import ABC
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel
from fastapi.encoders import jsonable_encoder
from aicloudlibs.constants.error_constants import ErrorCode

class MLOpsException(Exception, ABC):
    """
    Abstract base class of all Aicloud exceptions.
    """

    def __init__(self, code: int,message: str) -> None:
        super().__init__(message)
        super().__init__(code)
    


class DbConnectionError(MLOpsException):
  pass

class BusinessException(MLOpsException):
    def __init__(self,code,message):
        self.status_code = HTTP_STATUS_BAD_REQUEST
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)

class NotFoundException(MLOpsException):
    def __init__(self,code,message):
        self.status_code = HTTP_STATUS_NOT_FOUND
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)

class ForbiddenException(MLOpsException):
    def __init__(self):
        self.status_code = HTTP_NOT_AUTHORIZED_ERROR
        error_detail=ErrorCode.NOT_AUTHORIZED_ERROR
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=error_detail.value.message)
        self.detail =  jsonable_encoder(apierrResp)

class InternalServerException(MLOpsException):
    def __init__(self):
        self.status_code = HTTP_STATUS_INTERNAL_SERVER_ERROR
        error_detail=ErrorCode.INTERBAL_SERVER_ERROR
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=error_detail.value.message)
        self.detail =  jsonable_encoder(apierrResp)

class InvalidComputeTypeException(MLOpsException):
     def __init__(self):
        self.status_code = HTTP_STATUS_BAD_REQUEST
        error_detail=ErrorCode.COMPUTE_TYPE_VALUE_ERROR
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=error_detail.value.message)
        self.detail =  jsonable_encoder(apierrResp)

class DiskQuotaException(MLOpsException):
    def __init__(self,total,used):
        self.status_code = HTTP_QUOTA_EXCEED_ERROR
        error_detail=ErrorCode.DISK_QUOTA_ERROR
        message=error_detail.value.message.replace("QUOTALIMIT",str(total))
        message=message.replace("USEDLIMIT",str(used))
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)
        
class GpuQuotaException(MLOpsException):
    def __init__(self,total,used):
        self.status_code = HTTP_QUOTA_EXCEED_ERROR
        error_detail=ErrorCode.GPU_QUOTA_ERROR
        message=error_detail.value.message.replace("QUOTALIMIT",str(total))
        message=message.replace("USEDLIMIT",str(used))
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)

class CpuQuotaException(MLOpsException):
    def __init__(self,total,used):
        self.status_code = HTTP_QUOTA_EXCEED_ERROR
        error_detail=ErrorCode.CPU_QUOTA_ERROR
        message=error_detail.value.message.replace("QUOTALIMIT",str(total))
        message=message.replace("USEDLIMIT",str(used))
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)

class MemoryQuotaException(MLOpsException):
    def __init__(self,total,used):
        self.status_code = HTTP_QUOTA_EXCEED_ERROR
        error_detail=ErrorCode.MEMORY_QUOTA_ERROR
        message=error_detail.value.message.replace("QUOTALIMIT",str(total))
        message=message.replace("USEDLIMIT",str(used))
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)

class QuotaExceedException(MLOpsException):
    def __init__(self):
        self.status_code = HTTP_QUOTA_EXCEED_ERROR
        error_detail=ErrorCode.QUOTA_ERROR
        apierrResp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE",
                message=error_detail.value.message)
        self.detail =  jsonable_encoder(apierrResp)