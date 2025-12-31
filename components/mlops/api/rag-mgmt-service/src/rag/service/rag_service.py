# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: service.py
description: handles the CRUD operation for  Usecase module

"""
import pydantic
import re
from dotenv import dotenv_values, find_dotenv
from operator import itemgetter
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import List, Any, Set
import string
import uuid
from fastapi import Request, UploadFile
from aicloudlibs.schemas.pipeline_mappers import *
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException
from aicloudlibs.constants.util_constants import EXECUTE_PIPELINE, WORKSPACEADMIN, CREATE_PIPELINE, VIEW
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from rag.exception.exception import *
import rag.constants.local_constants as local_errors
from rag.mappers.mappers import RagIndex, Index, SetUp, FileUploadResponseData, RagResponse, SetUpResponse, SetUpResponseData, IndexResponseData, RagResponseData, GetRagIndexStatusResponse, GetRagIndexStatusResponseData, SearchDetails, SearchResponse, SearchResponseData
import json
import s3fs
import os
from rag.service.template_generation import TemplateGenerationKubeflow
from rag.service.payload_generation import PayloadGenerationKubeflow
from fastapi import Request, Header, Response, Query
import requests

dotenv_path = find_dotenv()
config = dotenv_values(dotenv_path)

class BaseService:
    def __init__(self, app):
        self.log = app.logger
        self.app = app

class RagService(BaseService):

    def __init__(self, app):
        super(RagService, self).__init__(app)
        self.metric_output = {"name": None, "value": None}

    def create_rag_index(self, payload: RagIndex, userId: str) -> RagResponseData:
        payload= jsonable_encoder(payload)
        print(payload["projectId"])
        if len(payload['projectId']) != 32:
            raise InvalidValueException(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectObj is None:
            raise InvalidValueException(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        has_access = globalValidations.hasAccess(userId, payload['projectId'], CREATE_PIPELINE) or globalValidations.hasAccess(userId,payload['projectId'], WORKSPACEADMIN)

        if has_access:
            check_already_exists = self.app.database["index"].find({"projectId": payload['projectId'], "name": payload['name'], "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()
            if check_already_exists != 0:
                raise RagAlreadyExistsError(local_errors.ErrorCode.RAG_INDEX_EXIST_ERROR)
        else:
            raise ForbiddenException()

        payload['status'] = "Created"
        payload['createdOn'] = datetime.utcnow()
        payload['createdBy'] = userId
        payload['isDeleted'] = False
        payload['modifiedOn'] = None
        payload["id"] = str(uuid.uuid4().hex)
        indexdata = self.app.database["index"].insert_one(payload)
        
        created_index = self.app.database["index"].find_one({"_id": indexdata.inserted_id}, {"_id": 0})
        
        return RagResponseData(**created_index)

    def getRagIndexStatus(self, request: Request, indexId: str, userId: str)-> GetRagIndexStatusResponseData:
        indexObj = request.app.database["index"].find_one({"id": indexId, "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})
        
        if indexObj is None:   
            raise InvalidValueError(local_errors.ErrorCode.INDEX_NOT_FOUND_ERROR)

        projectId = indexObj['projectId']
        projectObj = self.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
    
        updated_indexObj = request.app.database["index"].find_one({"id": indexId, "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})  
                       
        projectId = projectObj['id']

        has_access = globalValidations.hasAccess(userId, projectId, VIEW) or globalValidations.hasAccess(userId, projectId, WORKSPACEADMIN)
        if not has_access:
            raise ForbiddenException
       
        return updated_indexObj   


    def create_index(self, payload: Index, userId: str) -> IndexResponseData:
        payload= jsonable_encoder(payload)
        if userId != "aicglobal@infosys.com":
            raise ForbiddenException()
        setup_record = self.app.database['setup'].find_one({"indexName": payload['indexName']})
        if setup_record is None:
            raise InvalidValueException(local_errors.ErrorCode.INDEX_NOT_FOUND_ERROR)
        updated_index = self.app.database["setup"].update_one({"indexName": payload['indexName']},{"$set": {"indexId" : payload['indexId'], "status":"Active"}})    
        find_index = self.app.database["setup"].find_one({"indexName": payload['indexName']})
        return IndexResponseData(**find_index)

    def create_setup(self, payload: SetUp, userId: str) -> SetUpResponseData:
        payload= jsonable_encoder(payload)
        print(payload["projectId"])
        if len(payload['projectId']) != 32:
            raise InvalidValueException(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectObj is None:
            raise InvalidValueException(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        has_access = globalValidations.hasAccess(userId, payload['projectId'], CREATE_PIPELINE) or globalValidations.hasAccess(userId,payload['projectId'], WORKSPACEADMIN)

        if has_access:
            check_already_exists = self.app.database["setup"].find({"projectId": payload['projectId'], "indexName": payload['indexName'], "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()
        else:
            raise ForbiddenException()

        pipeline_payload = document = self.app.database["pipeline_definition"].find_one({'id':payload['pipelineId'],"isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})

        if pipeline_payload is None:
            raise InvalidValueException(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)
        
        openaiModels = ["text-embedding-ada-002"]
        sentenceTransformerModels = ["all-MiniLM-L6-v2"]
        customModels = ["mistral-embd"]
        if payload['embeddingModelName'] in openaiModels:
            openaiEnabled = True
            sentenceTransformerEnabled = False
            customEnabled = False   
        elif payload['embeddingModelName'] in sentenceTransformerModels:
            openaiEnabled = False
            sentenceTransformerEnabled = True
            customEnabled = False
        elif payload['embeddingModelName'] in customModels:
            openaiEnabled = False
            sentenceTransformerEnabled = False
            customEnabled = True

        setup_record = self.app.database['setup'].find_one({"indexName": payload['indexName']})
        if setup_record is not None:
            index_name = ""
            index_id = setup_record['indexId']
            payload_enabled = False
        else:
            index_name = payload['indexName']
            index_id = ""
            payload_enabled = True
        
        obj = TemplateGenerationKubeflow()
        config_file = obj.get_kubeflow_code(payload, index_name, index_id, payload_enabled, openaiEnabled, sentenceTransformerEnabled, customEnabled)
    
        cwd = os.getcwd()
        with open(cwd+'/rag/service/config_file.json', 'w') as f:
            f.write(config_file)
        id = str(uuid.uuid4().hex)
        payload['status'] = "Inprogress"
        payload['createdOn'] = datetime.utcnow()
        payload['createdBy'] = userId
        payload['isDeleted'] = False
        payload['modifiedOn'] = None
        payload["id"] = id
        #cwd = os.getcwd()
        files = {'file': open(cwd+'/rag/service/config_file.json', 'rb')}
        url = config['UPLOAD_FILE_URL']
        parameter = {'indexName':payload['indexName']}
        response = requests.post(url, params=parameter, files=files)
        config_path_var = "transformer-studio/rag_data_injection/"+payload['indexName']+"/data/config/config_file.json"
        
        
        #print(pipeline_payload)
        jobHeadersExe = { 'pipelineId':payload['pipelineId'],'userId':userId,  'Content-Type': 'application/json'}
        execution_payload ={}
        execution_payload['pipeline']={}
        execution_payload['pipeline']['dataStorage']=pipeline_payload['pipeline']['dataStorage']
        execution_payload['pipeline']['variables']={
            "input_config_file_path":"/data/config/config_file.json",
        }
        execution_payload['pipeline']['globalVariables']={
            "DPP_STORAGE_SERVER_URL" : "${DPP_STORAGE_SERVER_URL}",
            "DPP_STORAGE_ROOT_URI" : "${DPP_STORAGE_ROOT_URI}"+payload['indexName'],
            "LOG_FILE_NAME" : "indexer",
            "LOG_LEVEL" : "DEBUG"
        }
        
        execution_payload = json.dumps(execution_payload)
        print(execution_payload)
        url1 = config['EXECUTE_PIPELINE_URL']+payload['pipelineId']
        executionresponse = requests.post(url1, data=execution_payload,headers=jobHeadersExe)
        if executionresponse.status_code == 200:
            executionresponse_struct = executionresponse.json()
            execution_id=executionresponse_struct['data']['executionId']
            payload['executionId'] = execution_id
        else:
            raise InternalServerException(local_errors.ErrorCode.PIPELINE_EXECUTION_ERROR)
        setupdata = self.app.database["setup"].insert_one(payload)
        created_setup = self.app.database["setup"].find_one({"_id": setupdata.inserted_id},{"_id": 0})
        
        return SetUpResponseData(**created_setup)


    def uploadFile(self, request: Request, indexName:str, fileName: str)-> FileUploadResponseData:
        s3_access_key=config["AWS_ACCESS_KEY_ID"]
        s3_secret_key=config["AWS_SECREAT_KEY"]
        s3_url = config["S3_URL"]
        s3 = s3fs.S3FileSystem(key=s3_access_key, secret=s3_secret_key, endpoint_url=s3_url)
        if fileName == "config_file.json" or fileName == "config_file":
            dest = "transformer-studio/rag_data_injection/"+indexName+"/data/config/"+fileName
        else:
            dest = "transformer-studio/rag_data_injection/"+indexName+"/data/input/"+fileName
        s3.put(fileName, dest)
        os.remove(fileName)
        return FileUploadResponseData(path=dest)  


    def deleteIndex(self, indexId: str, userId: str)-> GetRagIndexStatusResponseData:    
        indexObj = self.app.database["setup"].find_one({"indexId": indexId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if indexObj is None:
            raise  InvalidValueException(local_errors.ErrorCode.INDEX_NOT_FOUND_ERROR)

        vectorPayload = { 
            "model_name": indexObj['embeddingModelName'],
            "index_id": indexId,
            "collection_name": "documents",
            "collection_secret_key": ""     
        }
        vectorPayload = json.dumps(vectorPayload)
        print(vectorPayload)
        url = config['DELETE_INDEX_VECTORDB_URL']
        headers = {'Content-Type': 'application/json'}
        response1 = requests.post(url, data = vectorPayload, headers = headers)

        sparsePayload = {
            "method_name": "bm25s",
            "index_id": indexId,
            "collection_name": "documents", 
            "collection_secret_key": ""
        }

        sparsePayload = json.dumps(sparsePayload)
        print(sparsePayload)
        url = config['DELETE_INDEX_SPARSEDB_URL']
        headers = {'Content-Type': 'application/json'}
        response2 = requests.post(url, data = sparsePayload, headers = headers)
        res1 = response1.json()
      
        res2 = response2.json()
        
        if res1['responseCde'] == 200 and res2['responseCde'] == 200:     
            new_updated_setupObj=self.app.database["setup"].update_one({"indexId": indexId},{"$set": {"status":"Inactive", "isDeleted": True}})     
        else:  
            raise InvalidValueException(local_errors.ErrorCode.INDEX_DELETE_ERROR)

        new_updated_setupObj = self.app.database["setup"].find_one({"indexId": indexId, "isDeleted": pydantic.parse_obj_as(bool, "true")},{'_id': 0})     
                                                       
        return new_updated_setupObj

    def getSetupIndexStatus(self, request: Request, setupId: str, userId: str)-> GetRagIndexStatusResponseData:
        indexObj = request.app.database["setup"].find_one({"id": setupId},{'_id': 0})
        
        if indexObj is None:   
            raise InvalidValueException(local_errors.ErrorCode.INDEX_NOT_FOUND_ERROR)

        executionObj = request.app.database["pipeline_execution"].find_one({"id": indexObj['executionId'], "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})

        if executionObj['status'] == "Failed":
            new_updated_setupObj=request.app.database["setup"].update_one({"id": setupId},{"$set": {"status" : executionObj['status']}})
        
        updated_setupObj = request.app.database["setup"].find_one({"id": setupId},{'_id': 0})     

        return updated_setupObj   


    def listIndex(self, request: Request, projectId: str, pipelineId: Optional[str], queryType: Optional[str]) -> dict:

        log = request.app.logger
        log.info("rag_service listIndex() - request : " + str(projectId) + " " + str(pipelineId))
        projectObj = request.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectId is not None and pipelineId is not None:    
            if queryType == "status":
                indexObj = list(request.app.database["setup"].find({"projectId": projectId,"pipelineId": pipelineId}, {'_id': 0}))
            elif queryType == "search" or queryType == "setup":
                indexObj = list(request.app.database["setup"].find({"projectId": projectId,"pipelineId": pipelineId, "status":"Active"}, {'_id': 0}))
        elif projectId is not None and pipelineId is None:  
            indexObj = list(request.app.database["setup"].find({"projectId": projectId}, {'_id': 0}))  
        else:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        indexObj_sorted=sorted(indexObj, key=lambda i: (i['createdOn']), reverse=True)
        
        index_response = {}
        index_response= indexObj_sorted
        log.info("rag_service listIndex() - returning response")
        return  index_response

    def getSearchDetails(self, request: Request, chatId: str, queryId:str)-> SearchResponse:
        searchObj = request.app.database["chatDetails"].find_one({"chatId": chatId, "queryId": queryId},{'_id': 0})
        if searchObj is None:
            raise InvalidValueException(local_errors.ErrorCode.SEARCH_NOT_FOUND_ERROR)
        return searchObj  

    def search(self, payload: SearchDetails) -> SearchResponseData:
        payload= jsonable_encoder(payload)
        
        payload['status'] = "Created"
        payload['createdOn'] = datetime.utcnow()
        payload['createdBy'] = payload['chatId']
        payload['isDeleted'] = False
        payload['modifiedOn'] = None
        payload["id"] = str(uuid.uuid4().hex)
        searchdata = self.app.database["chatDetails"].insert_one(payload)
        
        searchDetails = self.app.database["chatDetails"].find_one({"_id": searchdata.inserted_id}, {"_id": 0})
        print("searchDetails",searchDetails)
        
        return SearchResponseData(**searchDetails)