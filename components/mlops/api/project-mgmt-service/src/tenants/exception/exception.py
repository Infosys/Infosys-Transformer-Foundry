# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: exception.py
description: handles usecase module specific exception
"""  
 
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel
from fastapi.encoders import jsonable_encoder 
from abc import ABC

"""
dscription: Abstract base class of UsecaseException.
"""
class TenantsException(Exception, ABC):
    def __init__(self, status_code: int, detail: str) -> None:
       super().__init__(status_code)
       super().__init__(detail)

class exception(TenantsException):
    """
    description: Exption will be thrown by Tenants service :                 
    """
    def __init__(self,code,message):
        self.status_code = HTTP_422_UNPROCESSABLE_ENTITY            
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE", message=message)
        self.detail =  jsonable_encoder(apierrResp)