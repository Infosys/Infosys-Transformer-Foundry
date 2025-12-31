# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from abc import ABC
from aicloudlibs.constants.http_status_codes import HTTP_STATUS_NOT_FOUND,HTTP_NOT_AUTHORIZED_ERROR,HTTP_STATUS_INTERNAL_SERVER_ERROR,HTTP_STATUS_BAD_REQUEST
from aicloudlibs.schemas.global_schema import ApiErrorResponseModel
from fastapi.encoders import jsonable_encoder
from aicloudlibs.constants.error_constants import ErrorCode
from aicloudlibs.constants.util_constants import MLOPS_SERVICES
from aicloudlibs.utils.apiDbUtils import APIDBUtils
from aicloudlibs.utils.apiUtils import checkForQuota,getGPUQuotaDetails,getCPUQuotaDetails,updateCurrentResourceUsage
import pydantic
from datetime import datetime
from aicloudlibs.exceptions.global_exception import DiskQuotaException,InvalidComputeTypeException,GpuQuotaException,CpuQuotaException,MemoryQuotaException,QuotaExceedException,NotFoundException,BusinessException

class GlobalValidations(object):  

    @staticmethod
    def hasAccess(userId,projectId,serviceName):
       
        projectDet=APIDBUtils.findOneById("project",projectId)
        haveAccess= False
        if len(serviceName)>0 and serviceName in MLOPS_SERVICES:  
            if projectDet['createdBy'] == userId:
                    haveAccess = True
            else:
                accessLists = projectDet['userLists']
                if accessLists:
                    for user in accessLists:
                        if userId == user['userEmail']:
                            userPerm = user['permissions']
                            if userPerm and (userPerm.get(serviceName, False) == True or userPerm.get('workspaceAdmin', False) == True):
                                haveAccess = True
                                print("User have access to the trial ID")
                                break
        return haveAccess
    
    @staticmethod
    def isQuotaExceeded(userId,projectId,resourceQuotaReq):
        projectDet=APIDBUtils.findOneById("project",projectId)
        tenantId=projectDet['tenantId']
        tenantDetails=APIDBUtils.findOneById("tenant",tenantId)
        currentResourceUsage=tenantDetails['currentResourceUsage']
        resourceConfig=tenantDetails['quotaConfig']  
        requestedDiskSpace=resourceQuotaReq['volumeSizeinGB']
        totalDiskSpace=resourceConfig['volumeSizeinGB']
        currentDiskSpace=currentResourceUsage['volumeSizeinGB']
        is_diskspace_available=False
        is_gpu_available=False
        is_cpu_available=False
        is_memory_available=False
        is_diskspace_available=checkForQuota(totalDiskSpace,currentDiskSpace,requestedDiskSpace)
        if (is_diskspace_available):
            print("computetype is_diskspace_available")
            print(is_diskspace_available)
            computes=resourceQuotaReq['computes']
            resType=""
            reqType=""
            for compute in computes:
               if compute['type'].lower() == "gpu":
                  print("computetype GPU")
                  if resType == "":
                      resType="1"
                      reqType="gpu"
                  else:
                      resType="2"
                  reqMinQty= int(compute['minQty'])
                  reqMaxQty= int(compute['maxQty'])
                  reqGPUMemory=compute['memory']
                  currentMinVal,currentMaxVal=getGPUQuotaDetails(reqGPUMemory,currentResourceUsage['computes'],"gpu")
                  totalMinVal,totalMaxVal=getGPUQuotaDetails(reqGPUMemory,resourceConfig['computes'],"gpu")
                  is_gpu_available=checkForQuota(totalMaxVal,currentMaxVal,reqMaxQty)  
                  totalGpu=totalMaxVal
                  currentGpu=currentMaxVal
                  print(is_gpu_available)
               elif compute['type'].lower() == "cpu":
                   print("computetype CPU") 
                   if resType == "":
                      resType="1"
                      reqType="cpu"
                   else:
                      resType="2"        
                   reqMinQty= int(compute['minQty'])
                   reqMaxQty= int(compute['maxQty'])
                   reqCPUMemory=compute['memory']
                   
                   currentMinVal,currentMaxVal,currentMemory=getCPUQuotaDetails(currentResourceUsage['computes'])
                   totalMinVal,totalMaxVal,totalMemory=getCPUQuotaDetails(resourceConfig['computes'])
                   is_cpu_available=checkForQuota(totalMaxVal,currentMaxVal,reqMaxQty)
                   totalCpu=totalMaxVal
                   currentCpu=currentMaxVal
                   
                   if reqCPUMemory =='' :
                       reqCPUMemory=0
                   elif currentMemory == '':
                       currentMemory=0
                   elif totalMemory == '':
                       totalMemory=0

                   reqCPUMemory=reqCPUMemory.lower().replace("gb","")
                   
                   is_memory_available=checkForQuota(totalMemory,currentMemory,int(reqCPUMemory))
                   totalMem=totalMemory
                   currentMem=currentMemory
               else:
                   raise InvalidComputeTypeException()           
        else:
            raise DiskQuotaException(totalDiskSpace,currentDiskSpace)
        
        if is_diskspace_available and is_gpu_available and resType == "1":
            return True
        elif is_diskspace_available and is_gpu_available and is_cpu_available and is_memory_available and resType == "2":
            return True
        elif is_diskspace_available and  is_cpu_available and is_memory_available and resType == "1":
            return True
        
        else:
            
            if reqType=="gpu"and not is_gpu_available and resType == "1":
                 raise GpuQuotaException(totalGpu,currentGpu)
            if reqType=="cpu"and not is_cpu_available and resType == "1":
                 raise CpuQuotaException(totalCpu,currentCpu)
            elif reqType=="cpu"and not is_memory_available and resType == "1":
                 raise MemoryQuotaException(totalMem,currentMem)
            elif (resType == "2" and is_gpu_available and is_cpu_available and not is_memory_available ):
                 raise MemoryQuotaException(totalMem,currentMem)
            elif(resType == "2" and ((is_gpu_available and not is_cpu_available and is_memory_available))):
                raise CpuQuotaException(totalCpu,currentCpu)
            elif(resType == "2" and (not is_gpu_available and  is_cpu_available and is_memory_available)):
                raise GpuQuotaException(totalGpu,currentGpu)
            else:
                raise QuotaExceedException()

    @staticmethod
    def updateResourceUsage(userId,projectId,resourceQuotaReq,flag):
        projectDet=APIDBUtils.findOneById("project",projectId)
        if projectDet is None:
            error_detail=ErrorCode.PROJECT_NOT_FOUND
            raise NotFoundException(error_detail.value.code,error_detail.value.message)
        tenantId=projectDet['tenantId']
        if tenantId is None or tenantId=="":
            error_detail=ErrorCode.TENANT_ID_NOT_EMPTY_ERROR
            raise NotFoundException(error_detail.value.code,error_detail.value.message)

        tenantDetails=APIDBUtils.findOneById("tenant",tenantId)
        if tenantDetails is None:
            error_detail=ErrorCode.TENANT_DET_NOT_FOUND_ERROR
            raise NotFoundException(error_detail.value.code,error_detail.value.message)

        currentResourceUsage=tenantDetails['currentResourceUsage']
        print(currentResourceUsage)
        quotaConfig=tenantDetails['quotaConfig']
        newCurrentResUsage=updateCurrentResourceUsage(currentResourceUsage,resourceQuotaReq,quotaConfig,flag)
        print(newCurrentResUsage)
        if newCurrentResUsage == "Invalid Compute":
            return "Invalid ComputeType"
        elif newCurrentResUsage == "VolumeQuotaExceed":
            raise QuotaExceedException()
        elif newCurrentResUsage == "GPUQuotaExceed":
            raise QuotaExceedException()
        elif newCurrentResUsage == "CPUQuotaExceed":
            raise QuotaExceedException()
        elif newCurrentResUsage == "MemoryQuotaExceed":
            raise QuotaExceedException()
        else:
            filter={"id": tenantId,"isDeleted": pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            newValues={'$set': {'currentResourceUsage': newCurrentResUsage,'modifiedOn': last_modified_at, 'updatedBy': userId}}
            tenant_update_obj = APIDBUtils.updateEntity("tenant",filter,newValues)
            return "Success"