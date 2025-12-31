# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#


from typing import List
import datetime
from bson.objectid import ObjectId
from mms.constants.local_constants import *
from mms.exception.exception import ModelAPINotFoundError
from aicloudlibs.exceptions.global_exception import *

class ModelsBaseService:

    def __init__(self, app, customlog, userId=None):
        self.log = app.logger
        self.app = app
        self.customlog = customlog
        self.loggedUser = userId


class CommonService(ModelsBaseService):
    
    #This method will return the project details for the given project id
    def getProjectDetails(self, projectId: str) :
        self.customlog.debug('START getProjectDetails')
        projectColl = self.app.database['project']
        if projectId is not None:
            try:
                projectObj = projectColl.find_one({"id": projectId, "isDeleted": False})
            except:
                raise NotFoundException('1002',errorCodeMsgDict['1002'])
        self.customlog.debug('END getProjectDetails')
        return projectObj
    
    #This method will check for the given project id exist or not
    def checkIfProjectExists(self, projectId:str) -> bool:
        self.customlog.debug('START checkIfProjectExists')
        isProjectPresent = False
        projectObj = self.getProjectDetails(projectId)
        if projectObj is not None:
            isProjectPresent = True
        self.customlog.debug('END checkIfProjectExists==%s', isProjectPresent)
        return isProjectPresent

    #This method is used to update the resources allocated to the project.
    def updateResourcesForProject(self, deploymentId):
        self.customlog.debug('START updateResourcesForProject')

        projectColl = self.app.database['project']
        deploymentColl = self.app.database['deployment']
        
        deployObj = deploymentColl.find_one({"_id": ObjectId(deploymentId)})
        if deployObj:
            gpuQty = deployObj['body']['inferenceConfig']['inferenceSpec']['containerResourceConfig']['gpuQty']
            gpuQty = int(gpuQty) if gpuQty is not None else 0
            cpuQty = deployObj.get('body').get('inferenceConfig').get('inferenceSpec').get('containerResourceConfig').get('cpuQty')
            cpuQtyInt = float(str(cpuQty).strip().replace('m','')) if cpuQty is not None else 0
            cpuMem = deployObj.get('body').get('inferenceConfig').get('inferenceSpec').get('containerResourceConfig').get('cpuMemory')
            cpuMemInt = int(str(cpuMem).strip().replace('Gi','')) if cpuMem is not None else 0
            
            projectId = deployObj.get('body').get('projectId')
            if projectId:
                projectObj = projectColl.find_one({"_id": ObjectId(projectId)})
                
                gpuAllCnt: int = int(projectObj.get('body').get('gpuAllocatedCount', 0))
                gpuAllCnt = gpuAllCnt + gpuQty
            
                cpuAllCnt: float = float(projectObj.get('body').get('cpuAllocatedCount', 0))
                cpuAllCnt = cpuAllCnt + cpuQtyInt

                cpuMemAllCnt: int = int(projectObj.get('body').get('cpuMemAllocatedCount', 0))
                cpuMemAllCnt = cpuMemAllCnt + cpuMemInt
            
                filter = {'_id': ObjectId(projectId), 'body.isDeleted': False}
                setVal = {'body.updatedBy': self.loggedUser}
                if gpuAllCnt > 0 :
                    setVal['body.gpuAllocatedCount'] = gpuAllCnt
                if cpuAllCnt > 0 :
                    setVal['body.cpuAllocatedCount'] = cpuAllCnt
                if cpuMemAllCnt > 0 :
                    setVal['body.cpuMemAllocatedCount'] = cpuMemAllCnt

                setVal['body.modifiedOn'] = datetime.datetime.utcnow()
                result = projectColl.update_one(filter, {'$set': setVal})

        self.customlog.debug('END updateResourcesForProject==%s', result.modified_count)

    #This method is used get resources allocated to the user.
    def getUserResourceCount(self, userId) -> dict:
        self.customlog.debug('START getUserResourceCount')
        projectColl = self.app.database['project']
        projectList = projectColl.find({'body.createdBy': userId})
        if projectList : 
            gpuAllCount = 0
            cpuAllCount = 0
            cpuMemAllCount = 0
            for project in projectList :
                gpuAllCount = gpuAllCount + int(project.get('body').get('gpuAllocatedCount', 0))
                cpuAllCount = cpuAllCount + int(project.get('body').get('cpuAllocatedCount', 0))
                cpuMemAllCount = cpuMemAllCount + int(project.get('body').get('cpuMemAllocatedCount', 0))
        else:
            raise ModelAPINotFoundError('1002')
        
        userRes = {}
        if gpuAllCount > 0:
            userRes['gpuAlloc']: gpuAllCount
        if cpuAllCount > 0:
            userRes['cpuAlloc']: cpuAllCount
        if cpuMemAllCount > 0:
            userRes['cpuMemAlloc']: cpuMemAllCount

        self.customlog.debug('END getUserResourceCount')
        return userRes

    #This method is used get resources allocated to the project.
    def getProjectResourceCount(self, projectId) -> dict:
        self.customlog.debug('START getProjectResourceCount')
        projectColl = self.app.database['project']
        projectObj = projectColl.find_one({'_id': ObjectId(projectId)})
        if projectObj: 
            gpuAllCount = int(projectObj.get('body').get('gpuAllocatedCount', 0))
            cpuAllCount = int(projectObj.get('body').get('cpuAllocatedCount', 0))
            cpuMemAllCount = int(projectObj.get('body').get('cpuMemAllocatedCount', 0))
        else:
            raise ModelAPINotFoundError('1002')
        
        projRes = {}
        if gpuAllCount > 0:
            projRes['gpuAlloc']: gpuAllCount
        if cpuAllCount > 0:
            projRes['cpuAlloc']: cpuAllCount
        if cpuMemAllCount > 0:
            projRes['cpuMemAlloc']: cpuMemAllCount
        self.customlog.debug('END getProjectResourceCount')
        return projRes
    
    #This method is used to check the user access for the project.
    def checkUserAccessForProject(self, projectId:str, userPermission:str) -> bool:
        self.customlog.debug('START checkUserAccessForProject')
        hasAccess = False
        userId = self.loggedUser
        projectObj = self.getProjectDetails(projectId)
        if projectObj:
            if projectObj['createdBy'] == userId :
                hasAccess = True
            else:
                userAccessList = projectObj['userLists']
                if userAccessList :
                    for userA in userAccessList :
                        if userId == userA['userEmail'] :
                            userPerm = userA['permissions']
                            if userPerm and (userPerm[userPermission] or userPerm['workspaceAdmin']) :
                                hasAccess = True
                            else :
                                hasAccess = False

        self.customlog.debug('END checkUserAccessForProject==%s', hasAccess)
        return hasAccess

