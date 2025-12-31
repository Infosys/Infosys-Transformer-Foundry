# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: exception.py
description: handles project module specific exception
""" 
  
import projects.constants.local_constants  as constant
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel,ApiResponse
from abc import ABC
from fastapi.encoders import jsonable_encoder

class projectException(Exception, ABC):
    """
    dscription: Abstract base class of projectException.
    """
    def __init__(self, status_code: int, detail: str) -> None:         
        super().__init__(status_code)
        super().__init__(detail) 
    
class exception(projectException):
    """
    description: Exption will be thrown by project service :                 
    """
    def __init__(self,code,message):
        self.status_code = HTTP_422_UNPROCESSABLE_ENTITY            
        apierrResp = ApiErrorResponseModel(code=code, status="FAILURE", message=message)
        self.detail =  jsonable_encoder(apierrResp)