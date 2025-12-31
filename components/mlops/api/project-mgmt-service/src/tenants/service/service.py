# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: service.py
description: handles the CRUD operation for  Usecase module
"""
from fastapi import Depends,Request, status
from tenants.exception.exception import *
from fastapi.encoders import jsonable_encoder
from tenants.constants import local_constants as constant
from typing import List
import pydantic 
import datetime  
from aicloudlibs.schemas.project_mappers import Tenant, TenantStatusEnum, ResourceConfig, Compute
from projects.mappers.mappers import is_valid_uuid
import uuid
import re
from aicloudlibs.constants.error_constants import *

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class TenantsService:
        """
        TenantsService class which handles the create and delete operations for tenant module
        """
        ## Create tenants
        def create_tenants(request: Request, userId:str, body:Tenant) -> dict:                 
            if (userId is None) or (userId =='' ) :
              raise exception(1094,constant.USERID) 
            
            if not (re.fullmatch(regex,userId)):
              raise exception(1004,constant.INVALIDEMAIL)                       
            
            if(len(body.name)> int("25")):
              raise exception(1005, constant.CHARVALIDATION)  
                                                          
            checkAlreayExists = request.app.database["tenant"].count_documents({ "name": body.name, "createdBy":userId, "isDeleted":pydantic.parse_obj_as(bool, "false") })            
                         
            if (checkAlreayExists >=1)  :
              raise exception(1009,constant.TENANT_ALREADY_EXISTS.replace(constant.PLACEHOLDER_TEXT,body.name))         
                                          
            todayDate = datetime.datetime.utcnow()                
            Jsonbody = jsonable_encoder(body)            
            Jsonbody["createdBy"] = userId
            Jsonbody["id"] = str(uuid.uuid4().hex)  
            Jsonbody["status"] =  TenantStatusEnum.Created
            Jsonbody["modifiedOn"] = None
            
            computesArray = []  
            quotoComputes = []         
            for data_Item in body.quotaConfig.computes:
              dictComputes = {}
              dictComputes['type'] = data_Item.type.upper()
              dictComputes["maxQty"] = 0
                            
              if(data_Item.type.upper()=="CPU"):                       
                  dictComputes['memory']= "0GB"

              if(data_Item.type.upper()=="GPU"):
                data_Item.memory = data_Item.memory.upper()
                dictComputes['memory'] = data_Item.memory

              dictComputes["minQty"] = 0
              computesArray.append(dictComputes)

            listComputes = {'computes': computesArray, 'volumeSizeinGB': 0}

            Jsonbody["currentResourceUsage"]= listComputes
            print(Jsonbody)

            new_tenant_info = request.app.database["tenant"].insert_one(Jsonbody)        
            created_tenant = request.app.database["tenant"].find_one({"_id": new_tenant_info.inserted_id}, {"_id":0})
            return  created_tenant
        
        # Delete a tenant from the database - soft delete
        def delete_tenant(request:Request,tenantId: str, userId: str): 
            if (userId is None) or (userId =='' ) :
              raise exception(1094,constant.USERID) 
            
            if not (re.fullmatch(regex,userId)):
              raise exception(1004,constant.INVALIDEMAIL)         
            
            tenant = list(request.app.database["tenant"].find({ "id" : str(tenantId), "isDeleted":pydantic.parse_obj_as(bool, "false")}))
            if len(tenant)==0:
              raise exception(status.HTTP_204_NO_CONTENT, constant.TENANT_DOESNOT_EXIST)
            
            todayDate = datetime.datetime.utcnow()

            # soft delete projects present in the tenant
            projects = list(request.app.database["project"].find({ "tenantId" : str(tenantId), "isDeleted":pydantic.parse_obj_as(bool, "false")}))
            for project in projects:
                filter = {'id':project['id'], 'isDeleted':False}
                project['isDeleted'] = True
                project['updatedBy'] = userId
                project['modifiedOn'] = todayDate
                request.app.database["project"].update_one(filter, {"$set":project})
                                                  
            tenant = list(request.app.database["tenant"].find({ "id" : str(tenantId), "createdBy":userId,"isDeleted":pydantic.parse_obj_as(bool, "false")}))
            if len(tenant)>0:
              request.app.database["tenant"].update_one({ "id" : str(tenantId)},{"$set":{"status":TenantStatusEnum.Deleted , "isDeleted":True, "updatedBy": userId,"modifiedOn":todayDate}})
              return True
            else:
              raise exception(1009, NOT_AUTHORIZED_ERROR)
            
        ## get tenant
        def get_tenant(request:Request, tenantId:str, userId:str) -> dict:             
          if not is_valid_uuid(tenantId):              
            raise exception(1085, constant.IS_VALID_UUID) 
          
          tenant = request.app.database["tenant"].find_one({"id": tenantId, "createdBy" : userId, "isDeleted": pydantic.parse_obj_as(bool,"false")},{"_id":0})
          if tenant is None:                         
            tenant = request.app.database["tenant"].find_one({"id": tenantId, "userLists.userEmail" : userId, "isDeleted": pydantic.parse_obj_as(bool,"false")})
            if tenant is None: 
              raise exception(1032, TENANT_DET_NOT_FOUND_ERROR)      
          return tenant

        def ResponseModel(code,data):
         return {
               "status":"SUCCESS", 
               "code": code,
               "data": data
              }

        def ErrorResponseModel(code, message):
          return {
            "status": "FAILURE", 
            "code": code, 
            "message": message
             }     