# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import time
import datetime
import calendar
from typing import List
import uvicorn
from fastapi import FastAPI, APIRouter, Body, HTTPException as StarletteHTTPException, status, Request, Response, Cookie, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from common.ainauto_logger_factory import AinautoLoggerFactory
from common.app_config_manager import AppConfigManager
from data.api_schema_data import GetProjectIdResultData
from routes.api import router as api_router
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from aicloudlibs.db_management.core.db_utils import connect_mongodb, get_db
from pipeline.config.logger import CustomLogger
from aicloudlibs.exceptions import global_exception_handler

app_config = AppConfigManager().get_app_config()
logger = AinautoLoggerFactory().get_logger()

log = CustomLogger()

app = FastAPI(title='Generic Pipeline Management Service (GPMS)', openapi_url="/api/v2/pipelines/openapi.json", docs_url="/api/v2/pipelines/docs", description="Infosys AIcloud Pipeline Service", version=app_config['DEFAULT']['service_version'])

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to connect to the MongoDB database
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = connect_mongodb()
    app.database = get_db(app.mongodb_client)
    app.logger = log
    log.info("Connected to the MongoDB database!")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return global_exception_handler.validation_error_handler(exc)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=int(app_config['DEFAULT']['port']), log_level=int(app_config['DEFAULT']['logging_level']), reload=True)
    logger.info("App is running....")