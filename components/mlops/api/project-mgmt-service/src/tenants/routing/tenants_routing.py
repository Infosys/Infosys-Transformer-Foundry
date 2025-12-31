# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""  
fileName: tenants_routing.py
description: Routing details for Tenants CRUD operations

"""
from fastapi import Depends,Request, Response,APIRouter, HTTPException,Body,status, Cookie, Header 
from tenants.service.service import TenantsService as service
from tenants.exception.exception import TenantsException
import tenants.constants.local_constants as constants  
import pydantic 
from bson import ObjectId
from aicloudlibs.schemas.project_mappers import *
from aicloudlibs.constants.http_status_codes import HTTP_NOT_AUTHORIZED_ERROR,HTTP_STATUS_INTERNAL_SERVER_ERROR
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException,InternalServerException

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str 
router = APIRouter()

"""
method: Create Tenants 
description: Defines the routing path details for create tenant operation and invokes the create tenant service.

params:
   :payload - A pydantic model object for input payload 
returns:
   :tenant - A pydantic model object for output with tenant id

exceptions:
    :TenantException - handles the tenants specific exception thrown by create tenant service         
"""         
@router.post('/tenants', response_model=TenantResponse,  name="Create Tenant API", description="Create a tenant in AICloud", include_in_schema=False)
def create_tenants(request:Request, userId: str = Header(convert_underscores=False), body: Tenant = Body(...)) -> TenantResponseData:     
   try:    
    log = request.app.logger        
    log.info(constants.PROJECTMEMTSERVICE + "["+"create_tenants()"+"]["+userId+"]")           
    tenants_detail = service.create_tenants(request, userId, body)  
    log.info("Response: "+str(tenants_detail))     
    TenantResponse.data =  tenants_detail   
    responseDict = TenantResponse.__dict__       
    return responseDict 
   
   except TenantsException as tenanatsException:
      log.error(tenanatsException.__dict__)
      raise HTTPException(**tenanatsException.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__) 
     
"""
method: Delete Tenant 
description: Defines the routing path details to delete the Tenant
params:
   :payload - TenantId and userId as parameter.    
returns:
   :message
exceptions:
    :TenantException - handles the Usecase specific exception thrown by update tenant service         
"""
@router.delete('/tenants/{tenantId}', name="Delete tenant API",  description="Delete the tenant based on tenantId and userId.", include_in_schema=False)
def delete_tenant(request:Request, tenantId: str, userId: str = Header(convert_underscores=False)): 
   try:   
    log = request.app.logger
    log.debug("delete_tenant() - request tenant id: "+ str(tenantId) + str(userId))  
    deleted_tenant = service.delete_tenant(request,tenantId, userId)
    log.debug("delete_tenanat() - Response tenant id: "+ str(deleted_tenant))    
    return service.ResponseModel(status.HTTP_204_NO_CONTENT, constants.DELETE_TENANT.format(tenantId))
   
   except TenantsException as tenanatsException:
      log.error(tenanatsException.__dict__)
      raise HTTPException(**tenanatsException.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)

"""
method: Get Tenant 
description: Defines the routing path details for get tenant operation and invokes the get tenant service.

params:
   :id - tenant specific id  
returns:
   :tenant - A pydantic model object for output with tenant id

exceptions:
    :tenantException - handles the tenant specific exception thrown by get tenant service
         
"""
@router.get('/tenants/{tenantId}', name="get Tenant API", description="get the tenant details based on tenant ID")  
def get_tenant(request:Request,response: Response, tenantId: str, userId: str = Header(convert_underscores=False))-> dict:   
   try:
    log = request.app.logger       
    log.info("Get_tenant - request tenant  id: "+ str(tenantId)+str(userId)) 
    tenant = service.get_tenant(request,tenantId,userId)
    return ResponseModel({"tenant":tenant})

   except TenantsException as tenanatsException:
      log.error(tenanatsException.__dict__)
      raise HTTPException(**tenanatsException.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)