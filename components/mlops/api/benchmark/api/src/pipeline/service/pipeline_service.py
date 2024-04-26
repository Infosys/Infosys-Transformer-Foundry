# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: pipeline_service.py
description: handles the CRUD operation for  Usecase module

"""
import pydantic
import re
import requests
import subprocess
import time
from dotenv import dotenv_values, find_dotenv
from operator import itemgetter
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import List, Any, Set, Optional
import string
import uuid
from fastapi import Request
from aicloudlibs.schemas.benchmark_pipeline_mappers import *
from aicloudlibs.exceptions.global_exception import ForbiddenException
from aicloudlibs.constants.util_constants import EXECUTE_PIPELINE, WORKSPACEADMIN, CREATE_PIPELINE, VIEW
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from pipeline.exception.exception import *
import pipeline.constants.local_constants as local_errors
import json
from pipeline.service.payload_generation import CodeGenerationKubeflow
from fastapi import Request, Header, Response, Query
from datetime import date, datetime, timedelta



dotenv_path = find_dotenv()
config = dotenv_values(dotenv_path)


class BaseService:

    def __init__(self, app):
        self.log = app.logger
        self.app = app
        # self.loggedUser = userId


class PipelineService(BaseService):

    def __init__(self, app):
        super(PipelineService, self).__init__(app)
        self.metric_output = {"name": None, "value": None}

    # To Execute the benchmark with respective model and dataset details in the payload.
    def create_pipeline(self, payload: BenchmarkPipeline, userId) -> PipelineResponseData:        

        payload = jsonable_encoder(payload)
        if(payload['projectId']==None or payload['projectId']==""):
            if(payload['type']=="code"):
                projectId=config['CODE']
                taskImage=config['CODE_TASK_IMAGE']
                consolidatedImage=config['CODE_CONSOLIDATED_IMAGE']
                esImage=config['CODE_ES_IMAGE']
                indexName=config['CODE_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "code"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))
            elif(payload['type']=="text"):
                projectId=config['TEXT']
                taskImage=config['TEXT_TASK_IMAGE']
                consolidatedImage=config['TEXT_CONSOLIDATED_IMAGE']
                esImage=config['TEXT_ES_IMAGE']
                indexName=config['TEXT_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "text"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))
            elif(payload['type']=="embedding"):
                projectId=config['EMBEDDING']
                taskImage=config['EMBEDDING_TASK_IMAGE']
                consolidatedImage=config['EMBEDDING_CONSOLIDATED_IMAGE']
                esImage=config['EMBEDDING_ES_IMAGE']
                indexName=config['EMBEDDING_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "embedding"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))

                
        else:
            projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
            if projectObj is None:
                    raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
            projectId=payload['projectId'] 
            if(payload['type']=="code"):
                taskImage=config['CODE_TASK_IMAGE']
                consolidatedImage=config['CODE_CONSOLIDATED_IMAGE']
                esImage=config['CODE_ES_IMAGE']
                indexName=config['CODE_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "code"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))
            elif(payload['type']=="text"):
                taskImage=config['TEXT_TASK_IMAGE']
                consolidatedImage=config['TEXT_CONSOLIDATED_IMAGE']
                esImage=config['TEXT_ES_IMAGE']
                indexName=config['TEXT_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "text"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))
            elif(payload['type']=="embedding"):
                taskImage=config['EMBEDDING_TASK_IMAGE']
                consolidatedImage=config['EMBEDDING_CONSOLIDATED_IMAGE']
                esImage=config['EMBEDDING_ES_IMAGE']
                indexName=config['EMBEDDING_INDEX_VALUE']
                metadataObj = list(self.app.database["benchmark_metadata_genargs"].find({"type": "embedding"},{'_id': 0,"createdBy":0,"createdOn":0,"isDeleted":0,"updatedBy":0,"modifiedOn":0,"type":0}))
       
        
        has_access = globalValidations.hasAccess(userId, projectId, CREATE_PIPELINE) or globalValidations.hasAccess(userId, projectId, WORKSPACEADMIN)

        if not has_access:
            raise InvalidValueError(local_errors.ErrorCode.USER_PERMISSION_ERROR)

        benchmark = self.app.database["benchmark"].find_one({'name':payload['name'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        if benchmark != None:
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NAME_ERROR)
        
        if payload['name'] == "":
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NAME)
        
        if len(payload['configuration']['model'])>1 and len(payload['configuration']['data'])>1:
            raise InvalidValueError(local_errors.ErrorCode.INVALID_DATA_MODEL_INPUT_ERROR)

        obj = CodeGenerationKubeflow(payload['type'])
        kubeflow_code = obj.get_kubeflow_code(payload,projectId,metadataObj,indexName,taskImage,consolidatedImage,esImage)
       
        maxlength = len(payload['configuration']['model'])
        dependsOn = [] 
        variable_dict = {}
        
        dataset = payload['configuration']['data'][0]
        l= len(payload['configuration']['model'])
        
        
        jobHeaders = {'userId':userId,'Content-Type': 'application/json' }
        
        url= config['CREATE_PIPELINE_URL']
        response = requests.post(url, data=kubeflow_code, headers=jobHeaders)
       
        if response.status_code == 200:
            exe_payload=json.loads(kubeflow_code)
            response_struct = response.json()
            pipeline_id=response_struct['data']['id']
            document = self.app.database["pipeline_definition"].find_one({'id':pipeline_id},{'_id': 0})
            jobHeadersExe = { 'pipelineId':pipeline_id,'userId':userId,  'Content-Type': 'application/json'}
            execution_payload ={}
            execution_payload['pipeline']={}
            execution_payload['pipeline']['dataStorage']=[{
                "storageType": payload['configuration']['dataStorage']['storageType'],
                "name": "vp-test-run",
                "uri": payload['configuration']['dataStorage']['uri']
            }]
            execution_payload['pipeline']['variables']=exe_payload['pipeline']['variables']
            execution_payload['pipeline']['globalVariables']=exe_payload['pipeline']['globalVariables']
          
            execution_payload = json.dumps(execution_payload)

            url1 = config['EXECUTE_PIPELINE_URL']+pipeline_id
            executionresponse = requests.post(url1, data=execution_payload,headers=jobHeadersExe)
           
            if executionresponse.status_code == 200:
                executionresponse_struct = executionresponse.json()
                execution_id=executionresponse_struct['data']['executionId']
        
                payload['status'] = "INPROGRESS"
                payload['createdOn'] = datetime.utcnow()
                payload['createdBy'] = userId
                payload['isDeleted'] = False
                payload['modifiedOn'] = None
                payload["id"] = str(uuid.uuid4().hex)
                payload['projectId']=projectId
                payload['pipelineId']=pipeline_id
                payload['executionId']=execution_id
                pipelinedata = self.app.database["benchmark"].insert_one(payload)
                
                created_pipeline = self.app.database["benchmark"].find_one({"_id": pipelinedata.inserted_id},{"_id": 0})
               
                return PipelineResponseData(**created_pipeline)
                
            else:
                raise JenkinsJobError("Error occured while executing pipeline")  
        else:
            raise JenkinsJobError("Error occured while creating pipeline")    
        
    # To get the status of the executed benchmark with benchmarkId and userId
    def getBenchmarkStatus(self, request: Request, benchmarkId: str, userId: str)-> GetBenchmarkStatusResponseData:
        benchmarkObj = request.app.database["benchmark"].find_one({"id": benchmarkId, "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})
        
        executionObj = request.app.database["pipeline_execution"].find_one({"id": benchmarkObj['executionId'], "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})

        if benchmarkObj is None:
                raise InvalidValueError(local_errors.ErrorCode.BENCHMARK_NOT_FOUND_ERROR)
        projectId = benchmarkObj['projectId']
        projectObj = self.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        

        new_updated_benchmarkObj=request.app.database["benchmark"].update_one({"id": benchmarkId},{"$set": {"status" : executionObj['status']}})
        updated_benchmarkObj = request.app.database["benchmark"].find_one({"id": benchmarkId, "isDeleted": pydantic.parse_obj_as(bool, "false")},{'_id': 0})     
                                                       
        projectId = projectObj['id']

        has_access = globalValidations.hasAccess(userId, projectId, VIEW) or globalValidations.hasAccess(
            userId, projectId, WORKSPACEADMIN)
        if not has_access:
            raise ForbiddenException
        
        return updated_benchmarkObj
    
    # To get the task/modelGenArgs for benchmark w.r.t benchmarkType and metadataType
    def list_benchmark_metadata(self, request: Request, benchmarkType: str, metadataType: str,userId: str):        
        
        if metadataType=='modelGenArgs':
            metadataObj = list(request.app.database["benchmark_metadata_genargs"].find({"type": benchmarkType},{'_id': 0}).distinct('model gen args name'))
        else:
            metadataObj = list(request.app.database["benchmark_metadata"].find({"type": benchmarkType},{'_id': 0}).distinct(metadataType))
       
        return metadataObj

    # To get the dataset for benchmark w.r.t benchmarkType and task
    def list_dataset(self, request: Request, benchmarkType: str, task: str,userId: str):
        datasetObj =list(request.app.database["benchmark_metadata"].find({"type": benchmarkType,"task":task},{'_id': 0,'type':0,'task':0,'language':0}).distinct('dataset'))        
        return datasetObj
    
    # To get the list of benchmark associated with given projectId and userId
    def list_benchmark(self, request: Request, projectId: str, userId: str) -> dict:
        
        invalid_characters = set(string.punctuation)
        if projectId is not None:

            if any(char in invalid_characters for char in projectId):
                InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

            if len(projectId) != 32:
                raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

            projectObj = request.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})

            if projectObj is None:
                raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

            permissions_available = [EXECUTE_PIPELINE, WORKSPACEADMIN, VIEW]
            has_access = False

            for permission in permissions_available:
                has_access = globalValidations.hasAccess(userId, projectId, permission)
                if has_access:
                    break

            if has_access:
                benchmarkObj = list(request.app.database["benchmark"].find({"projectId": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0}))
                benchmarkObj_sorted=sorted(benchmarkObj, key=lambda i: (i['createdOn']), reverse=True)
                benchmark_response = {}
                benchmark_response['benchmarks']= benchmarkObj_sorted
                return  benchmarkObj

            else:
                raise ForbiddenException()