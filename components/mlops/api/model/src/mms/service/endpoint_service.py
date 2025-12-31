# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import random
from dotenv import dotenv_values
from typing import List
from bson import ObjectId
import datetime
import requests 
import re
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.schemas.model_mappers import *
from aicloudlibs.constants.http_status_codes import *
from aicloudlibs.validations.global_validations import GlobalValidations
from mms.service.common_service import CommonService, ModelsBaseService
from mms.service.model_service import *
from mms.exception.exception import *
from mms.utils.CommonUtils import *
from mms.constants.local_constants  import *



class EndpointService(ModelsBaseService):

    def __init__(self, app, customlog, userId):
        self.commonService = CommonService(app, customlog, userId)
        #self.resourceUtil = ResourceUtility()
        self.modelService = ModelService(app, customlog, userId)
        self.endpointColl = app.database['endpoint']
        self.deployColl = app.database['deployment']
        self.idpLogColl = app.database['idp_job_details']
        self.projectColl = app.database['project']
        self.tenantColl = app.database['tenant']
        self.modellColl = app.database['model']
        self.config = dotenv_values(".env")
        ModelsBaseService.__init__(self, app, customlog, userId)

    #To create endpoint within the project.
    def createEndpoint(self, endpoint:Endpoint) -> EndpointResponseData:
        self.customlog.debug('START createEndpoint')
        
        if checkIfNull(endpoint) :
            raise NotFoundException(2300, 'Endpoint Request Payload not found')
        
        isValidProject = self.commonService.checkIfProjectExists(endpoint.projectId)
        if not isValidProject:
            raise ModelAPINotFoundError('1002')
        
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, endpoint.projectId, DEPLOY_MODEL)
        if hasUserAccess == False:
            raise ForbiddenException()
        
        if self._checkEndpointName(endpoint.name) :
            raise ModelAPIException(HTTP_STATUS_BAD_REQUEST, 2301, 'Endpoint Name already exists')
        
        pat = re.compile(r'^/.+')
        if not re.fullmatch(pat, endpoint.contextUri):
            raise ModelAPIBusinessError('3607')
        
        if not checkIfNotEmpty(endpoint.createdOn) :
            endpoint.createdOn = datetime.utcnow()
        if endpoint.createdBy is None or endpoint.createdBy=='' :
            endpoint.createdBy = self.loggedUser

        endpointDict = endpoint.dict()
        endpointDict['id'] = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        endpointDict['status'] = EndpointStatuseEnum.Created 
        endpointId:ObjectId = self.endpointColl.insert_one(endpointDict).inserted_id
        self.customlog.debug('inserted endpoint record===%s', endpointId)

               
        endPRespD = EndpointResponseData.parse_obj(endpointDict)
        self.customlog.debug('END createEndpoint')
        return endPRespD

    #To check if endpoint name already exists
    def _checkEndpointName(self, endpointName) :
        self.customlog.debug('START _checkEndpointName')
        endpoingObj = self.endpointColl.find_one({'name': endpointName, 'isDeleted': False})
        if checkIfNotNull(endpoingObj) :
            return True
        self.customlog.debug('END _checkEndpointName')
        return False
    
    #To check if endpoint available for deployment
    def _checkEndpointForDeployment(self, endpointId, modelId='') :
        self.customlog.debug('START _checkEndpointForDeployment')
        
        filter = {'id': endpointId, 'isDeleted': False}
        deployObj = self.endpointColl.find_one(filter)
        self.customlog.debug('END _checkEndpointForDeployment')
        return deployObj
    
    #To check if deployment already exists for the model and endpoint
    def _checkDeploymentWithSameModelEndpoint(self, endpointId, modelId, version) :
        self.customlog.debug('START _checkDeploymentWithSameModelEndpoint')
        filter = {'endpointId': endpointId, 'modelId': modelId, 'isDeleted': False}
        if checkIfNotEmpty(version) :
            filter['version'] = version
        orFlter = [{'status': DEPLOYMENT_STATUS_INPROGRESS}, {'status': DEPLOYMENT_STATUS_SUCCESS}]
        filter['$or'] = orFlter
        deployObj = self.deployColl.find_one(filter)
        self.customlog.debug('END _checkDeploymentWithSameModelEndpoint')
        return deployObj
    
    def _updateJobIdInDeployment (self, jobId, deploymentId) :
        self.customlog.debug('START _updateJobIdInDeployment')
        filter = {'id': deploymentId, 'isDeleted': False}
        newValues = { '$set': {'jobId': jobId} }
        self.deployColl.update_one(filter, newValues)
        self.customlog.debug('END _updateJobIdInDeployment')

    #To create model deployment using provided modelId, model version and endpointId.
    def createModelDeployment (self, body: Deployment) -> DeploymentResponseData :
        self.customlog.debug('START createModelDeployment')
        randomDeployId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        
        modelId = body.modelId
        endpointId = body.endpointId
        modelObj = self.modelService.getModelWithIdVersion(modelId, body.version)
        if checkIfNull(modelObj) :
            raise ModelAPINotFoundError('3620')
        
        endpointObj = self.endpointColl.find_one({"id": endpointId, "isDeleted": False,"status":"Created"}, {"_id":0})
        if endpointObj is not None and not endpointObj['projectId'] == modelObj['projectId']:
            raise ModelAPIBusinessError('3621')

        projectId = modelObj['projectId']
        deployO = self._checkEndpointForDeployment(body.endpointId)
        if deployO is None:
            raise ModelAPIBusinessError('3600')
        
        deployO = self._checkDeploymentWithSameModelEndpoint(body.endpointId, modelId, body.version)
        if deployO is not None and deployO.get('status')==DEPLOYMENT_STATUS_SUCCESS :
            raise ModelAPIBusinessError('3601')
        if deployO is not None and deployO.get('status')==DEPLOYMENT_STATUS_INPROGRESS :
            raise ModelAPIBusinessError('3619')
        
        hasDeployAccess: bool = GlobalValidations.hasAccess(self.loggedUser, projectId, 'deployModel')
        if hasDeployAccess==False :
            raise ModelUserAccessError('1086')
        
        ComputeArr = body.inferenceConfig.inferenceSpec.containerResourceConfig.computes
        for comp in ComputeArr:
            patMemory = re.compile(r'[. 0-9]+(GB|gb)')
            if not re.fullmatch(patMemory,comp.memory) and not comp.memory.isdigit():
                 raise ModelUserAccessError('3618')
            if comp.memory.isdigit():
                comp.memory = comp.memory+"GB"

        modelSpecArr = body.inferenceConfig.inferenceSpec.modelSpec
        for modelSpec in modelSpecArr:
            pat = re.compile(r'^/.+')
            if not re.fullmatch(pat, modelSpec.modelUris.predictUri):
                raise ModelAPIBusinessError('3608')
            if not re.fullmatch(pat, modelSpec.modelUris.prefixUri):
                raise ModelAPIBusinessError('3609')
            
        if body.inferenceConfig.servingSpec is None and body.inferenceConfig.servingFramework == "Triton":
            raise ModelAPIBusinessError('3614')
        
        if body.inferenceConfig.servingFramework == "Triton"and  body.inferenceConfig.servingSpec.tritonSpec is None:
            raise ModelAPIBusinessError('3616')
        
        if body.inferenceConfig.servingFramework == "Triton" and body.inferenceConfig.servingSpec.tritonSpec.logLevel == "":
            raise ModelAPIBusinessError('3615')
        
        if body.inferenceConfig.servingFramework == "Triton" and body.inferenceConfig.servingSpec.tritonSpec.logLevel != "" and not body.inferenceConfig.servingSpec.tritonSpec.logLevel.upper() in ['INFO','WARNING','ERROR']:
            raise ModelAPIBusinessError('3617')

        resConfig = body.inferenceConfig.inferenceSpec.containerResourceConfig.dict()

        self.customlog.debug('projectId==%s',projectId)
        quotaExc:bool = GlobalValidations.isQuotaExceeded(self.loggedUser, projectId, resConfig)
        GlobalValidations.updateResourceUsage(self.loggedUser, projectId, resConfig, "allocate")

        projectObj  = self.projectColl.find_one({'id':projectId,'isDeleted':False},{"_id":0}) 
        tenantObj  = self.tenantColl.find_one({'id':projectObj['tenantId'],'isDeleted':False},{"_id":0})
        tenantName = tenantObj['name']

        servingFramework = body.inferenceConfig.servingFramework

        if body.createdOn is None or body.createdOn=='':
            body.createdOn = datetime.utcnow()
        if body.createdBy is None or body.createdBy=='':
            body.createdBy = self.loggedUser
        deployDict = body.dict()
        deployDict['status'] = DEPLOYMENT_STATUS_INPROGRESS
        deployDict['id'] = randomDeployId
        deployId = self.deployColl.insert_one(deployDict).inserted_id
        self.customlog.debug('Deployment Record inserted with _id==%s', deployId)
        
        if JENKINS_CUSTOM == servingFramework.upper():
            statusCode, jobId = self._invokeCustomJenkinsDeployment(body, modelObj, randomDeployId,tenantName)
        elif JENKINS_TRITON == servingFramework.upper():
            statusCode, jobId = self._invokeTritonJenkinsDeployment(body, modelObj, randomDeployId,tenantName)
        elif JENKINS_DJL == servingFramework.upper():
            statusCode, jobId = self._invokeDjlJenkinsDeployment(body, modelObj, randomDeployId,tenantName)

        deployDict['devOpsJobId'] = jobId
        deployRespD = DeploymentResponseData.parse_obj(deployDict)
        self.customlog.debug('START createModelDeployment')
        return deployRespD

    def _getJenkinsCrumbData(self):
        self.customlog.debug('START _getJenkinsCrumbData')

        jobHeaders = {'content-type': 'application/json'}
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])
        crumb_data = requests.get(self.config['JENKINS_AUTH_URL'], auth=jobAuth, headers=jobHeaders)
        
        self.customlog.debug('END _getJenkinsCrumbData')
        return crumb_data
    
    def _deleteJobParams(self):
        self.customlog.debug('START _createJobParams')
        inputData = {}
        randomJobId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        inputData['jobId'] = randomJobId
        inputData['deployEnv'] = self.config.get('JENKINS_DEPLOY_ENV')

    #To create job params for jenkins job
    def _createJobParams(self, body: Deployment, modelObj) :
        self.customlog.debug('START _createJobParams')
        inputData = {}
        randomJobId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        userId = re.sub(r'[^a-zA-Z -]+', r'-', self.loggedUser)
        #mVersion = re.sub(r'[^a-zA-Z0-9 -]+', r'-', modelObj['version'])
        inputData['jobId'] = randomJobId
        inputData['deployEnv'] = self.config.get('JENKINS_DEPLOY_ENV')
        inputData['userName'] = userId
        inputData['projectId'] = modelObj['projectId']
        inputData['modelName'] = modelObj['name']
        inputData['endpointId'] = body.endpointId
        inputData['containerImage'] = modelObj.get('container')['imageUri']
        inputData['modelVersion'] = modelObj.get('version')
        inputData['modelS3RepoPath'] = modelObj.get('artifacts').get('uri')
        inputData['inputMode'] = modelObj.get('artifacts').get('storageType')
        
        #ports = modelObj.get('container')['ports'] if modelObj.get('container')['ports'] is not None else []
        inputData['ports'] = modelObj.get('container').get('ports') if modelObj.get('container').get('ports') is not None else []
        inputData['envVariables'] = modelObj.get('container').get('envVariables') if modelObj.get('container').get('envVariables') is not None else []
        inputData['labels'] = modelObj.get('container').get('labels') if modelObj.get('container').get('labels') is not None else []
        if modelObj.get('container').get('command') is not None :
            inputData['command'] = modelObj.get('container').get('command')
        if modelObj.get('container').get('args') is not None :
            inputData['args'] = modelObj.get('container').get('args')
        if modelObj.get('container').get('healthProbeUri') is not None :
            inputData['healthProbeUri'] = modelObj.get('container').get('healthProbeUri')
        inputData['inferenceSpec'] = body.inferenceConfig.inferenceSpec.dict()

        self.customlog.debug('END _createJobParams')
        return inputData

    #This methou is used to insetr the job details in idp_job_details collection
    def _insertIdpJobDetails(self, body: Deployment, jobParams:dict):
        self.customlog.debug('START _insertIdpJobDetails')
                
        jobId = jobParams['jobId']
        servingFramework = body.inferenceConfig.servingFramework

        if JENKINS_CUSTOM == servingFramework.upper():
            jobName = self.config['JENKINS_CUSTOM_JOB_NAME']
        elif JENKINS_TRITON == servingFramework.upper():
            jobName = self.config['JENKINS_TRITON_JOB_NAME']
        elif JENKINS_DJL == servingFramework.upper():
            jobName = self.config['JENKINS_DJL_JOB_NAME']
        
        #request_json = "{'header'=" + str(header) + ",\n'body'=" + str(body) + "\n}"
        self.customlog.info('request_json==%s', jobParams)
        self.customlog.info('job name==%s', jobName)

        if body.createdOn is None:
            body.createdOn = datetime.utcnow()
        if body.createdBy is None:
            body.createdBy = self.loggedUser

        idpLogDict = {'_id': ObjectId(jobId), 'jobName': jobName, 'status':JOB_STATUS_INPROGRESS, 
                      'requestJson': {'jobId': jobId, 'inputData':jobParams},
                    'responseJson':{}, 'createdOn':  body.createdOn, 'createdBy': body.createdBy,
                    'modifiedOn': '', 'updatedBy': '',
                    'isDeleted': False}
        
        idpLogId = self.idpLogColl.insert_one(idpLogDict).inserted_id
        self.customlog.info('inserted idp_log_details record==%s', idpLogId)

        self.customlog.debug('END _insertIdpJobDetails')
        return idpLogId
    
    """
    Invokes Jenkins pipelime job for CUSTOM model deployment
    """    
    def _invokeCustomJenkinsDeployment(self, body: Deployment, modelObj, deploymentId,tenantName):
        self.customlog.debug('START invokeCustomJenkinsDeployment')
        
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])
        
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json',
                        'Jenkins-Crumb': crumbData.json()['crumb']}
            
            jobParams = self._createJobParams(body, modelObj)
            jobParams['deploymentId'] = deploymentId
            endpointObj = self._getEndpointDetails(body.endpointId)
            jobParams['contextUri'] = endpointObj.get('contextUri')
            jobParams['endpointVersion'] = self.config.get('ENDPOINT_API_VERSION', 'v1')
            jobParams['tenantName'] = tenantName

            self.customlog.debug('Job Params===%s', str(jobParams))

            self._insertIdpJobDetails(body, jobParams)
            
            jenkinsParam = {}
            jenkinsParam['token'] = self.config['JENKINS_API_TOKEN']
            jenkinsParam['jobId'] = jobParams['jobId']
            jenkinsParam['deploymentId'] = jobParams['deploymentId']
            jenkinsParam['deployEnv'] = jobParams['deployEnv']
            jenkinsParam['userName'] = jobParams['userName']

            print(str(jenkinsParam))
            data = requests.get(self.config['JENKINS_CUSTOM_DEPLOY_URL'], auth=jobAuth, 
                        params=jenkinsParam, headers=jobHeaders)
            statusCode = str(data.status_code)
            
            self.customlog.info('Jenkins Deployment API Output==%s', statusCode)
            if statusCode == "201":
                self.customlog.debug("Jenkins job is triggered")
                self._updateJobIdInDeployment(jobParams['jobId'], jobParams['deploymentId'])
            else:
                self.customlog.debug("Failed to trigger the Jenkins job")

        self.customlog.debug('END invokeCustomJenkinsDeployment')
        return statusCode, jobParams['jobId']

    """
    Invokes Jenkins pipelime job for TRITON model deployment
    """    
    def _invokeTritonJenkinsDeployment(self, body: Deployment, modelObj, deploymentId,tenantName):
        self.customlog.debug('START invokeTritonJenkinsDeployment')
        
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])
        
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json',
                        'Jenkins-Crumb': crumbData.json()['crumb']}
        
            jobParams = self._createJobParams(body, modelObj)
            jobParams['deploymentId'] = deploymentId
            endpointObj = self._getEndpointDetails(body.endpointId)
            jobParams['contextUri'] = endpointObj.get('contextUri')
            jobParams['endpointVersion'] = self.config.get('ENDPOINT_API_VERSION', 'v1')
            jobParams['tenantName'] = tenantName
            
            if body.inferenceConfig.servingSpec is not None and body.inferenceConfig.servingSpec.tritonSpec is not None and body.inferenceConfig.servingSpec.tritonSpec.logLevel is not None:
                jobParams['tritonLogLevel'] = body.inferenceConfig.servingSpec.tritonSpec.logLevel
            self.customlog.debug('Job Params===%s', str(jobParams))
            
            self._insertIdpJobDetails(body, jobParams)

            jenkinsParam = {}
            jenkinsParam['token'] = self.config['JENKINS_API_TOKEN']
            jenkinsParam['jobId'] = jobParams['jobId']
            jenkinsParam['deploymentId'] = jobParams['deploymentId']
            jenkinsParam['deployEnv'] = jobParams['deployEnv']
            jenkinsParam['userName'] = jobParams['userName']

            data = requests.get(self.config['JENKINS_TRITON_DEPLOY_URL'], auth=jobAuth, 
                          params=jenkinsParam, headers=jobHeaders)

            statusCode = str(data.status_code)
            self.customlog.info('Jenkins Deployment API Output==%s', statusCode)
            if statusCode == "201":
                print("Jenkins job is triggered")
                self._updateJobIdInDeployment(jobParams['jobId'], jobParams['deploymentId'])
            else:
                print("Failed to trigger the Jenkins job")

        self.customlog.debug('END invokeTritonJenkinsDeployment')
        return statusCode, jobParams['jobId']

    """
    Invokes Jenkins pipelime job for TRITON model deployment
    """    
    def _invokeDjlJenkinsDeployment(self, body: Deployment, modelObj, deploymentId,tenantName):
        self.customlog.debug('START invokeDjlJenkinsDeployment')
        
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])
        
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json',
                        'Jenkins-Crumb': crumbData.json()['crumb']}
            
            jobParams = self._createJobParams(body, modelObj)

            jobParams['deploymentId'] = deploymentId
            
            endpointObj = self._getEndpointDetails(body.endpointId)
            jobParams['contextUri'] = endpointObj.get('contextUri')
            jobParams['endpointVersion'] = self.config.get('ENDPOINT_API_VERSION', 'v1')
            jobParams['tenantName'] = tenantName
            
            self._insertIdpJobDetails(body, jobParams)
            
            jenkinsParam = {}
            jenkinsParam['token'] = self.config['JENKINS_API_TOKEN']
            jenkinsParam['jobId'] = jobParams['jobId']
            jenkinsParam['deploymentId'] = jobParams['deploymentId']
            jenkinsParam['deployEnv'] = jobParams['deployEnv']
            jenkinsParam['userName'] = jobParams['userName']

            data = requests.get(self.config['JENKINS_DJL_DEPLOY_URL'], auth=jobAuth, 
                          params=jenkinsParam, headers=jobHeaders)

            statusCode = str(data.status_code)
            #statusCode="201"
            self.customlog.info('Jenkins Deployment API Output==%s', statusCode)
            if statusCode == "201":
                print("Jenkins job is triggered")
                self._updateJobIdInDeployment(jobParams['jobId'], jobParams['deploymentId'])
            else:
                print("Failed to trigger the Jenkins job")

        self.customlog.debug('END invokeDjlJenkinsDeployment')
        
        return statusCode, jobParams['jobId'] #statusCode,
    
    #To get the endpoint details based on the endpoint id.
    def _getEndpointDetails(self, endpoint_id) :
        endpointObj = self.endpointColl.find_one({"id": endpoint_id, "isDeleted": False, "status":"Created"}, {"_id":0})
        if endpointObj is None:
            raise NotFoundException(3600,errorCodeMsgDict['3600'])
        self.customlog.debug("ENDPOINT OBJECT : %s",endpointObj)
        return endpointObj
    
    #To get the endpoint details based on the endpoint id.
    def getEndpoint (self, endpoint_id) :
        print("inside getEndpoint",endpoint_id)   

        endpointObj = self._getEndpointDetails(endpoint_id)

        projectObj = self.projectColl.find_one({'id':endpointObj['projectId'],'isDeleted':False},{"_id":0})
        if projectObj is None:
            print('No project Associated with this Endpoint ID')
            raise NotFoundException('3000','No project Associated with this Endpoint ID')
        print("PROJECT OBJECT : ",projectObj)

        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, endpointObj['projectId'], DEPLOY_MODEL)
        if hasUserAccess == False:
            raise ForbiddenException()

        return EndpointResponseData.parse_obj(endpointObj)
    
    #To get the deployment status based on the deployment id.
    def getDeploymentStatus(self, deployment_id, user_id):

        deployObj = self.deployColl.find_one({'id':deployment_id,'isDeleted':False},{"_id":0})

        if deployObj is None:
            raise ModelAPIBusinessError('3622')

        modelObj = self.modellColl.find_one({'id':deployObj['modelId'],'isDeleted':False},{"_id":0})

        projectObj = self.projectColl.find_one({'id':modelObj['projectId'],'isDeleted':False},{"_id":0})

        if projectObj is None:
            print('No project Associated with this Endpoint ID')
            raise NotFoundException('3000','No project Associated with this Deployment')
        print("PROJECT OBJECT : ",projectObj)

        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, modelObj['projectId'], VIEW)
        if hasUserAccess == False:
            raise ForbiddenException()
        
        if deployObj['status'] in [DeploymentStatusEnum.Deployed,DeploymentStatusEnum.DeleteInProgress,DeploymentStatusEnum.InProgress]:
            return deployObj

        if deployObj['status'] == DeploymentStatusEnum.Failed:
            idpJobObj =self.idpLogColl.find_one({'requestJson.inputData.deploymentId':deployObj['id'],'isDeleted':False},{"_id":0})
            print(idpJobObj)
            raise JenkinsJobError(idpJobObj['responseJson']['errorMsg'])

     #This method is used to delete the and point and its associated model deployment  
    def deleteEndpoint(self,endpoint_id):

        endpointObj = self._getEndpointDetails(endpoint_id)

        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, endpointObj['projectId'], DEPLOY_MODEL)
        if hasUserAccess == False:
            raise ForbiddenException()

        
        if 'deployedModels' in endpointObj:
            
            deployModels=endpointObj['deployedModels']
            if deployModels != None:

                inputData={}
                depjobidlist =[]
                modelNameList=[]
                modelVersionList=[]
                depFrameworkList=[]
                projectIdList=[]
                for deploy in deployModels:
                    deploymentId = deploy['deploymentId']
                    deployObj = self.deployColl.find_one({'id':deploymentId,'status':DeploymentStatusEnum.Deployed,'isDeleted':False},{"_id":0})
                    if deployObj is None:
                            raise ModelAPIBusinessError('3622')
                    modelVersionList.append(deployObj['version'])
                    depFrameworkList.append(deployObj['inferenceConfig']['servingFramework'])
                    modelObj = self.modellColl.find_one({'id':deployObj['modelId'],'isDeleted':False},{"_id":0})
                    projectObj  = self.projectColl.find_one({'id':modelObj['projectId'],'isDeleted':False},{"_id":0}) #added by Gokul
                    tenantObj  = self.tenantColl.find_one({'id':projectObj['tenantId'],'isDeleted':False},{"_id":0})
                    tenantName = tenantObj['name']
                    modelNameList.append(modelObj['name'])
                    projectIdList.append(modelObj['projectId'])
                    jobParams = self._createJobParamsForDelete(deployObj, modelObj)
                    jobName = self.config['JENKINS_DELETEDEPL_JOB_NAME']
                    jobParams['tenantName'] = tenantName
                    self.customlog.debug('Job Params===%s', jobParams)
                    idpLogDict = {'_id': ObjectId(jobParams['jobId']), 'jobName': jobName, 'status':JOB_STATUS_INPROGRESS, 
                      'requestJson': {'jobId': jobParams['jobId'], 'inputData':jobParams},
                    'responseJson':{}, 'createdOn':  datetime.utcnow(), 'createdBy': self.loggedUser,
                    'modifiedOn': '', 'updatedBy': '',
                    'isDeleted': False}
                    depjobid = self._insertIdpJobDetailsForDelete(idpLogDict)
                    depjobidlist.append(depjobid)
                    self._updateJobIdInDeployment(depjobid, deploymentId)
                inputData['depjobidlist']= depjobidlist
                inputData['modelNameList']= modelNameList
                inputData['modelVersionList']= modelVersionList   
                inputData['depFrameworkList']= depFrameworkList
                inputData['projectIdList']= projectIdList
                inputData['tenantName']=tenantName

            
                statusCode = self._invokeDeleteEndpointJenkins(endpoint_id,inputData) 
              
                if statusCode == "201":
                    print("Jenkins job is triggered")
                    filter = {'jobId':{"$in":depjobidlist},'status':DeploymentStatusEnum.Deployed,'isDeleted':False}                                  
                    newValues = { '$set': {'status': DeploymentStatusEnum.DeleteInProgress}}
                    self.deployColl.update_many(filter,newValues)
                    filter = {"id": endpoint_id, "isDeleted": False, "status":EndpointStatuseEnum.Created}
                    self.endpointColl.update_one(filter,{"$set":{'status':EndpointStatuseEnum.DeleteInProgress}})
                    Resp = {'Message': endpoint_id+" endpoint and asscoicated deployment deletion is inprogress."}
                    return Resp
                else:
                    print("Failed to trigger the Jenkins job")
                    Resp = {'Message': "Some error occured while deleting the endpoint, Please try again later."}  
                    return Resp
                
                      
        else:
        
                filter = {"id": endpoint_id, "isDeleted": False, "status":EndpointStatuseEnum.Created}
                self.endpointColl.update_one(filter,{"$set":{'status':EndpointStatuseEnum.Deleted,'isDeleted':True}})
                print("changed")
                Resp = {'Message': endpoint_id+" endpoint deleted"}
                return Resp

    #This method is used to invoke the Jenkins job for deleting the endpoint and its associated model deployment    
    def _invokeDeleteEndpointJenkins(self,endpoint_id,inputData):
        self.customlog.debug('START invokeDeleteEndpointJenkins')
        
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])
        
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json',
                        'Jenkins-Crumb': crumbData.json()['crumb']}
            
            randomJobId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
            
            jobParams={}
            jobParams['jobId'] = randomJobId
            jobParams['endpointId'] = endpoint_id
            jobParams['inputDataList'] = inputData
            self.customlog.debug('Job Params===%s', str(jobParams))

            jobName = self.config['JENKINS_DELETE_ENDPOINT_JOB_NAME']
        

            self.customlog.info('request_json==%s', jobParams)
            self.customlog.info('job name==%s', jobName)

            idpLogDict = {'_id': ObjectId(jobParams['jobId']), 'jobName': jobName, 'status':JOB_STATUS_INPROGRESS, 
                        'requestJson': {'jobId': jobParams['jobId'],'endpointId':jobParams['endpointId'],'inputData':jobParams['inputDataList']},
                        'responseJson':{}, 'createdOn': datetime.utcnow(), 'createdBy': self.loggedUser,
                        'modifiedOn': '', 'updatedBy': '',
                        'isDeleted': False}

            self._insertIdpJobDetailsForDelete(idpLogDict)

            jenkinsParam = {}
            jenkinsParam['endpointId']=jobParams['endpointId']
            jenkinsParam['jobId'] = jobParams['jobId']
            jenkinsParam['deployEnv'] = self.config['JENKINS_DEPLOY_ENV']
            print("****",self.config['JENKINS_DELETE_ENDPOINT_URL'])
          
            
            data = requests.post(self.config['JENKINS_DELETE_ENDPOINT_URL'], auth=jobAuth, 
                          params=jenkinsParam, headers=jobHeaders)
            

            statusCode = str(data.status_code)
            print(data)
            self.customlog.info('Jenkins Deleteendpoint API Output==%s', statusCode)
            if statusCode == "201":
                print("Jenkins job is triggered")
                
            else:
                print("Failed to trigger the Jenkins job")
        self.customlog.debug('END invokeDeleteEndpointJenkins')
        return statusCode

    #This method is used to get all the endpoints created under given project
    def getAllEndpoint(self, projectId):
        print("inside getAllEndpoint")         
        endpointColl = self.app.database["endpoint"]
        isProjectPresent = self.commonService.checkIfProjectExists(projectId)
        if isProjectPresent == False:
            raise NotFoundException('1002',errorCodeMsgDict['1002'])
            
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, projectId, VIEW)
        if hasUserAccess == True :
            endpointList = list(endpointColl.find({'projectId': projectId, 'isDeleted': False},{"_id" : 0}))
            #sorting the list in descending order based on createdOn date
            endpointList_sorted=sorted(endpointList, key=lambda i: (i['createdOn']), reverse=True) 
        else :
            raise ForbiddenException()
        
        return endpointList_sorted
    
    #This method is used to delete the deployment based on the deployment id
    def deleteDeployment(self,deployment_id,delete):       
        
        deployObj = self.deployColl.find_one({"id": deployment_id, "isDeleted": False,"status":DeploymentStatusEnum.Deployed}, {"_id":0})        
        if deployObj is None:
            raise ModelAPIBusinessError('3627')     
        modelObj = self.modellColl.find_one({'id':deployObj['modelId'],'isDeleted':False},{"_id":0})     
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, modelObj['projectId'], DEPLOY_MODEL)
        if hasUserAccess == False:
            raise ForbiddenException()        
        projectObj  = self.projectColl.find_one({'id':modelObj['projectId'],'isDeleted':False},{"_id":0}) 
        tenantObj  = self.tenantColl.find_one({'id':projectObj['tenantId'],'isDeleted':False},{"_id":0})
        tenantName = tenantObj['name']
        filter = {"id": deployment_id, "isDeleted": False}               
        statusCode = self.jenkinsDeleteDeployment(deployObj, modelObj,tenantName,delete)

        if statusCode == "201":
            print("Jenkins job is triggered")
            self.deployColl.update_one(filter,{"$set":{'status':DeploymentStatusEnum.DeleteInProgress}})
            Resp = {'Message': deployment_id+" deletion inprogress."}
            return Resp
        else:
            print("Failed to trigger the Jenkins job")
            Resp = {'Message': "Some error occured while deleting the deployment, Please try again later."}  
            return Resp
                
    #This method is used to invoke jenkins to delete the deployment
    def jenkinsDeleteDeployment(self, deployObj, modelObj,tenantName,delete):        
        self.customlog.debug('START jenkinsDeleteDeployment')
        jobAuth = (self.config['JENKINS_USER'], self.config['JENKINS_API_TOKEN'])        
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json',
                        'Jenkins-Crumb': crumbData.json()['crumb']}            
            jobParams = self._createJobParamsForDelete(deployObj, modelObj)
            self.customlog.debug('Job Params===%s', jobParams)            
            data = requests.post(self.config['JENKINS_DELETE_DEPLOY_URL'], auth=jobAuth,params=jobParams, headers=jobHeaders)
            self.customlog.debug(data)
            statusCode = str(data.status_code)
            jobParams['tenantName'] = tenantName
            self.customlog.info('Jenkins Deployment API Output==%s', statusCode)
            if statusCode == "201":
                print("Jenkins job is triggered")
                if delete=="deployment":
                    jobName = self.config['JENKINS_DELETEDEPL_JOB_NAME']
                    self.customlog.info('job name==%s', jobName) 
                else:
                    jobName = DELETE_MODEL
                    self.customlog.info('job name==%s', jobName)     
                self.customlog.info('request_json==%s', jobParams)
                idpLogDict = {'_id': ObjectId(jobParams['jobId']), 'jobName': jobName, 'status':JOB_STATUS_INPROGRESS, 
                        'requestJson': {'jobId': jobParams['jobId'], 'inputData':jobParams},
                    'responseJson':{}, 'createdOn':  datetime.utcnow(), 'createdBy': self.loggedUser,
                    'modifiedOn': '', 'updatedBy': '',
                    'isDeleted': False}

                self._insertIdpJobDetailsForDelete(idpLogDict)
                self._updateJobIdInDeployment(jobParams['jobId'], deployObj['id'])		
            else:
                print("Failed to trigger the Jenkins job")
        self.customlog.debug('END jenkinsDeleteDeployment')
        return statusCode

    #This method is used to create job parameters for delete deployment
    def _createJobParamsForDelete(self,deployObj,modelObj) :
        self.customlog.debug('START _createJobParamsForDelete')
        randomJobId = ''.join(random.choices('0123456789abcdef', k=int(self.config['RANDOM_JOB_ID_CHARACTERS'])))
        inputData={}
        inputData['jobId'] = randomJobId
        inputData['deployEnv'] = self.config.get('JENKINS_DEPLOY_ENV')
        inputData['projectId'] = modelObj['projectId']
        inputData['modelName'] = modelObj['name']
        inputData['modelVersion'] = deployObj['version']
        inputData['deployFramework']=deployObj['inferenceConfig']['servingFramework']         
        self.customlog.debug('END _createJobParamsForDelete')  
        return inputData       

    #This method is used to insert the job details in idp_job_details collection for delete deployment
    def _insertIdpJobDetailsForDelete(self,idpLogDict) :          
        self.customlog.debug('START _insertIdpJobDetailsForDelete')                
        idpLogId = self.idpLogColl.insert_one(idpLogDict).inserted_id
        self.customlog.info('inserted idp_log_details record==%s', idpLogId)
        self.customlog.debug('END _insertIdpJobDetailsForDelete')
        return idpLogDict['requestJson']['jobId']

        
    