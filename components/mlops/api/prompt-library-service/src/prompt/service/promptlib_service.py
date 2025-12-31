# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import datetime
import random
from typing import List
from dotenv import dotenv_values
from fastapi import Depends, Request, APIRouter, Cookie, HTTPException, Header, Response, Query
from prompt.mappers.prompt_mapper import PromptResponse, PromptStatusEnum
from prompt.service.common_service import ModelsBaseService, CommonService
from aicloudlibs.exceptions.global_exception import *
from prompt.constants.local_constants import ErrorMessageCode, GLOBAL_USER_ID, ROLE_LIST, MODE_LIST

class PromptLibraryService(ModelsBaseService):

    def __init__(self, app, customlog, userId):
        self.promptcoll = app.database['promptlibrary']
        self.commomService = CommonService(app, customlog, userId)
        self.config = dotenv_values(".env")
        ModelsBaseService.__init__(self, app, customlog, userId)
       
        
    def createPrompt(self, body):
        self.customlog.info("Inside createPrompt")
        try:
            """ Check if the user is authorized to create the prompt """
            if self.loggedUser != GLOBAL_USER_ID:
                raise ForbiddenException()

            """ Check if the project is valid """
            isValidProject = self.commomService.getProjectDetails(body.projectId)
            if not isValidProject:
                raise NotFoundException(ErrorMessageCode.PROJECT_NOT_FOUND_ERROR.value.code, ErrorMessageCode.PROJECT_NOT_FOUND_ERROR.value.message)
            
            """ Validate the input data  for create the prompt """
            
            body.conversationRole = body.conversationRole.lower()
            body.mode = body.mode.lower()

            if body.mode not in MODE_LIST:
                raise BusinessException(ErrorMessageCode.INVALID_MODE_ERROR.value.code, ErrorMessageCode.INVALID_MODE_ERROR.value.message)
            
            if body.mode == "text" and (body.conversationContent == "" or body.conversationContent == None):
                raise BusinessException(ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR.value.code, ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR.value.message)
            
            if body.mode == "chat" and (body.conversationRole == "" or body.conversationRole == None ):
                raise BusinessException(ErrorMessageCode.EMPTY_CONVERSATION_ROLE_ERROR.value.code, ErrorMessageCode.EMPTY_CONVERSATION_ROLE_ERROR.value.message)
            
 
            if body.mode == "chat"  and body.conversationRole not in ROLE_LIST:
                raise BusinessException(ErrorMessageCode.ROLE_LIST_INVALID_ERROR.value.code, ErrorMessageCode.ROLE_LIST_INVALID_ERROR.value.message)
            
            if body.mode == "chat" and (body.conversationContent == "" or body.conversationContent == None):
                raise BusinessException(ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR.value.code, ErrorMessageCode.EMPTY_CONVERSATION_CONTENT_ERROR.value.message)

            
            """ Generate the random prompt id """
            randomPromptId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))

            body.createdBy = self.loggedUser
            body.createdOn = datetime.datetime.utcnow()
            self.customlog.info("Prompt Request: %s", body.dict())   

            promptDict = body.dict()
            promptDict["id"] = randomPromptId
            promptDict["status"] = PromptStatusEnum.Created
            prompt = self.promptcoll.insert_one(promptDict).inserted_id

            promptRespDict = PromptResponse(**promptDict)
            self.customlog.info("Prompt Created: %s", promptRespDict)
            self.customlog.info("End createPrompt")

            return promptRespDict
        
        except NotFoundException as nfe:
            raise HTTPException(**nfe.__dict__)
        except ForbiddenException as fe:
            raise HTTPException(**fe.__dict__)
        except BusinessException as be:
            raise HTTPException(**be.__dict__)
        except Exception as ise:
            self.customlog.error("Exception: %s", ise)
            raise InternalServerException()
    

    def getAllPrompt(self) -> List[PromptResponse]:
        self.customlog.info("Inside getAllPrompt")
        try: 
            """ Check if the user is authorized to get the prompt """
            if self.loggedUser != GLOBAL_USER_ID:
                raise ForbiddenException()
            
            """ Get all the prompt from the database """
            promptList = list(self.promptcoll.find({"createdBy": self.loggedUser, "isDeleted": False},{"_id":0}))

            self.customlog.info("Prompt List: %s", promptList)
            self.customlog.info("End getAllPrompt")
            return promptList
        
        except NotFoundException as nfe:
            raise HTTPException(**nfe.__dict__)
        except ForbiddenException as fe:
            raise HTTPException(**fe.__dict__)
        except BusinessException as be:
            raise HTTPException(**be.__dict__)
        except Exception as ise:
            self.customlog.error("Exception: %s", ise)
            raise InternalServerException()
    

    def getPromptById(self, promptId) -> PromptResponse:
        self.customlog.info("Inside getPromptById")
        try:
            """ Check if the user is authorized to get the prompt """
            if self.loggedUser != GLOBAL_USER_ID:
                raise ForbiddenException()
            
            """ Check if the prompt is present in the database """
            prompt = self.promptcoll.find_one({"createdBy": self.loggedUser, "id": promptId, "isDeleted": False},{"_id":0})

            if prompt is None:
                raise NotFoundException(ErrorMessageCode.PROMPT_NOT_FOUND_ERROR.value.code, ErrorMessageCode.PROMPT_NOT_FOUND_ERROR.value.message)
            
            self.customlog.info("Prompt: %s", prompt)
            self.customlog.info("End getPromptById")
            return PromptResponse(**prompt)
        
        except NotFoundException as nfe:
            raise HTTPException(**nfe.__dict__)
        except ForbiddenException as fe:
            raise HTTPException(**fe.__dict__)
        except BusinessException as be:
            raise HTTPException(**be.__dict__)
        except Exception as ise:
            self.customlog.error("Exception: %s", ise)
            raise InternalServerException()
    
    def updatePrompt(self, body) -> PromptResponse:
        self.customlog.info("Inside updatePrompt")
        try:
            """ Check if the user is authorized to update the prompt """
            if self.loggedUser != GLOBAL_USER_ID:
                raise ForbiddenException()
            
            """ Check if the prompt is present in the database """
            promptObj = self.promptcoll.find_one({"id": body.id, "isDeleted": False})

            if promptObj is None:
                raise NotFoundException(ErrorMessageCode.PROMPT_NOT_FOUND_ERROR.value.code, ErrorMessageCode.PROMPT_NOT_FOUND_ERROR.value.message)
            
            if body.projectId != promptObj["projectId"]:
                raise BusinessException(ErrorMessageCode.PROJECT_NOT_FOUND_ERROR.value.code, ErrorMessageCode.PROJECT_NOT_FOUND_ERROR.value.message)
            
            """ Validate the input data  for update the prompt """
            if body.name is not None and body.name != promptObj["name"]:
                raise BusinessException(ErrorMessageCode.PROMPT_NAME_UPDATE_ERROR.value.code, ErrorMessageCode.PROMPT_NAME_UPDATE_ERROR.value.message)
            
            if body.mode not in MODE_LIST:
                raise BusinessException(ErrorMessageCode.INVALID_MODE_ERROR.value.code, ErrorMessageCode.INVALID_MODE_ERROR.value.message)

            if body.mode is not None and body.mode != "" and body.mode != promptObj["mode"] :
                promptObj["mode"] = body.mode

            if body.modelName is not None and  body.modelName != "" and body.modelName != promptObj["modelName"] :
                promptObj["modelName"] = body.modelName

            if body.modelId is not None and body.modelId != "" and body.modelId != promptObj["modelId"] :
                promptObj["modelId"] = body.modelId

            if body.version is not None and body.version != "" and body.version != promptObj["version"] :
                promptObj["version"] = body.version

            if body.mode == "chat"  and body.conversationRole not in ROLE_LIST:
                raise BusinessException(ErrorMessageCode.ROLE_LIST_INVALID_ERROR.value.code, ErrorMessageCode.ROLE_LIST_INVALID_ERROR.value.message)

            if body.conversationRole is not None and body.conversationRole != "" and body.conversationRole != promptObj["conversationRole"] :
                promptObj["conversationRole"] = body.conversationRole

            if body.conversationContent is not None and body.conversationContent != "" and body.conversationContent != promptObj["conversationContent"] :
                promptObj["conversationContent"] = body.conversationContent

            if body.parameters is not None:
                if isinstance(body.parameters, list):
                    promptObj["parameters"] = [param.__dict__ for param in body.parameters]
                else:
                    promptObj["parameters"] = body.parameters.__dict__

            promptObj["updatedBy"] = self.loggedUser
            promptObj["modifiedOn"] = datetime.datetime.utcnow()
            promptObj['status'] = PromptStatusEnum.Updated  
            print("Prompt Obj: ", promptObj)
            
            """ update the prompt  in the database """
            updatedPrompt = self.promptcoll.update_one({"id": body.id}, {"$set": promptObj})
            print("Updated Prompt: ", updatedPrompt)

            return PromptResponse(**promptObj)
        
        except NotFoundException as nfe:
            raise HTTPException(**nfe.__dict__)
        except ForbiddenException as fe:
            raise HTTPException(**fe.__dict__)
        except BusinessException as be:
            raise HTTPException(**be.__dict__)
        except Exception as ise:
            self.customlog.error("Exception: %s", ise)
            raise InternalServerException()