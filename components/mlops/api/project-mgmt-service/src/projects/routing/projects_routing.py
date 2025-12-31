# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: Router.py
description: Routing details for Usecase CRUD operations
"""
from fastapi import Depends,Request, Response,APIRouter, HTTPException,Body,status, Header 
from projects.service.service import projectService as service  
from projects.exception.exception import projectException
from projects.mappers.mappers import *  
from typing import Union 
from bson import   ObjectId
import projects.constants.local_constants as constants 
import pydantic 
from bson import ObjectId
from aicloudlibs.schemas.project_mappers import Project, UpdateProject
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException,InternalServerException

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str 
router = APIRouter()

"""
method: Create project 
description: Defines the routing path details for create project operation and invokes the create project service.

params:
   :payload - A pydantic model object for input payload
   :db_session - invokes the get_db funstion and get the db session object
returns:
   :project - A pydantic model object for output with project and usecase id

exceptions:
    :projectException - handles the project specific exception thrown by create project service
         
"""
@router.post('/projects', status_code=status.HTTP_201_CREATED, name="Create Project API", description="Create Project under specific tenant") 
def create_project(request:Request,response: Response, body: Project = Body(...), userId: str = Header(convert_underscores=False)) -> dict:     
   try:
    log = request.app.logger   
    log.info(constants.PROJECTMEMTSERVICE + "["+"Create Project()"+"]["+userId+"]")                  
    project_detail = service.create_project(request,userId,body)   
    log.debug("response : "+ str(project_detail))
    response.status_code=status.HTTP_201_CREATED 
    return ResponseModel(status.HTTP_201_CREATED ,project_detail)    
   
   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)
 
"""
method: Search project 
description: Defines the routing path details for get project operation and invokes the get project service.

params:
   :id - project specific id  
returns:
   :project - A pydantic model object for output with project id

exceptions:
    :projectException - handles the project specific exception thrown by get project service
         
"""
@router.get('/projects/search', name="Search Project API", description="Search the project based on given search data.")  
def Search_project(request:Request,response: Response, tenantId: Union[str,None]=None, name: Union[str,None]=None, userId: str = Header(convert_underscores=False))-> dict:   
   try:
    log = request.app.logger       
    log.debug("Search_project - request project  id: "+ str(tenantId)+ str(name) + userId )
    projects = service.search_project(request,tenantId,name, userId)     
    return ResponseModel(status.HTTP_200_OK ,{"projects":projects})  
   
   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)

"""
method: Get project 
description: Defines the routing path details for get project operation and invokes the get project service.

params:
   :id - project specific id  
returns:
   :project - A pydantic model object for output with project id

exceptions:
    :projectException - handles the project specific exception thrown by get project service
         
"""
@router.get('/projects/{projectId}', name="get Project API", description="get the project details based on project ID")  
def get_project(request:Request,response: Response, projectId: str, userId: str = Header(convert_underscores=False))-> dict:   
   try:
    log = request.app.logger       
    log.info("Get_project - request project  id: "+ str(projectId)+str(userId)) 
    project = service.get_project(request,projectId, userId)      
    if len(project)==0 :       
       return ErrorResponseModel(1002, constants.PROJECT_NOT_FOUND)  
    return ResponseModel(status.HTTP_200_OK,{"project":project})

   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)
 
"""
method: List Projects for specific tenant
description: Defines the routing path details for list tenant operation and invokes the list tenant service.

params:

   :db_session - invokes the get_db funstion and get the db session object
returns:
   :tenant - A list of project pydantic model object 

exceptions:
    :tenantException - handles the tenant specific exception thrown by list tenant service
         
"""
@router.get('/tenants/{tenantId}/projects', response_description="projects retrieved",  name="List Projects API" ,description="List all the projects based on user id / requested user or  tenanat Id.") 
def list_projects( request:Request, response: Response, tenantId: str, userId: str = Header(convert_underscores=False))-> dict: 
   try:
    log = request.app.logger    
    log.info("List Projects for specific tenantId/userId " +str(userId) + str(tenantId))
    projectList = service.list_Projects(request,tenantId,userId)          
    response.status_code=status.HTTP_200_OK  
    if len(projectList)==0 :     
       return ErrorResponseModel(1002, constants.PROJECT_NOT_FOUND)
    return ResponseModel(status.HTTP_200_OK,{"projects": projectList})

   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)

"""
method: update project 
description: Defines the routing path details for update project operation and invokes the update project service.

params:
   :payload - A pydantic model object for input payload 
returns:
   :project - project object with updated details
exceptions:
    :projectException - handles the project specific exception thrown by update project service
         
"""
@router.put('/projects', name="Update Project API", description="Update Project for specific tenanat") 
def update_project(request:Request, response: Response,  body: UpdateProject = Body(...),userId: str = Header(convert_underscores=False)):    
   try:
    log = request.app.logger
    log.info("update_project - " + str(userId))
    updated_project = service.update_project(request, body, userId)
    log.debug("response : update_project "+ str(updated_project)) 
    if updated_project:
       response.status_code=status.HTTP_201_CREATED       
       return ResponseModel(status.HTTP_201_CREATED, updated_project)
    
   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)     
     
"""
method: Delete project 
description: Defines the routing path details for update project operation and invokes the update project service.params:
   :payload - id as parameter.    
returns:
   :message
exceptions:
    :projectException - handles the project specific exception thrown by update project service         
"""

@router.delete("/projects/{projectId}", name="Delete Project API", description="Delete Project for specific tenant")
def delete_project(request:Request,response: Response,projectId: str, userId: str = Header(convert_underscores=False)):
   try:
    log = request.app.logger
    log.info("delete_project - Requested ProjectID " + str(projectId)+str(userId)) 
    deleted_project = service.delete_project(request,projectId, userId)
    log.info("response:delete_project() "+str(deleted_project))
    if deleted_project:
       response.status_code=status.HTTP_200_OK            
       return ResponseModel(status.HTTP_200_OK,constants.REMOVED_PROJECT.format(projectId))
    return ErrorResponseModel(404, constants.DOES_NOT_EXIT.format(projectId)) 
               
   except projectException as projectExc:
      log.error(projectExc.__dict__)
      raise HTTPException(**projectExc.__dict__)
   except ForbiddenException as fe:
      raise ForbiddenException(**fe.__dict__)
   except InternalServerException as InternalEx:
      raise HTTPException(**InternalEx.__dict__)
   except NotFoundException as nfe:
      raise HTTPException(**nfe.__dict__)