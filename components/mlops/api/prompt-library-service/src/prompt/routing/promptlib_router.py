# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import logging
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, Header, Response, Query
from aicloudlibs.schemas.global_schema import *
from aicloudlibs.exceptions.global_exception import *
from prompt.service.promptlib_service import PromptLibraryService
from prompt.constants.local_constants import *
from prompt.exception.exception import *
from prompt.util.log_formatter import LogFormatter
from prompt.mappers.prompt_mapper import PromptRequest, UpdatePromptRequest

router = APIRouter()
log_formatter = LogFormatter('Prompt Library Management')

@router.post("/prompt",response_model=ApiResponse)
def create_new_prompt( request: Request, response: Response, user_id: str = Header(..., alias='userId'), body: PromptRequest = ...):
    """ create a prompt record in the database """
    try:
        logP: dict = {'apiName': '/api/v1/library'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START create_new_prompt==%s',user_id)
        promptLibrary = PromptLibraryService(request.app, customlog, user_id)
        prompt = promptLibrary.createPrompt(body)
        return ApiResponse(data=prompt)
    
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except BusinessException as be:
        raise HTTPException(**be.__dict__)
    except InternalServerException as ise:
        raise HTTPException(**ise.__dict__)
    

@router.get("/prompt",response_model=ApiResponse)
def list_prompts( request: Request, response: Response, user_id: str = Header(..., alias='userId')):
    """ list all the prompt records """
    try:
        logP: dict = {'apiName': '/api/v1/library'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START list_prompts==%s',user_id)
        promptLibrary = PromptLibraryService(request.app, customlog, user_id)
        prompt = promptLibrary.getAllPrompt()
        return ApiResponse(data={"Prompt List":prompt})
    
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except BusinessException as be:
        raise HTTPException(**be.__dict__)
    except InternalServerException as ise:
        raise HTTPException(**ise.__dict__)
    
@router.get("/prompt/id",response_model=ApiResponse)
def get_prompt_by_id( request: Request, response: Response, user_id: str = Header(..., alias='userId'),  prompt_id: str = Query(..., alias='promptId')):
    """ get a prompt record by id """
    try:
        logP: dict = {'apiName': '/api/v1/library'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START get_prompt_by_id==%s',user_id)
        promptLibrary = PromptLibraryService(request.app, customlog, user_id)
        prompt = promptLibrary.getPromptById(prompt_id)
        return ApiResponse(data=prompt)
    
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except BusinessException as be:
        raise HTTPException(**be.__dict__)
    except InternalServerException as ise:
        raise HTTPException(**ise.__dict__)
    
@router.put("/prompt",response_model=ApiResponse)
def update_prompt( request: Request, response: Response, user_id: str = Header(..., alias='userId'),    body: UpdatePromptRequest = ...):
    """ update a prompt record in the database """
    try:
        logP: dict = {'apiName': '/api/v1/library'}
        customlog = logging.LoggerAdapter(request.app.logger, logP)
        customlog.debug('START getEndpoint==%s',user_id)
        promptLibrary = PromptLibraryService(request.app, customlog, user_id)
        updatedPrompt = promptLibrary.updatePrompt(body)
        return ApiResponse(data=updatedPrompt)
    
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except BusinessException as be:
        raise HTTPException(**be.__dict__)
    except InternalServerException as ise:
        raise HTTPException(**ise.__dict__)