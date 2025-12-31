# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#


from typing import List
import datetime
import random
from dotenv import dotenv_values
from bson.objectid import ObjectId
from mms.constants.local_constants import *
from mms.exception.exception import *
from mms.config.logger import CustomLogger
from mms.service.common_service import ModelsBaseService, CommonService
from aicloudlibs.schemas.model_mappers import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.validations.global_validations import GlobalValidations
from aicloudlibs.constants.util_constants import *

class ModelService(ModelsBaseService):

    def __init__(self, app, customlog, userId=None):
        self.commonService = CommonService(app, customlog, userId)
        self.modelColl = app.database['model']
        self.modellColl = app.database['model']
        self.endpointColl = app.database['endpoint']
        self.tenantColl = app.database['tenant']
        self.projectColl = app.database['project']
        self.deployColl = app.database['deployment']
        self.config = dotenv_values(".env")
        ModelsBaseService.__init__(self, app, customlog, userId)

    #This method will return the list of models associated with the projectID.
    def getAllModels(self, projectId):
        print("inside getAllModels")
        
        modelColl = self.app.database["model"]
        isProjectPresent = self.commonService.checkIfProjectExists(projectId)
        if isProjectPresent == False:
            raise NotFoundException('1002',errorCodeMsgDict['1002'])            
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, projectId, VIEW)
        if hasUserAccess == True :
            modelList = list(modelColl.find({'projectId': projectId, 'isDeleted': False},{"_id" : 0}))
            modelList_sorted=sorted(modelList, key=lambda i: (i['createdOn']), reverse=True) 
        else :
            raise ForbiddenException()
        return modelList_sorted    

    #This method is used to get the model details with given modelId and versionId
    def getModelWithAccess(self, modelId:str, versionId:int) :
        self.customlog.debug('START getModelWithAccess')
        modelExists = False
        modelObj = self.modelColl.find_one({"id": modelId, "isDeleted": False,"version":versionId}, {"_id":0})
        if modelObj :
            owner = modelObj['createdBy']
            if owner is not None and owner == self.loggedUser :
                modelExists = True
            else :
                projectId = modelObj['projectId']
                hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, projectId, VIEW)
                if hasUserAccess == True :
                    modelExists = True
                else :
                    raise ForbiddenException()
            if modelExists==True :
                if modelObj['status'] == MODEL_STATUS_DEPLOYED :
                    deployObj = self.deployColl.find_one({"modelId": modelId,"version": versionId,"status": DeploymentStatusEnum.Deployed},{"_id": 0})
                    modelObj["endpointId"] = deployObj["endpointId"]
                self.customlog.debug("END getModelWithAccess")
                return modelObj
        else :
            raise NotFoundException('1010',errorCodeMsgDict['1010'])
        
    #This method is used to get the model details with given model name  and version and projectId
    def _getModelWithProjectNameVersion(self, body: ModelDetails) :
        self.customlog.debug('START getModelWithProjectNameVersion')
        modelObj = self.modelColl.find_one({'name':body.name, 'version':body.version,
                            'projectId':body.projectId, 'isDeleted': False})
        self.customlog.debug('END getModelWithProjectNameVersion')
        return modelObj
    
    #This method is used to get the model details with given model name and projectId
    def _getModelWithProjectName(self, body: ModelDetails) :
        self.customlog.debug('START getModelWithProjectName')
        modelObj = self.modelColl.find_one({'name':body.name,'projectId':body.projectId, 'isDeleted': False})
        self.customlog.debug('END getModelWithProjectName')
        return modelObj
    
    #This method is used to get the model details with given model name and version
    def getModelWithNameVersion(self, modelName:str, version:str) :
        self.customlog.debug('START getModelWithNameVersion')
        modelObj = self.modelColl.find_one({'name': modelName, 'version': version, 'isDeleted': False})
        self.customlog.debug('END getModelWithNameVersion')
        return modelObj
    
    #This method is used to get the model details with given model Id and version
    def getModelWithIdVersion(self, modelId:str, version:str) :
        self.customlog.debug('START getModelWithIdVersion')
        modelObj = self.modelColl.find_one({'id': modelId, 'version': version, 'isDeleted': False})
        self.customlog.debug('END getModelWithIdVersion')
        return modelObj
    
    #This method is used to get the model details with given model Id
    def getModelWithId(self, modelId:str) :
        self.customlog.debug('START getModelWithId')
        modelObj = self.modelColl.find_one({'id': modelId, 'isDeleted': False})
        self.customlog.debug('END getModelWithId')
        return modelObj
    
    #This method is used to register the model with given model details
    def registerModel (self, body: ModelDetails) :
        self.customlog.debug('START getModelDetails')

        isValidProject = self.commonService.checkIfProjectExists(body.projectId)
        if not isValidProject:
            raise ModelAPINotFoundError('1002')
        
        hasDeployAccess: bool = self.commonService.checkUserAccessForProject(body.projectId, USER_PERMISSION_DEPLOYMODEL)
        if hasDeployAccess==False :
            raise ModelUserAccessError('1087')
        
        if self._getModelWithProjectNameVersion(body) is not None:
            raise ModelAPIBusinessError('1065')
        
        modelwithsamename = self._getModelWithProjectName(body)
        if modelwithsamename is not None:
            randomModelId = modelwithsamename['id']
        else :
            randomModelId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        
        ports=body.container.ports
        hasValid = False
        print(len(ports))
        if len(ports) != 0 :
            for port in ports:
                res=True
                print(port.name)
                temp_name = port.name.lower()
                print(temp_name)
                if port.name in ['http', 'containerport', 'http-triton']:
                    hasValid = True
                if temp_name == port.name:
                    res=False    
                port=port.dict()
                if port['value'].isdigit()==False:
                    raise ModelAPIBusinessError('3605')    
               
        if len(ports) == 0:
            raise ModelAPIBusinessError('3612')
        
        if not hasValid and len(ports) != 0 and not res:
            raise ModelAPIBusinessError('3613')   

        if res:
            raise ModelAPIBusinessError('3626') 
        
        if body.createdOn is None or body.createdOn=='':
            body.createdOn = datetime.utcnow()
        if body.createdBy is None or body.createdBy=='':
            body.createdBy = self.loggedUser

                    
        modelDict = body.dict()
        modelDict['id'] = randomModelId
        modelDict['status']= ModelStatusEnum.Registered
        modelId = self.modelColl.insert_one(modelDict).inserted_id
        model_data = ModelResponseData.parse_obj(modelDict)
        self.customlog.debug('END registerModel')
        return model_data

    #This method is used to update the model status with given modelId and versionId
    def updateModelStatus(self,versionId:int,modelId: str, status: str):
        self.customlog.debug('START updateModelStatus')
        
        filter = {"id": modelId, "isDeleted": False,"version":versionId}
        newValues = {'$set': {'status': status, 'isDeleted': True,'updatedBy': self.loggedUser, 
                              'modifiedOn': datetime.utcnow()}}
        result = self.modelColl.update_one(filter, newValues)

        self.customlog.debug('END updateModelStatus==%s', result.modified_count)


    #This method is used to update the model metadata for given modelId and version
    def updateModelMetadata(self, modelId: str, version:str, body:ModelMetaData) :
        self.customlog.debug('START updateModelMetadata')
        
        modelId = modelId
        modelVersion = version
        modelObj = self.modelColl.find_one({'id':modelId, 'version':modelVersion, 'isDeleted':False})
        
        if modelObj is None:
            raise NotFoundException('3620',errorCodeMsgDict['3620'])
        
        hasDeployAccess: bool = self.commonService.checkUserAccessForProject(modelObj['projectId'], USER_PERMISSION_DEPLOYMODEL)
        if hasDeployAccess==False :
            raise ForbiddenException()
        
        metadataDict = body.dict()
        if modelObj['metadata'] is None :
            print("Metadata is None")
            if metadataDict['modelDetails']['tasktype'] is not None and metadataDict['modelDetails']['tasktype'] != '':
                taskTypeVal = metadataDict['modelDetails']['tasktype']
                if taskTypeVal not in taskTypeJson['tasktype']:
                    print("Enter any other Value")
                    raise NotFoundException('3625',errorCodeMsgDict['3625'])
                else:    
                    print("Value Exists")
                    modelObj['metadata'] = metadataDict

        else:
            if metadataDict['modelDetails'] is not None:
                print("Metadata is Not None")
                if metadataDict['modelDetails']['displayName'] is not None and metadataDict['modelDetails']['displayName'] != '':
                    modelObj['metadata']['modelDetails']['displayName'] = metadataDict['modelDetails']['displayName']
                if metadataDict['modelDetails']['overview'] is not None and metadataDict['modelDetails']['overview'] != '':
                    modelObj['metadata']['modelDetails']['overview'] = metadataDict['modelDetails']['overview']
                if metadataDict['modelDetails']['tasktype'] is not None and metadataDict['modelDetails']['tasktype'] != '':
                    taskTypeVal = metadataDict['modelDetails']['tasktype']
                    if taskTypeVal not in taskTypeJson['tasktype']:
                        raise NotFoundException('3625',errorCodeMsgDict['3625'])
                    else:    
                        modelObj['metadata']['modelDetails']['tasktype'] = metadataDict['modelDetails']['tasktype']
                if metadataDict['modelDetails']['customTags'] is not None and metadataDict['modelDetails']['customTags'] != '':
                    customTags = metadataDict['modelDetails']['customTags']
                    for customTag in customTags:
                        if customTag['tags'] is not None and customTag['tags'] != '':
                            modelObj['metadata']['modelDetails']['customTags'][0]['tags'] = customTag['tags'] 
                if metadataDict['modelDetails']['documentation'] is not None and metadataDict['modelDetails']['documentation'] != '':
                    modelObj['metadata']['modelDetails']['documentation'] = metadataDict['modelDetails']['documentation']
                if metadataDict['modelDetails']['owners'] is not None and metadataDict['modelDetails']['owners'] != '':
                    owners = metadataDict['modelDetails']['owners']
                    for owner in owners:
                        if owner['name'] is not None and owner['name'] != '':
                            modelObj['metadata']['modelDetails']['owners'][0]['name'] = owner['name']
                        if owner['contact'] is not None and owner['contact'] != '':
                            modelObj['metadata']['modelDetails']['owners'][0]['contact'] = owner['contact']
                if metadataDict['modelDetails']['versionHistory'] is not None and metadataDict['modelDetails']['versionHistory'] != '':
                    versions = metadataDict['modelDetails']['versionHistory']
                    for version in versions:
                        if version['name'] is not None and version['name'] != '':
                            modelObj['metadata']['modelDetails']['versionHistory'][0]['name'] = version['name']
                        if version['date'] is not None and version['date'] != '':
                            modelObj['metadata']['modelDetails']['versionHistory'][0]['date'] = version['date']
                        if version['diff'] is not None and version['diff'] != '':
                            modelObj['metadata']['modelDetails']['versionHistory'][0]['diff'] = version['diff']
                if metadataDict['modelDetails']['licenses'] is not None and metadataDict['modelDetails']['licenses'] != '':
                    licenses = metadataDict['modelDetails']['licenses']
                    for license in licenses:
                        if license['identifier'] is not None and license['identifier'] != '':
                            modelObj['metadata']['modelDetails']['licenses'][0]['identifier'] = license['identifier']
                        if license['customText'] is not None and license['customText'] != '':
                            modelObj['metadata']['modelDetails']['licenses'][0]['customText'] = license['customText']
                if metadataDict['modelDetails']['references'] is not None and metadataDict['modelDetails']['references'] != '':
                    references = metadataDict['modelDetails']['references']
                    for reference in references:
                        if reference['reference'] is not None and reference['reference'] != '':
                            modelObj['metadata']['modelDetails']['references'][0]['reference'] = reference['reference']
                if metadataDict['modelDetails']['citations'] is not None and metadataDict['modelDetails']['citations'] != '':
                    citations = metadataDict['modelDetails']['citations']
                    for citation in citations:
                        if citation['style'] is not None and citation['style'] !='':
                            modelObj['metadata']['modelDetails']['citations'][0]['style'] = citation['style']
                        if citation['citation'] is not None and citation['citation'] !='':
                            modelObj['metadata']['modelDetails']['citations'][0]['citation'] = citation['citation']
                if metadataDict['modelDetails']['path'] is not None and metadataDict['modelDetails']['path'] != '':
                    modelObj['metadata']['modelDetails']['path'] = metadataDict['modelDetails']['path']

            if metadataDict['modelParameters'] is not None:
                if metadataDict['modelParameters']['modelArchitecture'] is not None and metadataDict['modelParameters']['modelArchitecture'] != '':
                    modelObj['metadata']['modelParameters']['modelArchitecture'] = metadataDict['modelParameters']['modelArchitecture']
                if metadataDict['modelParameters']['data'] is not None and metadataDict['modelParameters']['data'] != '':
                    datas = metadataDict['modelParameters']['data']
                    for data in datas:
                        if data['name'] is not None and data['name'] !='':
                            modelObj['metadata']['modelParameters']['data'][0]['name'] = data['name']
                        if data['link'] is not None and data['link'] !='':
                            modelObj['metadata']['modelParameters']['data'][0]['link'] = data['link']
                        if data['sensitive'][0]['Fields'] is not None and data['sensitive'][0]['Fields'] !='':
                            if data['sensitive'][0]['Fields'][0] is not None and data['sensitive'][0]['Fields'][0] !='':
                                modelObj['metadata']['modelParameters']['data'][0]['sensitive'][0]['Fields'] = data['sensitive'][0]['Fields']

                        if data['classification'] is not None and data['classification'] != '':
                            modelObj['metadata']['modelParameters']['data'][0]['classification'] = data['classification']
                if metadataDict['modelParameters']['inputFormat'] is not None and metadataDict['modelParameters']['inputFormat'] != '':
                    modelObj['metadata']['modelParameters']['inputFormat'] = metadataDict['modelParameters']['inputFormat']
                if metadataDict['modelParameters']['inputFormatMap'] is not None and metadataDict['modelParameters']['inputFormatMap'] != '':
                    modelObj['metadata']['modelParameters']['inputFormatMap'] = metadataDict['modelParameters']['inputFormatMap']
                if metadataDict['modelParameters']['outputFormat'] is not None and metadataDict['modelParameters']['outputFormat'] != '':
                    modelObj['metadata']['modelParameters']['outputFormat'] = metadataDict['modelParameters']['outputFormat']
                if metadataDict['modelParameters']['outputFormatMap'] is not None and metadataDict['modelParameters']['outputFormatMap'] != '':
                    modelObj['metadata']['modelParameters']['outputFormatMap'] = metadataDict['modelParameters']['outputFormatMap']

            if metadataDict['quantitativeAnalysis'] is not None:
                if metadataDict['quantitativeAnalysis']['performanceMetrics'] is not None and metadataDict['quantitativeAnalysis']['performanceMetrics'] != '':
                    performanceMetrics = metadataDict['quantitativeAnalysis']['performanceMetrics']
                    for performanceMetric in performanceMetrics:
                        if performanceMetric['type'] is not None and performanceMetric['type'] != '':
                            modelObj['metadata']['quantitativeAnalysis']['performanceMetrics'][0]['type'] = performanceMetric['type']
                        if performanceMetric['value'] is not None and performanceMetric['value'] != '':
                            modelObj['metadata']['quantitativeAnalysis']['performanceMetrics'][0]['value'] = performanceMetric['value']
                        if performanceMetric['slice'] is not None and performanceMetric['slice'] != '':    
                            modelObj['metadata']['quantitativeAnalysis']['performanceMetrics'][0]['slice'] = performanceMetric['slice']
                        if performanceMetric['confidenceInterval'] is not None and performanceMetric['confidenceInterval'] != '':
                            if performanceMetric['confidenceInterval']['lowerBound'] is not None and performanceMetric['confidenceInterval']['lowerBound'] != '':
                                modelObj['metadata']['quantitativeAnalysis']['performanceMetrics'][0]['confidenceInterval']['lowerBound'] = performanceMetric['confidenceInterval']['lowerBound']
                            if performanceMetric['confidenceInterval']['upperBound'] is not None and performanceMetric['confidenceInterval']['upperBound'] != '':
                                modelObj['metadata']['quantitativeAnalysis']['performanceMetrics'][0]['confidenceInterval']['upperBound'] = performanceMetric['confidenceInterval']['upperBound']

            if metadataDict['considerations'] is not None:
                if metadataDict['considerations']['users'] is not None and metadataDict['considerations']['users'] != '':
                    modelObj['metadata']['considerations']['users'] = metadataDict['considerations']['users']
                if metadataDict['considerations']['useCases'] is not None and metadataDict['considerations']['useCases'] != '':
                    modelObj['metadata']['considerations']['useCases'] = metadataDict['considerations']['useCases']
                if metadataDict['considerations']['limitations'] is not None and metadataDict['considerations']['limitations'] != '':
                    modelObj['metadata']['considerations']['limitations'] = metadataDict['considerations']['limitations']
                if metadataDict['considerations']['tradeoffs'] is not None and metadataDict['considerations']['tradeoffs'] != '':
                    modelObj['metadata']['considerations']['tradeoffs'] = metadataDict['considerations']['tradeoffs']
                if metadataDict['considerations']['ethicalConsiderations'] is not None and metadataDict['considerations']['ethicalConsiderations'] != '':
                    if metadataDict['considerations']['ethicalConsiderations'][0]['name'] is not None and metadataDict['considerations']['ethicalConsiderations'][0]['name'] != '':    
                        modelObj['metadata']['considerations']['ethicalConsiderations'][0]['name'] = metadataDict['considerations']['ethicalConsiderations'][0]['name']
                    if metadataDict['considerations']['ethicalConsiderations'][0]['mitigationStrategy'] is not None and metadataDict['considerations']['ethicalConsiderations'][0]['mitigationStrategy'] != '':
                        modelObj['metadata']['considerations']['ethicalConsiderations'][0]['mitigationStrategy'] = metadataDict['considerations']['ethicalConsiderations'][0]['mitigationStrategy']
                if metadataDict['considerations']['environmentalConsiderations'] is not None and metadataDict['considerations']['environmentalConsiderations'] != '':
                    if metadataDict['considerations']['environmentalConsiderations'][0]['hardwareType'] is not None and metadataDict['considerations']['environmentalConsiderations'][0]['hardwareType'] != '':
                        modelObj['metadata']['considerations']['environmentalConsiderations'][0]['hardwareType'] = metadataDict['considerations']['environmentalConsiderations'][0]['hardwareType']
                    if metadataDict['considerations']['environmentalConsiderations'][0]['hoursUsed'] is not None and metadataDict['considerations']['environmentalConsiderations'][0]['hoursUsed'] != '':    
                        modelObj['metadata']['considerations']['environmentalConsiderations'][0]['hoursUsed'] = metadataDict['considerations']['environmentalConsiderations'][0]['hoursUsed']
                    if metadataDict['considerations']['environmentalConsiderations'][0]['cloudProvider'] is not None and metadataDict['considerations']['environmentalConsiderations'][0]['cloudProvider'] != '':    
                        modelObj['metadata']['considerations']['environmentalConsiderations'][0]['cloudProvider'] = metadataDict['considerations']['environmentalConsiderations'][0]['cloudProvider']
                    if metadataDict['considerations']['environmentalConsiderations'][0]['computeRegion'] is not None and metadataDict['considerations']['environmentalConsiderations'][0]['computeRegion'] != '':    
                        modelObj['metadata']['considerations']['environmentalConsiderations'][0]['computeRegion'] = metadataDict['considerations']['environmentalConsiderations'][0]['computeRegion']
                    if metadataDict['considerations']['environmentalConsiderations'][0]['carbonEmitted'] is not None and metadataDict['considerations']['environmentalConsiderations'][0]['carbonEmitted'] != '':
                        modelObj['metadata']['considerations']['environmentalConsiderations'][0]['carbonEmitted'] = metadataDict['considerations']['environmentalConsiderations'][0]['carbonEmitted']


        filter = {'id':modelId, 'version': modelVersion, 'isDeleted':False}
        metaObjUpd = self.modelColl.update_one(filter,{"$set":{'metadata': modelObj['metadata']}})
        metaUpdate = self.modelColl.find_one({'id':modelId,'version':modelVersion,'isDeleted':False},{"_id":0})
        
        print("**Return Value**",metaObjUpd)
        self.customlog.debug('END updateModelMetadata')
        return metaUpdate
    
    #This method is used to get the model metadata task type
    def getModelMetadataTaskType(self, userId:str) :
        self.customlog.debug('START getModelMetadataTaskType')
        modelTaskTypeObj = taskTypeJsonVal
        self.customlog.debug('END getModelMetadataTaskType')
        return modelTaskTypeObj
    def deleteModel(self,projectId:str, modelId:str, versionId:int):
        isProjectPresent = self.commonService.checkIfProjectExists(projectId)
            
        if isProjectPresent == False:
            raise NotFoundException('1002',errorCodeMsgDict['1002'])
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser,projectId, DEPLOY_MODEL)
        if hasUserAccess == False:
            raise ForbiddenException()  
        modelObj = self.modellColl.find_one({"id": modelId,"projectId":projectId,"version":versionId,"isDeleted": False}, {"_id":0})
        if modelObj is None:
            raise NotFoundException('1010',errorCodeMsgDict['1010'])  
        
        if modelObj['status']==ModelStatusEnum.Registered:
            
            self.updateModelStatus(versionId,modelId,ModelStatusEnum.Deleted)
            return None

        if modelObj["status"]==ModelStatusEnum.Deployed:
            deployObj = self.deployColl.find_one({"modelId": modelId, "isDeleted": False,"version":versionId,"status":DeploymentStatusEnum.Deployed}, {"_id":0})  
            if deployObj is None:
                raise ModelAPIBusinessError('3627') 
            deploymentId = deployObj["id"]
            return deploymentId
            

