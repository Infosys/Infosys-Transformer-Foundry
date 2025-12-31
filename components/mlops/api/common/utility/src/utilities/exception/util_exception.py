# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: util_exception.py
description: handles aicloud utility service exception
"""

import sys, traceback
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel
from fastapi.encoders import jsonable_encoder
from aicloudlibs.constants.http_status_codes import HTTP_STATUS_OK,HTTP_STATUS_NOT_FOUND,HTTP_STATUS_BAD_REQUEST
from abc import ABC

class UtilityServiceException(Exception, ABC):
    """
    dscription: Abstract base class 
    """

    def __init__(self,status_code: int, detail: str) -> None:
        super().__init__(status_code)
        super().__init__(detail)

class JobDetailsNotFoundError(UtilityServiceException):
    def __init__(self,code,message):
        self.status_code = HTTP_STATUS_NOT_FOUND
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)
        
class EndPointDetailsNotFoundError(UtilityServiceException):
    def __init__(self,code,message):
        self.status_code = HTTP_STATUS_NOT_FOUND
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)
        
class DeploymentNotDeletedError(UtilityServiceException):
    def __init__(self,code,message):
        self.status_code = HTTP_STATUS_NOT_FOUND
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE",
                message=message)
        self.detail =  jsonable_encoder(apierrResp)