# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: pipeline_router.py
description: Routing details for Pipeline CRUD operations

"""
import json
from bson import json_util, ObjectId
from fastapi import Request, Header, Response, Query
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Request, APIRouter, HTTPException
from aicloudlibs.schemas.pipeline_mappers import PipelineJobDetails, ResponseModel, \
    ListPipelineResponse, DeletePipelineResponse, GetPipelineResponse
from aicloudlibs.schemas.global_schema import NotAuthorizedError, InternalServerError
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException
from aicloudlibs.constants.http_status_codes import HTTP_NOT_AUTHORIZED_ERROR, HTTP_STATUS_INTERNAL_SERVER_ERROR
from pipeline.exception.exception import PipelineException
from aicloudlibs.schemas.benchmark_pipeline_mappers import *
from pipeline.service.pipeline_service import PipelineService as service, BaseService
import pipeline.constants.local_constants as constant
from pipeline.util.log_formatter import LogFormatter
from typing import List, Optional

router = APIRouter()
log_formatter = LogFormatter('Benchmark Management')

def _get_encoded_response(data: dict):
    dumped_data = json_util.dumps(data, indent=4, default=json_util.default)
    page_sanitized = json.loads(dumped_data, object_hook=json_util.object_hook)
    return page_sanitized

# To Execute the benchmark with respective model and dataset details in the payload.
@router.post("/benchmarks",response_model=PipelineResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def create_benchmark_pipeline(request: Request, payload: BenchmarkPipeline, userId: str = Header(convert_underscores=False)):

    prefix = constant.LOG_PREFIX.format("Benchmark Management", "createBenchmark " + "{senderURI }" + "{RequestID }", str(userId), str(BenchmarkPipeline))
    log = request.app.logger
    try:
        log.info(constant.LOG_FORMAT.format(prefix, f"create_pipeline - request : " + str(BenchmarkPipeline)))
        service_obj = service(request.app)
        pipeline_detail = service_obj.create_pipeline(payload, userId)
        log.debug("response : " + str(pipeline_detail))
        PipelineResponse.code = 200
        PipelineResponse.status = "Success"
        PipelineResponse.data = jsonable_encoder(pipeline_detail)
        responseDict = PipelineResponse.__dict__
        return responseDict

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    
# To get the status of the executed benchmark with benchmarkId and userId
@router.get("/benchmarks/{benchmarkId}", response_model=GetBenchmarkStatusResponse, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
async def getBenchmarkStatus(request:Request,response: Response,benchmarkId: str, userId: str = Header(convert_underscores=False)):

    log = request.app.logger
    log_formatter.set_prefixes('benchmarkstatus Pipeline', userId, 'NA')
    try:
        service_obj = service(request.app)
        benchmarkStatusdetails = service_obj.getBenchmarkStatus(request, benchmarkId, userId)
        log.debug(log_formatter.get_msg(f"response : {str(benchmarkStatusdetails)}"))
        GetBenchmarkStatusResponse.code=200
        GetBenchmarkStatusResponse.status="Success"
        GetBenchmarkStatusResponse.data = jsonable_encoder(benchmarkStatusdetails)
        responseDict = GetBenchmarkStatusResponse.__dict__
        return responseDict
    
    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)
    
# To get the task/modelGenArgs for benchmark w.r.t benchmarkType and metadataType
@router.get("/benchmarks/metadata/taskargs")
async def list_benchmark_metadata(request: Request,benchmarkType: Benchmarktype , metadataType: Metadatatype, userId: str = Header(convert_underscores=False)):

    prefix = constant.LOG_PREFIX.format("Pipeline Management", "createPipeline " + "{senderURI }" + "{RequestID }", str(userId), str(PipelineJobDetails))
    log = request.app.logger
    try:
        service_obj = service(request.app)
        list_benchmark = service_obj.list_benchmark_metadata(request,benchmarkType,metadataType,userId)   
        if metadataType._value_=="task":
            responseDict=ListBenchmarkMetadata(data ={'tasks':list_benchmark})
        else:
            responseDict=ListBenchmarkMetadata(data ={'modelGenArgs':list_benchmark})
        return responseDict

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To get the dataset for benchmark w.r.t benchmarkType and task
@router.get("/benchmarks/metadata/data")
async def list_dataset(request: Request,benchmarkType: Benchmarktype , task: str, userId: str = Header(convert_underscores=False)):

    prefix = constant.LOG_PREFIX.format("Benchmark Management", "createBenchmark" + "{senderURI }" + "{RequestID }", str(userId), str(PipelineJobDetails))
    log = request.app.logger
    try:
        service_obj = service(request.app)
        list_benchmark = service_obj.list_dataset(request,benchmarkType,task,userId)      
        responseDict=ListBenchmarkMetadata(data ={'datasets':list_benchmark})
        return responseDict

    except PipelineException as pipelineException:
        log.error(log_formatter.get_msg(str(pipelineException.__dict__)))
        raise HTTPException(**pipelineException.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)

# To get the list of benchmark associated with given projectId and userId
@router.get("/benchmarks", response_model=dict, responses={HTTP_NOT_AUTHORIZED_ERROR: {"model": NotAuthorizedError}, HTTP_STATUS_INTERNAL_SERVER_ERROR: {"model": InternalServerError}})
def list_benchmark(request: Request, projectId: str, userId: str = Header(convert_underscores=False)):

    log = request.app.logger
    log_formatter.set_prefixes('list benchmarkPipeline', userId, 'NA')
    try:
        log.info(log_formatter.get_msg(f"list_pipeline - request : {str(projectId)} {str(userId)}"))
        service_obj = service(request.app)
        benchmark_list = service_obj.list_benchmark(request, projectId, userId)
        log.debug(log_formatter.get_msg("response : " + str(benchmark_list)))
        response = {"code" : 200, "status": "Success", "data" :benchmark_list}
        responseDict = jsonable_encoder(response)
        return responseDict

    except PipelineException as error:
        log.error(log_formatter.get_msg(str(error.__dict__)))
        raise HTTPException(**error.__dict__)
    except ForbiddenException as fe:
        raise HTTPException(**fe.__dict__)
    except InternalServerException as internalEx:
        raise HTTPException(**internalEx.__dict__)
    except NotFoundException as nfe:
        raise HTTPException(**nfe.__dict__)