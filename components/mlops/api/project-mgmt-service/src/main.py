# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from fastapi import FastAPI 
from dotenv import dotenv_values 
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Cookie,Depends 
import tenants.routing.tenants_routing as tenants_routing
import projects.routing.projects_routing as projects_routing
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware   
from tenants.config.logger import CustomLogger
from tenants.exception.exception import TenantsException
from projects.exception.exception import projectException 
from tenants.service.service import TenantsService as service
from dotenv import find_dotenv 
from aicloudlibs.db_management.core.db_utils import connect_mongodb,get_db
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse 
from aicloudlibs.exceptions import global_exception_handler  

router = APIRouter() 
NOT_AUTHORIZED_ERROR = 'Request Not Authorized. Please pass valid Auth token.'
dotenv_path = find_dotenv() 
config = dotenv_values(dotenv_path)
log = CustomLogger()

def getAuthSessionToken(authservice_session: str = Cookie(default=None)):
    if authservice_session is None:
        log.error('Request Not Authorized. Auth Token not passed.')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_AUTHORIZED_ERROR)

## initialize the app with openapi and docs url
enableAuthTokenFlg:str = config.get('ENABLE_GLOBAL_AUTHSESSION_TOKEN')
enableAuthTokenFlg = enableAuthTokenFlg if enableAuthTokenFlg is not None else 'N'
if enableAuthTokenFlg=='Y' :
    app = FastAPI(openapi_url="/api/v1/projects/openapi.json", docs_url="/api/v1/projects/docs", dependencies=[Depends(getAuthSessionToken)])
else :
    app = FastAPI(openapi_url="/api/v1/projects/openapi.json", docs_url="/api/v1/projects/docs")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client =connect_mongodb()     
    app.database = get_db(app.mongodb_client)
    app.logger = log
    log.info("Connected to the MongoDB database!")   

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

"""

    Adding the CORS Middleware which handles the requests from different origins

    allow_origins - A list of origins that should be permitted to make cross-origin requests.
                    using ['*'] to allow any origin
    allow_methods - A list of HTTP methods that should be allowed for cross-origin requests.
                    using ['*'] to allow all standard method
    allow_headers - A list of HTTP request headers that should be supported for cross-origin requests. 
                    using ['*'] to allow all headers
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=2048)

"""
FAST API raise RequestValidationError in case request contains invalid data.
A global exception handler function to handle the requests which contains the invalid data

"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return global_exception_handler.validation_error_handler(exc)      
    
"""
A global exception handler function to handle the http exception
"""
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
     return  global_exception_handler.http_exception_handler(exc)

@app.exception_handler(TenantsException)
async def usecase_exception_handler(request, exc):
    errRespArr = []
    apiErrResp = service.ErrorResponseModel(code=exc.code, message=exc.detail)
    errRespArr.append(apiErrResp)
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(errRespArr))

@app.exception_handler(projectException)
async def project_exception_handler(request, exc):
    errRespArr = []
    apiErrResp = service.ErrorResponseModel(code=exc.code, message=exc.detail)
    errRespArr.append(apiErrResp)
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(errRespArr))

@app.get('/ping', include_in_schema=False)
def healthProbeCheck(request: Request, response: Response) :
    return JSONResponse(
        status_code=200,
        content='Project Management API service is UP and running.'
    )

app.include_router(tenants_routing.router, prefix='/api/v1', tags=['Tenant Management']) 
app.include_router(projects_routing.router, prefix='/api/v1', tags=['Project Management'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)