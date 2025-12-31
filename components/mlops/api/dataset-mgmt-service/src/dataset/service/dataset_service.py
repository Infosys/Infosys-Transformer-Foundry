# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from typing import List
import datetime
import pydantic
import random
import uuid
from dotenv import dotenv_values
from bson.objectid import ObjectId
import dataset.constants.local_constants as local_errors
from dataset.config.logger import CustomLogger
# from aicloudlibs.schemas.model_mappers import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from aicloudlibs.constants.util_constants import *
from dataset.mappers.dataset_mappers import *
from dataset.exception.exception import *

class BaseService:
    def __init__(self, app):
        self.log = app.logger
        self.app = app

class DatasetService(BaseService):
    def __init__(self, app):
        super(DatasetService, self).__init__(app)
        self.metric_output = {"name": None, "value": None}

    def register_dataset(self, payload: DataSchema, userId) -> DatasetResponseData:
        payload= jsonable_encoder(payload)
        if len(payload['projectId']) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        has_access = globalValidations.hasAccess(userId, payload['projectId'], CREATE_PIPELINE) or globalValidations.hasAccess(userId,payload['projectId'], WORKSPACEADMIN)
        
        if has_access:
            check_already_exists = self.app.database["dataset"].find({"projectId": payload['projectId'], "dataset.name": payload['dataset']['name'], "dataset.version": payload['dataset']['version'], "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()
            if check_already_exists != 0:
                raise DatasetAlreadyExistsError(local_errors.ErrorCode.DATASET_EXIST_ERROR)
            
            payload['status'] = "Registered"
            payload['createdBy'] = userId
            payload['modifiedOn'] = None
            payload["id"] = str(uuid.uuid4().hex)

            new_dataset_record = self.app.database["dataset"].insert_one(payload)
            new_dataset=self.app.database["dataset"].find_one({"_id": new_dataset_record.inserted_id}, {"_id": 0})

            return DatasetResponseData(**new_dataset)        
        else:
            raise ForbiddenException()
        

    def get_userlist(self,projectId, userId) -> UserlistResponseData:
        if len(projectId) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        projectObj = self.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        has_access = globalValidations.hasAccess(userId, projectId, CREATE_PIPELINE) or globalValidations.hasAccess(userId,projectId, WORKSPACEADMIN)
        
        if has_access:
            userlist=[]
            userlist.append(projectObj['createdBy'])
            for user in projectObj['userLists']:
                userlist.append(user['userEmail'])
            return UserlistResponseData(userlist=userlist)
        else:
            raise ForbiddenException()
        

    def list_dataset(self, projectId, userId) -> ListDatasetResponseData:
        if len(projectId) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        projectObj = self.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)
        
        has_access = globalValidations.hasAccess(userId, projectId, VIEW) or globalValidations.hasAccess(userId,projectId, WORKSPACEADMIN)
        
        if has_access:
            datasetObj=list(self.app.database['dataset'].find({"projectId":projectId,"isDeleted":pydantic.parse_obj_as(bool, "false")},{'_id':0}))
            
            return ListDatasetResponseData(datasets=datasetObj)
        else:
            raise ForbiddenException()
        

    def list_dataset_by_scope(self,scope,userId) -> ListDatasetResponseData:
            
            datasetObj=list(self.app.database['dataset'].find({"dataset.scope":scope,"isDeleted":pydantic.parse_obj_as(bool, "false")},{'_id':0}))
            
            return ListDatasetResponseData(datasets=datasetObj)
    

    def get_dataset(self, datasetId, userId) -> GetDatasetResponseData:
        datasetObj = self.app.database["dataset"].find_one({"id": datasetId, "isDeleted": pydantic.parse_obj_as(bool, "false")},{"_id":0})
        print(datasetObj,"***&**&*&*")
        
        if datasetObj is None:
            raise InvalidValueError(local_errors.ErrorCode.DATASET_NOT_FOUND_ERROR)
        
        has_access = globalValidations.hasAccess(userId, datasetObj['projectId'], VIEW) or globalValidations.hasAccess(userId,datasetObj['projectId'], WORKSPACEADMIN)
        
        if has_access:
            return GetDatasetResponseData(dataset=datasetObj)
        else:
            raise ForbiddenException()
        

    def delete_dataset(self,datasetId, userId) -> str:
        datasetObj_exist = self.app.database["dataset"].find_one({"id": datasetId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if datasetObj_exist is None:
            raise InvalidValueError(local_errors.ErrorCode.DATASET_NOT_FOUND_ERROR)
                
        has_access = globalValidations.hasAccess(userId, datasetObj_exist['projectId'], CREATE_PIPELINE) or globalValidations.hasAccess(userId,datasetObj_exist['projectId'], WORKSPACEADMIN)
        
        if has_access:
            datasetObj = self.app.database["dataset"].update_one({"id": datasetId}, {"$set": {"isDeleted": True}})
            deleted_dataset = self.app.database["dataset"].find_one({"id": datasetId}, {'_id': 0})

            del_dataset_name = deleted_dataset['dataset']['name']
            del_dataset_version = deleted_dataset['dataset']['version']

            success_msg = "Dataset with name {} & version {} is deleted successfully".format(del_dataset_name, del_dataset_version)

            return success_msg
        else:
            raise ForbiddenException()


    def update_dataset(self, payload: DataSchema, datasetId, userId) -> DatasetResponseData:
        payload= jsonable_encoder(payload)
        datasetObj=self.app.database["dataset"].find_one({"id": datasetId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
        
        if datasetObj is None:
            raise InvalidValueError(local_errors.ErrorCode.DATASET_NOT_FOUND_ERROR)
        
        has_access = globalValidations.hasAccess(userId, datasetObj['projectId'], CREATE_PIPELINE) or globalValidations.hasAccess(userId,datasetObj['projectId'], WORKSPACEADMIN)
        
        if has_access:
            if ((datasetObj['dataset']['name']!=payload['dataset']['name']) or (datasetObj['dataset']['version']!=payload['dataset']['version'])):
                raise InvalidValueError(local_errors.ErrorCode.UPDATE_DATASET_ERROR)
            
            filter = {'id':datasetId,'isDeleted':False}
            datasetObjUpd = self.app.database["dataset"].update_one(filter,{"$set":{'dataset': payload['dataset'],'updatedBy': userId,'modifiedOn':datetime.utcnow()}})
            updated_dataset = self.app.database["dataset"].find_one(filter,{'_id':0})

            return DatasetResponseData(**updated_dataset)
        
        else:
            raise ForbiddenException()