
# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""

app: Model Management service
fileName: main.py
description: Model Management Services provides a collection of REST APIs
    to manage and track the models on AI cloud which helps to automate the model deployment
    in machine learning.

"""
import uvicorn
from dotenv import dotenv_values
from typing import List
from fastapi import FastAPI, Cookie, status, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError

from aicloudlibs.db_management.core.db_utils import connect_mongodb, get_db
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.exceptions import global_exception_handler
from mms.config.logger import CustomLogger
from mms.routing import model_router
from mms.exception.exception import ModelException, ModelAPIException
from mms.constants.local_constants import *


NOT_AUTHORIZED_ERROR = 'Request Not Authorized. Please pass valid Auth token.'
config = dotenv_values(".env")
log = CustomLogger()

def getAuthSessionToken(authservice_session: str = Cookie(default=None)):

    if authservice_session is None:
        log.error('Request Not Authorized. Auth Token not passed.')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_AUTHORIZED_ERROR)

## initialize the app with openapi and docs url
enableAuthTokenFlg:str = config.get('ENABLE_GLOBAL_AUTHSESSION_TOKEN')
enableAuthTokenFlg = enableAuthTokenFlg if enableAuthTokenFlg is not None else 'N'
if enableAuthTokenFlg=='Y' :
    app = FastAPI(openapi_url="/api/v1/models/openapi.json", docs_url="/api/v1/models/docs",
                    dependencies=[Depends(getAuthSessionToken)], title='Model Management API')
else :
    app = FastAPI(openapi_url="/api/v1/models/openapi.json", docs_url="/api/v1/models/docs",
                    title='Model Management API')

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = connect_mongodb()
    app.database = get_db(app.mongodb_client)
    app.logger = log
    log.info("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

"""
    Adding the CORS Middleware wh/ich handles the requests from different origins

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

@app.exception_handler(ModelException)
async def model_exception_handler(request, exc):
    errRespArr = []
    log.error('Model API exception caught == %s',exc.detail, exc_info=True)
    apiErrResp = ApiErrorResponseModel(code=exc.code, status=HTTP_RESPONSE_STATUS_FAILED,
                message=exc.detail)
    errRespArr.append(apiErrResp)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(errRespArr)
    )

@app.exception_handler(ModelAPIException)
async def model_exception_handler(request, exc):
    errRespArr = []
    log.error('Model API exception caught == %s',exc.detail, exc_info=True)
    apiErrResp = ApiErrorResponseModel(code=exc.code, status=HTTP_RESPONSE_STATUS_FAILED,
                message=exc.detail)
    errRespArr.append(apiErrResp)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(errRespArr)
    )

"""
FAST API raise RequestValidationError in case request contains invalid data.
A global exception handler function to handle the requests which contains the invalid data
"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):

    return  global_exception_handler.validation_error_handler(exc)

@app.get('/ping', include_in_schema=False)
def healthProbeCheck(request: Request, response: Response) :
    return JSONResponse(
        status_code=200,
        content='Model Management API service is UP and running'
    )

"""
incude the routing details of model service
"""
app.include_router(model_router.router, prefix='/api/v1', tags=['Model Management'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
