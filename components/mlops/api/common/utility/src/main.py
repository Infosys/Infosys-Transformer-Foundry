# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
app: AICloud Utility Services
fileName: main.py
description:
"""

from typing import List
import uvicorn
from fastapi import Depends, FastAPI,  Request, Response, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from aicloudlibs.db_management.core.db_utils import get_db,connect_mongodb
from aicloudlibs.exceptions import global_exception_handler
from utilities.config.logger import CustomLogger
from utilities.routing import utility_router

log = CustomLogger()

## initialize the app with openapi and docs url
app = FastAPI(openapi_url="/api/v1/utilities/openapi.json", docs_url="/api/v1/utilities/docs")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = connect_mongodb()
    app.database = get_db(app.mongodb_client)
    log.info("Connected to the MongoDB database!")
    app.logger=log

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

"""
FAST API raise RequestValidationError in case request contains invalid data.
A global exception handler function to handle the requests which contains the invalid data

"""
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return  global_exception_handler.validation_error_handler(exc)

"""
A global exception handler function to handle the http exception
"""
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return  global_exception_handler.http_exception_handler(exc)

"""
incude the routing details of model service
"""
app.include_router(utility_router.router, prefix='/api/v1', tags=['Utility Services'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)