# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from aicloudlibs.constants.error_constants import ErrorCode

def checkForQuota(totalValue,currentValue, requestedValue):
        availableQuota=totalValue-currentValue
        if requestedValue <= availableQuota:
           return True
        else:
            return False
        
def getGPUQuotaDetails(reqMemory,computes,reqType):
       minQty=0
       maxQty=0
       for compute in computes:
         if compute['memory']== reqMemory and compute['type'].lower()==reqType.lower() :
           minQty=minQty+compute['minQty']
           maxQty=maxQty+compute['maxQty']
       return minQty,maxQty
       
def getCPUQuotaDetails(computes):
       minQty=0
       maxQty=0
       memoryVal=0
       for compute in computes:
         if compute['type'].lower() == 'cpu':
           minQty=minQty+compute['minQty']
           maxQty=maxQty+compute['maxQty']
           memory=compute['memory']
           memory=memory.lower().replace("gb","")
           memoryVal=memoryVal+int(memory)
       return minQty,maxQty,memoryVal
       
def convertGBtoGIB(memory):
      if isinstance(memory,str):
          memory=memory.lower().replace("gb","")
          memory=int(memory)
      gibVal=memory*0.93
      return gibVal

def updateCurrentResourceUsage(currentResourceUsage,resourceQuotaReq,quotaConfig,flag):
    newCurrentResUsage=""
    updateDict=currentResourceUsage
    reqValue=resourceQuotaReq['volumeSizeinGB']
    oldValue=currentResourceUsage['volumeSizeinGB']
    maxValue=quotaConfig['volumeSizeinGB']
    if flag=="allocate":
      newValue=oldValue+reqValue
      if newValue > maxValue :
          newCurrentResUsage="VolumeQuotaExceed"
    else:
      newValue=oldValue-reqValue
      if newValue < 0:
          newValue=0
    if newCurrentResUsage != "VolumeQuotaExceed" :
        updateDict['volumeSizeinGB']=newValue
        computes=resourceQuotaReq['computes']
        currComputes=updateDict['computes']
        for compute in computes:
              if compute['type'].lower() == "gpu":
                reqMinQty= int(compute['minQty'])
                reqMaxQty= int(compute['maxQty'])
                reqGPUMemory=compute['memory']
                for currentCompute in currComputes:
                    if currentCompute['type'].lower()== "gpu" and currentCompute['memory'].lower()==reqGPUMemory.lower():
                        oldMinValue=currentCompute['minQty']
                        oldMaxValue=currentCompute['maxQty']
                        totalMinVal,totalMaxValue=getGPUQuotaDetails(reqGPUMemory,quotaConfig['computes'],"gpu")
                        if flag=="allocate":
                          newMinValue=oldMinValue+reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue+reqMaxQty
                          if newMaxValue > totalMaxValue:
                              newCurrentResUsage = "GPUQuotaExceed"
                        else:
                          newMinValue=oldMinValue-reqMinQty
                          if newMinValue < 0:
                              newMinValue=0 
                          newMaxValue=oldMaxValue-reqMaxQty
                          if newMaxValue < 0:
                              newMaxValue=0
                        if newCurrentResUsage == "":
                            currentCompute['minQty']=newMinValue
                            currentCompute['maxQty']=newMaxValue

              elif compute['type'].lower() == "cpu":
                reqMinQty= int(compute['minQty'])
                reqMaxQty= int(compute['maxQty'])
                reqCPUMemory=compute['memory']
                reqCPUMemVal=reqCPUMemory.lower().replace("gb","")
                totalMinVal,totalMaxVal,totalMemory=getCPUQuotaDetails(quotaConfig['computes'])

                for currentCompute in currComputes:
                    if currentCompute['type'].lower()== "cpu":
                      oldMinValue=currentCompute['minQty']
                      oldMaxValue=currentCompute['maxQty']
                      oldMem=currentCompute['memory']
                      oldMemValue=oldMem.lower().replace("gb","")
                      if flag=="allocate":
                          newMinValue=oldMinValue+reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue+reqMaxQty
                          if newMaxValue>totalMaxVal:
                              newCurrentResUsage = "CPUQuotaExceed"
                          if newCurrentResUsage !="CPUQuotaExceed":
                              newMemValue=int(oldMemValue)+int(reqCPUMemVal)
                              if newMemValue > totalMemory:
                                  newCurrentResUsage = "MemoryQuotaExceed"
                      else:
                          newMinValue=oldMinValue-reqMinQty
                          if newMinValue < 0:
                              newMinValue=0
                          newMaxValue=oldMaxValue-reqMaxQty
                          if newMaxValue < 0:
                              newMaxValue=0
                              
                          if newCurrentResUsage !="CPUQuotaExceed":
                              newMemValue=int(oldMemValue)-int(reqCPUMemVal)
                              if newMemValue < 0:
                                  newMemValue=0

                      if newCurrentResUsage =="":    
                          currentCompute['minQty']=newMinValue
                          currentCompute['maxQty']=newMaxValue
                          currentCompute['memory']=str(newMemValue)+"GB"
              else:
                    newCurrentResUsage="Invalid Compute" 
    if newCurrentResUsage == "" :
        newCurrentResUsage=updateDict
        print(currentResourceUsage)
    print(newCurrentResUsage)
    
    return newCurrentResUsage