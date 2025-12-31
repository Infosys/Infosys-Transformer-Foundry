# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

import time
import datetime
import calendar
from typing import List
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from common.ainauto_logger_factory import AinautoLoggerFactory
from common.app_config_manager import AppConfigManager
from data.api_schema_data import ResponseDataList
from dependencies import basic_authorize
from routes.api import router as api_router
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app_config = AppConfigManager().get_app_config()
logger = AinautoLoggerFactory().get_logger()

# Create FastAPI app
app = FastAPI(title='Transformer Studio Service (TSS)',
              #   dependencies=[Depends(basic_authorize)],
              openapi_url="/tfstudioservice/api/v1/pipelines/openapi.json", docs_url="/tfstudioservice/api/v1/pipelines/docs",
              description="Infosys AIcloud Transformer Studio Service",
              version=app_config['DEFAULT']['service_version'])

# CORS
origins = [
    "*"
]

# Exception handling for RequestValidationError
@app.exception_handler(RequestValidationError)
def http_exception_handler(request: Request, exc: RequestValidationError):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    # print(exc.errors())
    response_list = []
    for index, err in enumerate(exc.errors()):
        print(err)
        response_dict = {
            "code": err['type'].split('.')[1],
            "message": err['msg']
        }
        response_list.append(response_dict)
        # TODO: It's defect-multiple error return only last error raised
        break
    elapsed_time = round(time.time() - start_time, 3)
    response = ResponseDataList(response=response_list,
                                responseCde=999, responseMsg="Failure",
                                timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))

    json_compatible_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_data)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host=app_config['DEFAULT']['host'], port=int(app_config['DEFAULT']['port']),
                log_level=int(app_config['DEFAULT']['logging_level']), reload=True)
    logger.info("App is running....")
