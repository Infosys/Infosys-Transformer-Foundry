# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
app: Prompt Library service 
fileName: main.py

"""
from dotenv import dotenv_values, find_dotenv
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI, APIRouter, Body, HTTPException as StarletteHTTPException, status, Request, Response, Cookie, Depends
from fastapi.exceptions import RequestValidationError
from aicloudlibs.db_management.core.db_utils import connect_mongodb, get_db
from aicloudlibs.exceptions import global_exception_handler
from prompt.config.logger import CustomLogger
from prompt.routing import promptlib_router
from fastapi.responses import JSONResponse
from aicloudlibs.utils import *

router = APIRouter()
dotenv_path = find_dotenv()

log = CustomLogger()

NOT_AUTHORIZED_ERROR = 'Request Not Authorized. Please pass valid Auth token.'
config = dotenv_values(dotenv_path)

app = FastAPI(openapi_url="/api/v1/library/openapi.json", docs_url="/api/v1/library/docs", title="Prompt Library Service",)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=2048)

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
    print("IN MAIN VALIDATE")
    return global_exception_handler.validation_error_handler(exc)


@app.get('/ping',tags=["Health Check"])
def healthProbeCheck(request: Request, response: Response):
    return JSONResponse(status_code=200, content='Prompt Library API service is UP and running')

app.include_router(promptlib_router.router, prefix='/api/v1/library', tags=['Prompt Management'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)