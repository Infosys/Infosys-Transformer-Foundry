# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: project_appers.py
description: A Pydantic model object for project entity model 
             which maps the data model to the project entity schema
"""

from pydantic import BaseModel,Field,root_validator
from datetime import datetime
from typing import Optional, List,Union,Sequence
from aicloudlibs.schemas.global_schema import AuditableColumns,Compute,ResourceConfig,\
    StorageTypeEnum,Artifacts, NameValuePair,ApiResponse,ValidationError,ValidationTypeError
from enum import Enum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from aicloudlibs.constants.error_constants import *
from pydantic.error_wrappers import ErrorWrapper,ErrorList
import re
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
name_regex =  r'[a-zA-Z0-9-]+$'

class TenantPermissions(BaseModel):
    createProject: bool=Field(default=True)
    deleteProject: bool=Field(default=True)

class TenantUserList(BaseModel):
    userEmail: str=None
    permissions: TenantPermissions = None

class Tenant(AuditableColumns):
    name: str = None
    quotaConfig: ResourceConfig = None
    userLists: List[TenantUserList]=None
    #permission: TenantPermissions = None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props


    @root_validator(pre=True)
    def validateTenant(cls,values):
        errors=[]
        name=values.get("name")
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.TENANT_NAME_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 
        
        if (not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 

        resourceConfig=values.get("quotaConfig")
        resourceConfigEmptyErr=False
        if (resourceConfig is None or (resourceConfig is not None and len(resourceConfig) == 0)):
            error= ValidationError(ErrorCode.RESOURCECONFIG_EMPTY_ERROR)
            print(error)
            errors.append(error)
            resourceConfigEmptyErr=True
        if not resourceConfigEmptyErr:
             computeEmptyErr=False
             if(resourceConfig.get('volumeSizeinGB') is None):
                  error= ValidationError(ErrorCode.VOLUME_EMPTY_ERROR)
                  print(error)
                  errors.append(error)

                 
             if(resourceConfig.get('computes') is None or (resourceConfig.get('computes') is not None and len(resourceConfig.get('computes'))==0)):
                  error= ValidationError(ErrorCode.COMPUTE_LIST_EMPTY_ERROR)
                  print(error)
                  errors.append(error)
                  computeEmptyErr=True
             if(not computeEmptyErr):
                  computes=resourceConfig.get('computes')
                  for compute in computes:
                       gpumemryEmptyErr=False
                       computeTypeEmptyErr=False
                       computeTypeInstanceErr=False
                       if (compute.get('type') is None or (compute.get('type') is not None and  len(compute.get('type'))==0)):
                            error= ValidationError(ErrorCode.COMPUTE_TYPE_EMPTY_ERROR)
                            print(error)
                            errors.append(error)
                            computeTypeEmptyErr=True
                       if( not computeTypeEmptyErr and compute.get('type').lower() not in COMPUTE_TYPE_VALUES):
                             error= ValidationError(ErrorCode.COMPUTE_TYPE_VALUE_ERROR)
                             print(error)
                             errors.append(error)
                       if( not computeTypeEmptyErr and compute.get('type').lower() =='gpu' and  (compute.get('memory') is None or (compute.get('memory') is not None and len(compute.get('memory'))==0))):
                             error= ValidationError(ErrorCode.GPU_MEMORY_NOT_EMPTY)
                             print(error)
                             errors.append(error)
                             gpumemryEmptyErr=True
                             
                       if(not computeTypeEmptyErr and not gpumemryEmptyErr and compute.get('type').lower() =='gpu' and  compute.get('memory').lower() not in GPU_MEMORY_VALUES):
                             error= ValidationError(ErrorCode.GPU_MEMORY_VALUE_ERROR)
                             print(error)
                             errors.append(error)
                       if(not computeTypeEmptyErr and not (isinstance(compute.get('maxQty'),int) or isinstance(compute.get('minQty'),int))):
                             error= ValidationError(ErrorCode.RESOURCE_QTY_INSTANCE_ERROR)
                             print(error)
                             errors.append(error)
                             computeTypeInstanceErr=True
                             
                       if(not computeTypeEmptyErr and not computeTypeInstanceErr  and compute.get('maxQty') < compute.get('minQty')):
                             error= ValidationError(ErrorCode.RESOURCE_QTY_ERROR)
                             print(error)
                             errors.append(error) 
        
        userlst=values.get("userLists")

        if (not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 
        
        if len(userlst)>0:
             userEmailEmptyErr=False
             for user in userlst:
                if(user.get('userEmail') is None or (user.get('userEmail') is not None and len(user.get('userEmail'))==0)):
                    error= ValidationError(ErrorCode.USER_EMAIL_NOT_EMPTY)
                    print(error)
                    errors.append(error)
                    userEmailEmptyErr=True
                if(not userEmailEmptyErr and (not re.fullmatch(email_regex, user.get('userEmail')))):
                    error= ValidationError(ErrorCode.USER_EMAIL_INVALID)
                    print(error)
                    errors.append(error)
        
        if len(errors)>0:
            print(errors)
            # errorList=[]
            # for err in errors:
                
            #     errorList.append( ErrorWrapper(
            #     err,
            #     loc=('body', 'root')
            # ))
            # print(errorList)
            # print("********Sequence**********")
            # #print(Sequence[errorList])
            # print("**************")
            #raise RequestValidationError(errors=errorList)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values

class TenantStatusEnum(str,Enum):
    Created="Created"
    Deleted="Deleted"


class TenantResponseData(Tenant):
    id: str = None
    status: TenantStatusEnum = None
    currentResourceUsage: ResourceConfig = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class TenantResponse(ApiResponse):
    data: Optional[TenantResponseData] = None


class Permission(BaseModel):
      createPipeline : bool=Field(default=False)
      executePipeline: bool=Field(default=False)
      deployModel: bool=Field(default=False)
      #uploadDataset:bool=Field(default=False)
      view:bool=Field(default=True)
      workspaceAdmin:bool=Field(default=False)

class UserList(BaseModel):
    userEmail: str=None
    permissions: Permission = None

class Project(AuditableColumns):
    tenantId: str =None
    name: str=None
    description: str=None
    userLists: List[UserList]=None
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props 
    
    @root_validator(pre=True)
    def validateProject(cls,values):
        errors=[]
        tenantId=values.get("tenantId")
        if (tenantId is None or (tenantId is not None and len(tenantId) == 0)):
            error= ValidationError(ErrorCode.TENANT_ID_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 
        name=values.get("name")
        if (name is None or (name is not None and len(name) == 0)):
            error= ValidationError(ErrorCode.PROJECT_NAME_NOT_EMPTY_ERROR)
            print(error)
            errors.append(error) 

        userlst=values.get("userLists")

        if (not re.fullmatch(name_regex,name)):
            error= ValidationError(ErrorCode.SPECIAL_CHARS_ERROR)
            errors.append(error) 
        
        if len(userlst)>0:
             userEmailEmptyErr=False
             for user in userlst:
                if(user.get('userEmail') is None or (user.get('userEmail') is not None and len(user.get('userEmail'))==0)):
                    error= ValidationError(ErrorCode.USER_EMAIL_NOT_EMPTY)
                    print(error)
                    errors.append(error)
                    userEmailEmptyErr=True
                if(not userEmailEmptyErr and (not re.fullmatch(email_regex, user.get('userEmail')))):
                    error= ValidationError(ErrorCode.USER_EMAIL_INVALID)
                    print(error)
                    errors.append(error)
                
             
        
        if len(errors)>0:
            print(errors)
            raise RequestValidationError(errors=[
            ErrorWrapper(
                error,
                loc=('body', 'root'),
            ),
        ])
        else:
            return values


class UpdateProject(Project):
    id: str = None

class ProjectStatusEnum(str,Enum):
    Created="Created"
    Updated="Updated"
    Deleted="Deleted"

class ProjectResponseData(Project):
    id: str = None
    status: ProjectStatusEnum = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        @staticmethod
        def schema_extra(schema: dict, _):
            
            props = {}
            for k, v in schema.get('properties', {}).items():
                 props[k] = v
            schema["properties"] = props

class ProjectResponse(ApiResponse):
    data: Optional[ProjectResponseData] = None

class DeleteProjectResponse(BaseModel):
    data: Optional[str] = None

class DeleteTenantResponse(ApiResponse):
    data: Optional[str] = None

class GetProjectResponseData(BaseModel):
     project: Optional[ProjectResponseData] = None

class GetPipelineResponse(ApiResponse):
    data: Optional[GetProjectResponseData] = None


class ListProjectResponseData(BaseModel):
     projects: Optional[List[ProjectResponseData]] = None

class ListProjectResponse(ApiResponse):
    data: Optional[ListProjectResponseData] = None


def ResponseModel(data):
    api_response=ApiResponse(code=200, status="SUCCESS",
                data=data)
    return api_response  