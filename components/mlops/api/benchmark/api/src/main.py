# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
app: Benchmark Management service 
fileName: main.py
description: Benchmark management services helps to benchmark the model.

"""
from dotenv import dotenv_values, find_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Body, HTTPException as StarletteHTTPException, status, Request, Response, Cookie, Depends
from fastapi.exceptions import RequestValidationError
from aicloudlibs.db_management.core.db_utils import connect_mongodb, get_db
from aicloudlibs.exceptions import global_exception_handler
from pipeline.config.logger import CustomLogger
from pipeline.routing import pipeline_router
from fastapi.responses import JSONResponse
from aicloudlibs.utils import *

router = APIRouter()
dotenv_path = find_dotenv()

log = CustomLogger()

NOT_AUTHORIZED_ERROR = 'Request Not Authorized. Please pass valid Auth token.'
config = dotenv_values(dotenv_path)


def getAuthSessionToken(authservice_session: str = Cookie(default=None)):
    log.info('authservice_session == %s', authservice_session)
    if authservice_session is None:
        log.error('Request Not Authorized. Auth Token not passed.')
        raise StarletteHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_AUTHORIZED_ERROR)

enableAuthTokenFlg: str = config.get('ENABLE_GLOBAL_AUTHSESSION_TOKEN')
enableAuthTokenFlg = enableAuthTokenFlg if enableAuthTokenFlg is not None else 'N'
if enableAuthTokenFlg == 'Y':
    app = FastAPI(openapi_url="/api/v1/benchmarks/openapi.json", docs_url="/api/v1/benchmarks/docs", dependencies=[Depends(getAuthSessionToken)])
else:
    app = FastAPI(openapi_url="/api/v1/benchmarks/openapi.json", docs_url="/api/v1/benchmarks/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = connect_mongodb()
    app.database = get_db(app.mongodb_client)
    app.logger = log
    log.info("Connected to the MongoDB database!")

"""
A global exception handler function to handle the http exception
"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return global_exception_handler.validation_error_handler(exc)

@app.get('/ping', include_in_schema=False)
def healthProbeCheck(request: Request, response: Response):
    return JSONResponse(status_code=200, content='Benchmark Pipeline Management API is UP and running')

app.include_router(pipeline_router.router, prefix='/api/v1', tags=['Benchmark Pipeline Management Services'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)