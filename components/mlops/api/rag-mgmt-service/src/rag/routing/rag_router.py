# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: rag_router.py
description: Routing details for Pipeline CRUD operations

"""
import json
from bson import json_util, ObjectId
from fastapi import Request, Header, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Request, APIRouter, HTTPException
from aicloudlibs.schemas.global_schema import NotAuthorizedError, InternalServerError
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException
from aicloudlibs.constants.http_status_codes import HTTP_NOT_AUTHORIZED_ERROR, HTTP_STATUS_INTERNAL_SERVER_ERROR
from rag.exception.exception import RagException
from rag.service.rag_service import RagService as service, BaseService
import rag.constants.local_constants as constant
from rag.util.log_formatter import LogFormatter
from rag.mappers.mappers import RagIndex, SetUp, Index, FileUploadResponse, RagResponse, IndexResponse, SetUpResponse, GetRagIndexStatusResponse, SetUpResponse, SearchDetails, SearchResponse, SearchResponseData
from typing import List, Union
from fastapi import Request, Header, Response, Query
from typing import Optional


router = APIRouter()
log_formatter = LogFormatter('Rag Management')

def _get_encoded_response(data: dict):
    dumped_data = json_util.dumps(data, indent=4, default=json_util.default)
    page_sanitized = json.loads(dumped_data, object_hook=json_util.object_hook)
    return page_sanitized

# Create Rag Index API: Defines the routing path details for create usecase operation and invokes the create rag index service
@router.post("/rag/createrag",response_model=RagResponse, include_in_schema=False, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError},                       HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def create_ragindex(request: Request, payload: RagIndex  , userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Rag Evaluation", "Create rag index" + "{senderURI }" + "{RequestID }", str(userId), str(RagIndex))
    log = request.app.logger
    try:
        
        service_obj = service(request.app)
        rag_detail = service_obj.create_rag_index(payload, userId)
        log.debug("response : " + str(rag_detail))
        RagResponse.code = 200
        RagResponse.status = "Success"
        RagResponse.data = jsonable_encoder(rag_detail)
        responseDict = RagResponse.__dict__
        return responseDict

    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Get Rag Index Status API: Defines the routing path details for get rag index status operation and invokes the get rag index status service
@router.get("/rag/indexstatus/{indexId}", response_model=GetRagIndexStatusResponse, include_in_schema=False, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def getRagIndexStatus(request:Request,response: Response,indexId: str, userId: str = Header(convert_underscores=False)):
    
    log = request.app.logger
    log_formatter.set_prefixes('benchmarkstatus Pipeline', userId, 'NA')
    try:
        service_obj = service(request.app)
        benchmarkStatusdetails = service_obj.getRagIndexStatus(request, indexId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(benchmarkStatusdetails)}"))
        print(benchmarkStatusdetails)
        GetRagIndexStatusResponse.code=200
        GetRagIndexStatusResponse.status="Success"
        GetRagIndexStatusResponse.data = jsonable_encoder(benchmarkStatusdetails)
        responseDict = GetRagIndexStatusResponse.__dict__
        # apiResp = ResponseModel(benchmarkStatus)
        return responseDict
    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Create Index API: Defines the routing path details for create index operation and invokes the create index service
@router.post("/rag/index",response_model=IndexResponse,responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def create_index(request: Request, payload: Index  , userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Rag Evaluation", "Create rag index" + "{senderURI }" + "{RequestID }", str(userId), str(Index))
    log = request.app.logger
    try:
        
        service_obj = service(request.app)
        rag_detail = service_obj.create_index(payload, userId)
        log.debug("response : " + str(rag_detail))
        IndexResponse.code = 200
        IndexResponse.status = "Success"
        IndexResponse.data = jsonable_encoder(rag_detail)
        responseDict = IndexResponse.__dict__
        return responseDict

    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Create Setup API: Defines the routing path details for create setup operation and invokes the create setup service
@router.post("/rag/setup",response_model=SetUpResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def create_setup(request: Request, payload: SetUp  , userId: str = Header(convert_underscores=False)):
    prefix = constant.LOG_PREFIX.format("Rag Evaluation", "Create rag index" + "{senderURI }" + "{RequestID }", str(userId), str(SetUp))
    log = request.app.logger
    try:
        
        service_obj = service(request.app)
        rag_detail = service_obj.create_setup(payload, userId)
        log.debug("response : " + str(rag_detail))
        SetUpResponse.code = 200
        SetUpResponse.status = "Success"
        SetUpResponse.data = jsonable_encoder(rag_detail)
        responseDict = SetUpResponse.__dict__
        return responseDict

    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Upload File API: Defines the routing path details for upload file operation and invokes the upload file service
@router.post("/rag/uploadfile", response_model=FileUploadResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError},HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def uploadFile(request:Request,response: Response,indexName: str, file: UploadFile = File(...)):
    
    log = request.app.logger
    try:
        service_obj = service(request.app)
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        fileName = file.filename
        benchmarkStatusdetails = service_obj.uploadFile(request, indexName, fileName)
        FileUploadResponse.code=200
        FileUploadResponse.status="Success"
        FileUploadResponse.data = jsonable_encoder(benchmarkStatusdetails)
        responseDict = FileUploadResponse.__dict__
        return responseDict
    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Delete Index API: Defines the routing path details for delete index operation and invokes the delete index service
@router.delete('/rag/deleteIndex/{indexId}',response_model=GetRagIndexStatusResponse,responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def deleteIndex(request: Request, indexId:str = Query(..., alias='indexId'),userId: str = Header(..., alias='userId')):
    log = request.app.logger
    try:
        service_obj = service(request.app)
        deleteStatus = service_obj.deleteIndex(indexId, userId) 
        GetRagIndexStatusResponse.code=200
        GetRagIndexStatusResponse.status="Success"
        GetRagIndexStatusResponse.data = jsonable_encoder(deleteStatus)
        responseDict = GetRagIndexStatusResponse.__dict__
        return responseDict
    
    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# Get Setup Index Status API: Defines the routing path details for get setup index status operation and invokes the get setup index status service
@router.get("/rag/setupstatus/{setupId}", response_model=GetRagIndexStatusResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def getSetupIndexStatus(request:Request,response: Response,setupId, userId: str = Header(convert_underscores=False)):
    
    log = request.app.logger
    try:
        service_obj = service(request.app)
        setupIndexStatusdetails = service_obj.getSetupIndexStatus(request, setupId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(setupIndexStatusdetails)}"))
        print(setupIndexStatusdetails)
        GetRagIndexStatusResponse.code=200
        GetRagIndexStatusResponse.status="Success"
        GetRagIndexStatusResponse.data = jsonable_encoder(setupIndexStatusdetails)
        responseDict = GetRagIndexStatusResponse.__dict__
        # apiResp = ResponseModel(benchmarkStatus)
        return responseDict
    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)


# List Index API: Defines the routing path details for list index operation and invokes the list index service
@router.get("/rag/indexes", response_model=dict, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError},HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def listIndex(request: Request, projectId: str,  pipelineId: Optional[str]= None, queryType: Optional[str]= None):
    log = request.app.logger
    log.info("rag_router list_index() - request : " + str(projectId) + " " + str(pipelineId))
    #log_formatter.set_prefixes('list index', userId, 'NA')
    try:
        log.info("rag_router list_index() inside try block")
        #log.info(log_formatter.get_msg(f"list_index - request : {str(projectId)} {str(userId)}"))
        service_obj = service(request.app)
        log.info("rag_router list_index() before calling service_obj.listIndex()")
        indexList = service_obj.listIndex(request, projectId, pipelineId, queryType)
        log.info("rag_router list_index() after calling service_obj.listIndex()")
        log.debug(log_formatter.get_msg("response : " + str(indexList)))
        response = {
            "code" : 200,
            "status": "Success",
            "data" :indexList
        }
        responseDict = jsonable_encoder(response)
        log.info("rag_router list_index() before returning response")
        return responseDict

    except RagException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    

# Get Search Details API: Defines the routing path details for get search details operation and invokes the get search details service
@router.get("/rag/getSearch", response_model=dict, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def getSearchDetails(request: Request, chatId: str,  queryId: str):
    log = request.app.logger
    try:
        service_obj = service(request.app)
        searchDetails = service_obj.getSearchDetails(request, chatId, queryId)
        log.debug(log_formatter.get_msg("response : " + str(searchDetails)))
        response = {
            "code" : 200,
            "status": "Success",
            "data" :searchDetails
        }
        responseDict = jsonable_encoder(response)
        return responseDict

    except RagException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# Search API: Defines the routing path details for search operation and invokes the search service
@router.post("/rag/search", response_model=SearchResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def search(request:Request, payload: SearchDetails ):
    
    log = request.app.logger
    try:
        service_obj = service(request.app)
        searchDetails = service_obj.search(payload)
        print("searchDetails",searchDetails)
        SearchResponse.code=200
        SearchResponse.status="Success"
        SearchResponse.data = jsonable_encoder(searchDetails)
        responseDict = SearchResponse.__dict__
        return responseDict
    except RagException as ragException:
        log.error(log_formatter.get_msg(str(ragException.__dict__)))
        raise HTTPException(**ragException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)