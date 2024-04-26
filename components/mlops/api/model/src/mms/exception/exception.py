# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: exception.py
description: handles model module specific exception
"""
from fastapi.encoders import jsonable_encoder
from mms.constants.local_constants  import *
from abc import ABC
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel


class ModelException(Exception, ABC):
    """
    dscription: Abstract base class of ModelException.
    """

    def __init__(self, detail: str) -> None:
        self.status_code = HTTP_STATUS_BAD_REQUEST
        self.code = 0
        self.detail = ''
        super().__init__(detail)

class ModelAPIException(Exception, ABC):
    """
    dscription: Abstract base class of ModelAPIException.
    """

    def __init__(self, statusCd:int=422, errCode:int=0, errMsg: str='') -> None:
        self.status_code = statusCd
        self.code = errCode
        self.detail = errMsg
        super().__init__(errMsg)

class ModelAPIJenkinsExceptinon(Exception, ABC):

    def __init__(self, status_code: HTTP_STATUS_BAD_REQUEST, detail: str) -> None:
        super().__init__(status_code)
        super().__init__(detail)        

class ModelAPINotFoundError(ModelException):
    """
    description: ModelListNotFoundError thrown by model service 
                 when the requested model details not found for a specific user.
    """
    def __init__(self, code:str):
        self.code = int(code)
        self.status_code = HTTP_STATUS_NOT_FOUND
        self.detail =  errorCodeMsgDict[code]

class JenkinsDeploymentJobError(ModelException):
    """
    description: JenkinsDeploymentJobError thrown by model service 
                 when the model deployment failed through Jenkins pipeline
    """
    def __init__(self, errCode, errMsg):
        self.code = int(errCode)
        self.status_code = HTTP_STATUS_INTERNAL_SERVER_ERROR
        self.detail =  errorCodeMsgDict[errCode].replace(PLACEHOLDER_TEXT, errMsg)

class DeploymentNotFoundError(ModelException):
    """
    description: JenkinsDeploymentJobError thrown by model service 
                 when the model deployment failed through Jenkins pipeline
    """
    def __init__(self, errCode, errMsg):
        self.code = int(errCode)
        self.status_code = HTTP_STATUS_NOT_FOUND
        self.detail =  errorCodeMsgDict[errCode].replace(PLACEHOLDER_TEXT, errMsg)

class UserResourceQuotaExceedError(ModelException):
    """
    description: JenkinsDeploymentJobError thrown by model service 
                 when the model deployment failed through Jenkins pipeline
    """
    def __init__(self, errCode, errMsg):
        self.code = int(errCode)
        self.status_code = HTTP_STATUS_BAD_REQUEST
        self.detail =  errorCodeMsgDict[errCode].replace(PLACEHOLDER_TEXT, errMsg)

class ModelAPIBusinessError(ModelException):
    """
    description: ModelAPIBusinessError thrown by model service 
                 when the model deployment failed through Jenkins pipeline
    """
    def __init__(self, errCode, errMsg=''):
        self.code = int(errCode)
        self.status_code = HTTP_STATUS_BAD_REQUEST
        self.detail =  errorCodeMsgDict[errCode].replace(PLACEHOLDER_TEXT, errMsg)

class ModelUserAccessError(ModelException):
    """
    description: ModelUserAccessError thrown by model service 
                 when the model deployment failed through Jenkins pipeline
    """
    def __init__(self, errCode):
        self.code = int(errCode)
        self.status_code = HTTP_STATUS_FORBIDDEN
        self.detail =  errorCodeMsgDict[errCode]

class JenkinsJobError(ModelAPIJenkinsExceptinon):

    def __init__(self, error_detail):
        self.status_code = HTTP_STATUS_BAD_REQUEST
        api_err_resp = ApiErrorResponseModel(code=JENKINSJOBERRORCODE, status="FAILURE",
                                             message=error_detail)
        self.detail = jsonable_encoder(api_err_resp) 
        print(self.detail)       
