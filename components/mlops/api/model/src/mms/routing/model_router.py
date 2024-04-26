# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import logging
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, status, Header, Response, Query, Path
from typing import Union, List, Any
from mms.service.model_service import *
from aicloudlibs.schemas.global_schema import *
from aicloudlibs.exceptions.global_exception import *
import aicloudlibs.constants.http_status_codes as code
import aicloudlibs.constants.error_constants as status
from mms.exception.exception import *

router = APIRouter()

#To get the list of model associated with the given project as an list.
@router.get('/models',response_model= ApiResponse,status_code=code.HTTP_STATUS_OK)
def listModels(request: Request, response: Response,project_id: str = Query(..., alias='projectId'),user_id: str = Header(..., alias='userId')):

    try:
        logP: dict = {'apiName': '/api/v1/models'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START list_models')
        modelService = ModelService(request.app, customlog, user_id)
        modelList = modelService.getAllModels(project_id)
        apiResp = ApiResponse(code=code.HTTP_STATUS_OK, status=status.SUCCESS_STATUS_MESSAGE,data={'models':modelList})
        response.status_code = code.HTTP_STATUS_OK

        return apiResp
    
    except ModelException as modelException:
        logP.error(modelException.__dict__)
        raise HTTPException(**modelException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


