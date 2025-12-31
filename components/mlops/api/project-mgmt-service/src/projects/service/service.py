# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: service.py
description: handles the CRUD operation for  Usecase module
"""   

from projects.exception.exception import *
from aicloudlibs.schemas.project_mappers import *
from aicloudlibs.constants.error_constants import TENANT_ID_NOT_EMPTY_ERROR, TENANT_NAME_NOT_EMPTY_ERROR
from projects.mappers.mappers import is_valid_uuid
from fastapi.encoders import jsonable_encoder
import pydantic 
from fastapi import Depends,Request,APIRouter, HTTPException,Body,status 
import time
import re
import uuid

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class projectService:             

        """
        ProjectService class which handles the create, get, get_all ,update, delete operations for project module
        """
        ## Create usecase
        def create_project(request:Request,userId:str,payload: Project) -> dict:           
            
            if (payload.description is None) or (payload.description =='' ) :
                raise exception(1095,constant.DESCRIPTION)
 
            #check the project name is empty or not. 
            if (payload.name is None) or (payload.name =='' ) :
                raise exception(1008,constant.PROJECT_NAME_VALIDATION_ERROR)           
              
            if(len(payload.name)> int("25")):
                raise exception(1006,constant.CHARVALIDATION)
            
            if not is_valid_uuid(payload.tenantId):
               raise exception(1085, constant.IS_VALID_UUID)            
                    
            #check the tenant details are found or not.             
            Tenant = request.app.database["tenant"].find_one(
                   {"id":  payload.tenantId, "createdBy" : userId, "isDeleted": pydantic.parse_obj_as(bool,"false")})
            if Tenant is None:                         
               Tenant = request.app.database["tenant"].find_one(
                       {"id":  payload.tenantId, "userLists.userEmail" : userId, "userLists.permissions.createProject": pydantic.parse_obj_as(bool,"true"), "isDeleted": pydantic.parse_obj_as(bool,"false")})
               if Tenant is None: 
                   raise exception(1085,constant.PERMISSION_NOT_FOUND_CREATE.format(userId))  
            
            #check the project name exists or not. 
            checkAlreayExists = request.app.database["project"].count_documents({"name": payload.name, "createdBy": userId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
           
            #If project name does not exists then raise the exception
            if (checkAlreayExists >=1) :
                raise exception(1010, constant.PROJECT_ALREADY_EXISTS.replace(constant.PLACEHOLDER_TEXT,payload.name))
            #Convert the json obj to bson to understand the mongoDB format.        
           
            if len(payload.userLists)!=0 :
                for userlist in payload.userLists:
                    if not (re.fullmatch(regex,userlist.userEmail)):
                        raise exception(1004,constant.INVALIDEMAIL)
                    if userlist.userEmail == userId:
                      raise exception(1035,constant.INVALID_USERID)
             
            body = jsonable_encoder(payload)         
            # body['createdOn']= datetime.utcnow()
            body['createdBy']= userId
            body["modifiedOn"] = None
            body["id"]=str(uuid.uuid4().hex)   
            new_project_info = request.app.database["project"].insert_one(body)         
            #To create the new project in MongoDB 
            created_project = request.app.database["project"].find_one(
                   {"_id": new_project_info.inserted_id},{"_id":0})                    
            return  created_project
        
        
       ## Search project
        def search_project(request:Request, tenantId:str, projectName:str, userId:str) -> dict:
            if (tenantId is None) and (projectName is None) :
              raise exception(1008, constant.PROJECTIDORNAME)         
                       
            if tenantId is not None:            
               #If project Id is not valid then raise exeption as invalid object ID            
               if not is_valid_uuid(tenantId):            
                 raise exception(1085, constant.IS_VALID_UUID)   
               # list of project as owner
               list1 = list(request.app.database["project"].find({"createdBy": userId, "tenantId":tenantId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})) 

               # list of project as userlists
               list2 = list(request.app.database["project"].find({"tenantId":tenantId, "userLists.userEmail": userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})) 

               project_detail = list1 + list2

            else:
                if(len(projectName)> int("25")):
                  raise exception(1006, constant.CHARVALIDATION)  
                project_detail= list(request.app.database["project"].find({"createdBy": userId, "name":{'$regex': projectName}, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0}))
            if len(project_detail)==0 :
                raise exception(1002, constant.PROJECT_NOT_FOUND)
            return project_detail
        
           ## get project
        def get_project(request:Request, projectId:str, userId:str) -> dict:             
             #If project Id is not valid then raise exeption as invalid object ID.           
            if not is_valid_uuid(projectId):              
              raise exception(1085, constant.IS_VALID_UUID)  
            
            project = request.app.database["project"].find_one({"id": projectId, "isDeleted":pydantic.parse_obj_as(bool,"false")})
            if project is None:
             raise exception(1002, constant.PROJECT_NOT_FOUND)
            else :
              chkOwnerPermission = request.app.database["project"].find_one({"id": projectId, "createdBy": userId, "isDeleted":pydantic.parse_obj_as(bool,"false")})
              if chkOwnerPermission is not None:
                   project_detail = request.app.database["project"].find_one(
                   {"id" : projectId,  "createdBy" : userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})
                   print("*****owner",project_detail)
                   return project_detail       
              else:
               project_detail = request.app.database["project"].find_one({"id" : projectId, "userLists.userEmail" : userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})
               print("*******user",project_detail)

               if project_detail is None:                
                    raise exception(1085,constant.PROJECT_NOT_FOUND)

            return project_detail
        
        ## List project - Get all the collections from project table. 
        def list_Projects(request:Request,tenantId:str, userId:str) -> dict:    
           
            chkUser =list(request.app.database["project"].find({"createdBy" : userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0}))

            if len(chkUser)==0:
              prjuser=list(request.app.database["project"].find({"tenantId":tenantId, "userLists.userEmail": userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0}))
              if len(prjuser)==0: 
                raise exception(1009, NOT_AUTHORIZED_ERROR)             

            # list of project as owner
            list1 = list(request.app.database["project"].find({"createdBy": userId, "tenantId":tenantId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})) 

            # list of project as userlists
            list2 = list(request.app.database["project"].find({"tenantId":tenantId, "userLists.userEmail": userId, "isDeleted":pydantic.parse_obj_as(bool,"false")},{"_id":0})) 
            listCollections = list1 + list2
            if listCollections is None:                
              raise exception(1085,constant.PROJECT_NOT_FOUND)
            return listCollections
               
        ## update project - Return false if an empty request body is sent.
        def update_project(request:Request, payload: UpdateProject, userId: str,):            

            if (payload.tenantId is None) or (payload.tenantId=='' ) :
              raise exception(1007, constant.TENANTID_NOT_PRESENT) 
            
            if not (is_valid_uuid(payload.tenantId)):
              raise exception(1007, constant.TENANTID_NOT_PRESENT)            
                   
            if (userId is None) or (userId=='' ) :
              raise exception(1094,constant.USERID) 
           
            if not (re.fullmatch(regex,userId)):
              raise exception(1004,constant.INVALIDEMAIL) 
            
            if (payload.description is None) or (payload.description =='' ) :
              raise exception(1095, constant.DESCRIPTION)                                     
            
            #check the project name is empty or not. 
            if (payload.name is None) or (payload.name =='' ) :
              raise exception(1008, constant.PROJECT_NAME_VALIDATION_ERROR)          
              
            if(len(payload.name)> int("25")):
             raise exception(1006, constant.CHARVALIDATION)   
            
            #check the project name is empty or not. 
            if (payload.id is None) or (payload.id =='' ) :
              raise exception(2003, constant.PROJECT_ID)  
                
            if not (is_valid_uuid(payload.id)) :                   
               raise exception(2003, constant.PROJECT_ID)              
               
            Tenant = request.app.database["tenant"].find_one(
                   {"id":  payload.tenantId, "isDeleted": pydantic.parse_obj_as(bool,"false")})
            if Tenant is None:
               raise exception(1032, TENANT_DET_NOT_FOUND_ERROR)
            
            project= request.app.database["project"].find_one(
                   {"id":  payload.id, "isDeleted": pydantic.parse_obj_as(bool,"false")}) 
            if project is None:
               raise exception(1002,constant.PROJECT_NOT_FOUND)      
            
            if(project['tenantId'] != payload.tenantId):
               raise exception(1099, constant.INVALID_TENANT.format(payload.name,payload.tenantId))
                        
          # checking user having permission in tenant or project
            Tenant = request.app.database["tenant"].find_one({"id":  payload.tenantId, "createdBy" : userId,"isDeleted": pydantic.parse_obj_as(bool,"false")})
            if Tenant is None:                         
               Tenant = request.app.database["tenant"].find_one({"id":  payload.tenantId, "userLists.userEmail" : userId, "userLists.permissions.createProject": pydantic.parse_obj_as(bool,"true"),"isDeleted": pydantic.parse_obj_as(bool,"false")})
               if Tenant is None:                    
                   check_project=request.app.database["project"].find_one({"id":  payload.id,"userLists.userEmail" : userId, "userLists.permissions.workspaceAdmin":pydantic.parse_obj_as(bool,"true"),"isDeleted": pydantic.parse_obj_as(bool,"false")})
                   if check_project is None:
                      raise exception(1045,constant.PERMISSION_NOT_FOUND_UPDATE.format(userId)) 
    
            if project['name']!=payload.name :
              #check the project name exists or not. 
              checkAlreayExists = request.app.database["project"].count_documents({"name": payload.name,"createdBy": userId, "isDeleted": pydantic.parse_obj_as(bool, "false")})
              #If project name does not exists then raise the exception
              if (checkAlreayExists >=1) :
                raise exception(1010, constant.PROJECT_ALREADY_EXISTS.replace(constant.PLACEHOLDER_TEXT,payload.name))
     
            jsonbody=jsonable_encoder(payload)             

            jsonbody["createdOn"]=project["createdOn"]
            jsonbody["createdBy"]=project["createdBy"]
            jsonbody["updatedBy"]=userId

            del jsonbody["id"]                   
            #update the project details. 
            if project:
              updated_project = request.app.database["project"].update_one({"id": payload.id}, {"$set": jsonbody})
            #get teh updated project. 
            updated_project = request.app.database["project"].find_one({"id":  payload.id},{"_id":0})          
            return updated_project
    
        # Delete a usecase from the database
        def delete_project(request:Request,projectId: str, userId:str):     
         
           #raise invalid object exception.              
          if  not is_valid_uuid(projectId):              
             raise exception(1085, constant.IS_VALID_UUID) 
           #check the tenant details are found or not.       
                       
          #check the project data
          project = request.app.database["project"].find_one({"id": projectId, "isDeleted":pydantic.parse_obj_as(bool,"false")})
          if project is None:
             raise exception(1002, constant.PROJECT_NOT_FOUND)
          else :
             chkOwnerPermission = request.app.database["project"].find_one({"id": projectId, "createdBy": userId, "isDeleted":pydantic.parse_obj_as(bool,"false")})
             if chkOwnerPermission is not None:
                request.app.database["project"].update_one({"id": projectId},{"$set":{"isDeleted":True, "updatedBy": userId, "modifiedOn": datetime.utcnow()}})
                return True         
             else:  #To check user Permission
               Tenant = request.app.database["tenant"].find_one(
                   {"id":  project["tenantId"], "userLists.userEmail" : userId, "userLists.permissions.deleteProject":pydantic.parse_obj_as(bool,"true"), "isDeleted":pydantic.parse_obj_as(bool,"false")})
               if Tenant is None:                
                    raise exception(1085,constant.PERMISSION_NOT_FOUND_DELETE.format(userId)) 
               else:
                   request.app.database["project"].update_one({"id": projectId},{"$set":{"isDeleted":True, "updatedBy": userId, "modifiedOn": datetime.utcnow()}})
                   return True                              