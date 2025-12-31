# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: exception.py
description: handles model module specific exception
"""
from fastapi.encoders import jsonable_encoder
from prompt.constants.local_constants  import *
from abc import ABC
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel

class ModelStatusException(Exception, ABC):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code)
        super().__init__(detail)

class InvalidValueError(ModelStatusException):
    def __init__(self, error_detail):
        self.status_code = HTTP_STATUS_BAD_REQUEST
        api_err_resp = ApiErrorResponseModel(code=error_detail.value.code, status="FAILURE", message=error_detail.value.message)
        self.detail = jsonable_encoder(api_err_resp)