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
from fastapi import Request
from aicloudlibs.schemas.pipeline_mappers import *
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException
from aicloudlibs.constants.util_constants import EXECUTE_PIPELINE, WORKSPACEADMIN, CREATE_PIPELINE, VIEW
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from pipeline.exception.exception import *
import pipeline.constants.local_constants as local_errors
import json

dotenv_path = find_dotenv()
config = dotenv_values(dotenv_path)

class BaseService:
    def __init__(self, app):
        self.log = app.logger
        self.app = app

class PipelineService(BaseService):

    def __init__(self, app):
        super(PipelineService, self).__init__(app)
        self.metric_output = {"name": None, "value": None}

    # Function to convert string to int or float
    def _convert_float_int(self, number, d_type):
        try:
            return d_type(number)
        except ValueError:
            return False

    # Create the pipeline based on the input payload and userId
    def create_pipeline(self, payload: PipelineJobDetails, userId) -> PipelineResponseData:

        payload = jsonable_encoder(payload)

        if len(payload['projectId']) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        projectId = projectObj['id']

        has_access = globalValidations.hasAccess(userId, projectId, CREATE_PIPELINE) or globalValidations.hasAccess(
            userId, projectId, WORKSPACEADMIN)

        if has_access:
            check_already_exists = self.app.database["pipeline"].find({"projectId": payload['projectId'], "name": payload['name'], "version": payload['version'], "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()

            if check_already_exists != 0:
                raise PipelineAlreadyExistsError(local_errors.ErrorCode.PIPELINE_EXIST_ERROR)

            unique_job_arguments = []
            unique_step_argument = []

            for job_arg in payload['jobArguments']:
                unique_job_arguments.append(job_arg['name'])

                dataTypeTxt = job_arg['dataType']
                if dataTypeTxt not in ('bool', 'string', 'int', 'float'):
                    raise InvalidValueError(local_errors.ErrorCode.INVALIDJOBARGUMENTDATATYPE_ERROR)
                
                defaultVal = job_arg['defaultVal']
                if defaultVal != "":
                    if dataTypeTxt == 'string' and isinstance( defaultVal , str) and  defaultVal.lower() in {'true', 'false'}:
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_JOBARG_DEFAULTVALUE_ERROR)
                    if dataTypeTxt == 'bool' and not (str(defaultVal).lower() in ('true', 'false')):
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_JOBARG_DEFAULTVALUE_ERROR)
                    if dataTypeTxt == 'int' and not (self._convert_float_int(defaultVal, int)):
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_JOBARG_DEFAULTVALUE_ERROR)
                    if dataTypeTxt == 'float' and not (self._convert_float_int(defaultVal, float)):
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_JOBARG_DEFAULTVALUE_ERROR)

            job_arg_list = [n['name'] for n in payload['jobArguments']]

            for i, step in enumerate(payload['steps']):
                if step['trainingStep']['inputArtifacts']['uri'] is not None:
                    artifact_uri = step['trainingStep']['inputArtifacts']['uri']
                    if artifact_uri.startswith("s3://"):
                        artifact_uri = artifact_uri.split(payload['projectId'])
                        print("***********")
                        print(artifact_uri)
                        if len(artifact_uri) != 2:
                            raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_ARTIFACT_ERROR)
                        artifact_uri = payload['projectId'] + artifact_uri[1]
                        print("artifact_uri: ",artifact_uri)

                    expected_artificat_uri = "{}/pipeline/{}/{}/input".format(payload['projectId'],payload['name'],str(payload['version']))
                    if artifact_uri != expected_artificat_uri:
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_ARTIFACT_ERROR)

                stepArglst = step['trainingStep']['stepArguments']['jobArgNames']
                for step_arg in stepArglst:
                    if step_arg not in job_arg_list:
                        raise InvalidValueError(local_errors.ErrorCode.STEPARGUMENTSNOTINJOBARGUEMENT)

                outputArtifact = step['trainingStep']['outputArtifactBaseUri']
                if outputArtifact is not None and outputArtifact != "NA":    
                    if outputArtifact.startswith(("s3://","s3:/","s3:")):
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_OUTPUT_ARTIFACT_ERROR)

                logFileUri = step['trainingStep']['metricDetails']['logFileUri']  
                if logFileUri is not None and logFileUri != "NA":    
                    if logFileUri.startswith(("s3://","s3:/","s3:")):
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_LOGFILEURI_ERROR)

            count_unique_step_argument = len(set(stepArglst))
            count_unique_job_arguments = len(set(unique_job_arguments))

            if count_unique_step_argument != count_unique_job_arguments:
                raise InvalidValueError(local_errors.ErrorCode.JOBSTEPARGUMENTMISMATCH_ERROR)

            payload['status'] = "Created"
            payload['createdBy'] = userId
            payload['modifiedOn'] = None
            payload["id"] = str(uuid.uuid4().hex)
            new_pipeline_info = self.app.database["pipeline"].insert_one(payload)
            created_pipeline = self.app.database["pipeline"].find_one({"_id": new_pipeline_info.inserted_id}, {"_id": 0})

            return PipelineResponseData(**created_pipeline)
        else:
            raise ForbiddenException()

    # get the list of pipelines based on projectId and userId
    def list_pipeline(self, request: Request, projectId: str, userId: str) -> ListPipelineResponseData:

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
                pipelineObj = list(request.app.database["pipeline"].find({"projectId": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0}))

                pipeline_response = {}
                pipeline_response['pipelines']= pipelineObj

                if len(pipelineObj) == 0:
                    raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

                return ListPipelineResponseData(**pipeline_response)

            else:
                raise ForbiddenException()

    # get the detail of pipeline based on pipeline-Id and userId
    def get_pipeline(self, request: Request, pipelineId: str, userId: str) -> GetPipelineResponseData:

        invalid_characters = set(string.punctuation)

        if pipelineId is not None:

            if any(char in invalid_characters for char in pipelineId):
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            if len(pipelineId) != 32:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            pipelineObj_delete_check = request.app.database["pipeline"].find_one({"id": pipelineId, "isDeleted": pydantic.parse_obj_as(bool, "true")})

            if pipelineObj_delete_check is not None:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_EXIST_ERROR)

            pipelineObj = request.app.database["pipeline"].find_one({"id": pipelineId, "isDeleted": pydantic.parse_obj_as(bool, "false")})

            if pipelineObj is None:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            projectId = pipelineObj['projectId']

            permissions_available = [EXECUTE_PIPELINE, WORKSPACEADMIN, VIEW]
            has_access = False

            for permission in permissions_available:
                has_access = globalValidations.hasAccess(userId, projectId, permission)
                if has_access:
                    break

            if has_access:
                pipelineObj = request.app.database["pipeline"].find_one({"id": pipelineId, "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0})
                pipeline_response = {}
                pipeline_response['pipeline'] = pipelineObj

                return GetPipelineResponseData(**pipeline_response)
            else:
                raise ForbiddenException()

    # delete the pipeline based on pipelineId and userId
    def delete_pipeline(self, request: Request, pipelineId: str, userId: str) -> str:
        invalid_characters = set(string.punctuation)

        if pipelineId is not None:

            if any(char in invalid_characters for char in pipelineId):
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            if len(pipelineId) != 32:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            pipelineObj_delete_check = request.app.database["pipeline"].find_one({"id": pipelineId, "isDeleted": pydantic.parse_obj_as(bool, "true")})

            if pipelineObj_delete_check is not None:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_EXIST_ERROR)

            pipelineObj_exist = request.app.database["pipeline"].find_one({"id": pipelineId, "isDeleted": pydantic.parse_obj_as(bool, "false")})

            if pipelineObj_exist == 0:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            projectId = pipelineObj_exist['projectId']

            has_access = globalValidations.hasAccess(userId, projectId, CREATE_PIPELINE) or globalValidations.hasAccess(userId, projectId, WORKSPACEADMIN)

            if has_access:
                pipelineObj = request.app.database["pipeline"].update_one({"id": pipelineId}, {"$set": {"isDeleted": True}})
                deleted_pipeline = self.app.database["pipeline"].find_one({"id": pipelineId}, {'_id': 0})

                del_pipeline_name = deleted_pipeline['name']
                del_pipeline_version = deleted_pipeline['version']

                success_msg = "Pipeline with name {} & version {} is deleted successfully".format(del_pipeline_name, del_pipeline_version)

                return success_msg
            else:
                raise ForbiddenException()