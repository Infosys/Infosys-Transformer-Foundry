# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: utility_service.py
description: Service details for aicloud utility operations
"""
from bson.objectid import ObjectId
from utilities.config.logger import CustomLogger
from utilities.mappers.idp_job_response import IdpJobDetailsModel, KnativeJobResponse,TritonJobResponse,PipelineJobResponse,DeleteDeploymentJobResponse,DeleteEndpointJobResponse,ESBulkData
from aicloudlibs.validations.global_validations import GlobalValidations
from utilities.exception.util_exception import JobDetailsNotFoundError,EndPointDetailsNotFoundError,DeploymentNotDeletedError
from utilities.constants.util_constants import JOB_DETAILS_NOT_FOUND,JOB_ID_NOT_EMPTY,ENDPOINT_DETAILS_NOT_FOUND,DEPLOYMENT_NOT_DELETED,MODEL_STATUS_UNDEPLOYED
from datetime import datetime
from bson.objectid import ObjectId
import pydantic
from aicloudlibs.schemas.pipeline_mappers import TrialStatusEnum
from aicloudlibs.schemas.model_mappers import DeploymentStatusEnum, ModelStatusEnum
import re
import os
import requests
from urllib.parse import urlsplit
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time
import calendar
from utilities.constants.util_constants import *
from requests.auth import HTTPBasicAuth
import json
from fastapi.encoders import jsonable_encoder

class UtilityService:

    def __init__(self,app):
        self.log = app.logger
        self.db=app

    # Method to update Knative Job Status
    def updateKnativeJobStatus(self, jobDetails: KnativeJobResponse):
        self.log.info('Enter updateKnativeJobStatus')
        if jobDetails.jobId is None:
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        else:
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 
                        'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if jobDetails.jobStatus.strip().lower() == "success":
                deployCol1 = self.db.database['deployment']
                deployfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                deployObj=deployCol1.find_one({'jobId': jobDetails.jobId})
                if deployObj is not None:
                    newValues = {'$set': {'status': DeploymentStatusEnum.Deployed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "false")}}
                    result = deployCol1.update_one(deployfilter, newValues)
                    
                    self.log.info("updated deployment table for deployment Id "+ str(deployObj['_id']) +" with status "+DeploymentStatusEnum.Deployed)
                    modelId= deployObj['modelId']
                    version= deployObj['version']
                    modelCol1 = self.db.database['model']
                    
                    modelfilter = {'id': modelId,'version':version, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                    modelObj=modelCol1.find_one(modelfilter)
                    if modelObj is not None:
                        newValues = {'$set': {'status': ModelStatusEnum.Deployed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at}}
                result = modelCol1.update_one(modelfilter, newValues)   

                """update endpoint details start"""

                endpointColl=self.db.database['endpoint']
                endpointFilter={'id':deployObj['endpointId'],'isDeleted':pydantic.parse_obj_as(bool, "false")}
                endpointObj=endpointColl.find_one(endpointFilter)
               
                if 'deployedModels' not in endpointObj:
                    endpointObj['deployedModels'] = []
                updateDict = {}
                endpointArr = []
                updateDict.update(modelId = deployObj['modelId']),
                updateDict.update(version = deployObj['version']),
                updateDict.update(deploymentId = deployObj['id']),
                modelSpecArr = deployObj['inferenceConfig']['inferenceSpec']['modelSpec']
                for modelSpec in modelSpecArr:
                    modelUri = modelSpec.get('modelUris')
                    endpointUri = os.getenv("API_ENDPOINT")+'v1'+endpointObj['contextUri']+modelUri['prefixUri']+"/models/"+modelObj['name']+"/versions/"+str(modelObj['version'])+modelUri['predictUri']
                    endpointArr.append(endpointUri)
                updateDict.update(endpointUri = endpointArr)    
                endpointObj['deployedModels'].append(updateDict)
                endpointObject = endpointColl.update_one({"id": deployObj['endpointId']}, {"$set": endpointObj})

                """update endpoint details end"""
                self.log.info("updated Model table for Model Id "+modelId +" with status "+ModelStatusEnum.Deployed)
                self.log.info('Exit updateKnativeJobStatus')
                return idpmodel
            else:
                deployColl = self.db.database['deployment']
                deployfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                deployObj=deployColl.find_one(deployfilter)
                
                if deployObj is not None:
                    print(DeploymentStatusEnum.Failed)
                    newValues = {'$set': {'status': DeploymentStatusEnum.Failed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "false")}}
                    result = deployColl.update_one(deployfilter, newValues)
                    modelId = deployObj['modelId']
                    version= deployObj['version'] 
                    modelColl = self.db.database['model']
                    modelfilter = {'id': modelId, 'version':version,'isDeleted': pydantic.parse_obj_as(bool, "false")}
                    modelObj=modelColl.find_one(modelfilter)
                    if modelObj is not None:
                        newValues = {'$set': {'status': ModelStatusEnum.Registered, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at}}
                    result = modelColl.update_one(modelfilter, newValues)
                    reqResourceQuota=deployObj['inferenceConfig']['inferenceSpec']['containerResourceConfig']
                    print(reqResourceQuota)
                    userId=deployObj['createdBy']
                    flag="deallocate"
                    resp=GlobalValidations.updateResourceUsage(userId,modelObj['projectId'],reqResourceQuota,flag)
     
    # Method to update Triton Job Status
    def updateTritonJobStatus(self, jobDetails: TritonJobResponse):
        self.log.info('Enter updateTritonJobStatus')
        print('Enter updateTritonJobStatus')
        if jobDetails.jobId is None:
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        else:
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if jobDetails.jobStatus.strip().lower() == "success":
                deployCol1 = self.db.database['deployment']
                deployfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                deployObj=deployCol1.find_one({'jobId': jobDetails.jobId})
                if deployObj is not None:
                    newValues = {'$set': {'status': DeploymentStatusEnum.Deployed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "false")}}
                    result = deployCol1.update_one(deployfilter, newValues)
                    
                    self.log.info("updated deployment table for deployment Id "+ str(deployObj['_id']) +" with status UNDEPLOYED")
                    modelId= deployObj['modelId']
                    version= deployObj['version']
                    modelCol1 = self.db.database['model']
                    
                    modelfilter = {'id': modelId,'version':version, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                    modelObj=modelCol1.find_one(modelfilter)
                    if modelObj is not None:
                        newValues = {'$set': {'status': ModelStatusEnum.Deployed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at}}
                result = modelCol1.update_one(modelfilter, newValues)

                """update endpoint details start"""

                endpointColl=self.db.database['endpoint']
                endpointFilter={'id':deployObj['endpointId'],'isDeleted':pydantic.parse_obj_as(bool, "false")}
                endpointObj=endpointColl.find_one(endpointFilter)
                if 'deployedModels' not in endpointObj:
                    endpointObj['deployedModels'] = []
                updateDict = {}
                endpointArr = []
                updateDict.update(modelId = deployObj['modelId']),
                updateDict.update(version = deployObj['version']),
                updateDict.update(deploymentId = deployObj['id']),
                modelSpecArr = deployObj['inferenceConfig']['inferenceSpec']['modelSpec']
                for modelSpec in modelSpecArr:
                    modelUri = modelSpec.get('modelUris')
                    endpointUri = os.getenv("API_ENDPOINT")+'v1'+endpointObj['contextUri']+modelUri['prefixUri']+"/models/"+modelObj['name']+"/versions/"+str(modelObj['version'])+modelUri['predictUri']
                    endpointArr.append(endpointUri)
                updateDict.update(endpointUri = endpointArr)    
                endpointObj['deployedModels'].append(updateDict)
                endpointObject = endpointColl.update_one({"id": deployObj['endpointId']}, {"$set": endpointObj})

                """update endpoint details end"""
                self.log.info("updated Model table for Model Id "+modelId +" with status UNDEPLOYED")
                self.log.info('Exit updateKnativeJobStatus')
                return idpmodel
            else:
                deployColl = self.db.database['deployment']
                deployfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                deployObj=deployColl.find_one(deployfilter)
                
                if deployObj is not None:
                    newValues = {'$set': {'status': DeploymentStatusEnum.Failed, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "false")}}
                    result = deployColl.update_one(deployfilter, newValues)
                    modelId = deployObj['modelId']
                    version= deployObj['version'] 
                    modelColl = self.db.database['model']
                    modelfilter = {'id': modelId,'version':version, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                    modelObj=modelColl.find_one(modelfilter)
                    if modelObj is not None:
                        newValues = {'$set': {'status': ModelStatusEnum.Registered, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at}}
                    result = modelColl.update_one(modelfilter, newValues)
                    reqResourceQuota=deployObj['inferenceConfig']['inferenceSpec']['containerResourceConfig']
                    print(reqResourceQuota)
                    userId=deployObj['createdBy']
                    flag="deallocate"
                    resp=GlobalValidations.updateResourceUsage(userId,modelObj['projectId'],reqResourceQuota,flag)
        
    # Method to fetch Details of a Job
    def fetchDetails(self, jobId: str):
        self.log.info('Enter fetchDetails')
        print("Enter fetchDetails")
        print(jobId)
        if jobId is None:
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        else:
            filter = {'_id': ObjectId(jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            print(row)
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = row['requestJson']
            self.log.info('Exit updateKnativeJobStatus')
            return respDict

    # Method to update Pipeline Job Status
    def updatePipelineJobStatus(self, jobDetails: PipelineJobResponse):
        self.log.info('Enter updatePipelineJobStatus')
        print('Enter updatePipelineJobStatus')
        if jobDetails.jobId is None:
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY) 
        else:
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            print(row)
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if jobDetails.jobStatus.strip().lower() == "success":
                trialColl = self.db.database['trial']
                trialfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                trialObj=trialColl.find_one(trialfilter)
                if trialObj is not None:
                    newValues = {'$set': {'status': TrialStatusEnum.InProgress, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'kubeflowRunID':jobDetails.runId}}
                    result = trialColl.update_one(trialfilter, newValues)
                    self.log.info("updated Trial table with kubeflowRunID"+jobDetails.runId +"For Trial: "+ row['requestJson']['inputData']['runId'])
                    self.log.info('Exit updatePipelineJobStatus')
                else:
                    self.log.info("Not able to update the Kubeflow Run Reference Id For Trial: "+ row['requestJson']['inputData']['runId']+" in DB.Please connect the administrator for the same")
                    idpmodel={"message: Not able to update the Kubeflow Run Reference Id in DB.Please connect the administrator for the same " }
                return idpmodel
            else:
                trialColl = self.db.database['trial']
                trialfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                trialObj=trialColl.find_one(trialfilter)
                if trialObj is not None:
                    projectId=trialObj['projectId']
                    reqResourceQuota=trialObj['resourceConfig']
                    userId=trialObj['createdBy']
                    flag="deallocate"
                    resp=GlobalValidations.updateResourceUsage(userId,projectId,reqResourceQuota,flag)
                    self.log.info("updated resourceQuota"+jobDetails.runId +"For Trial: "+ row['requestJson']['inputData']['runId'])
                    self.log.info('Exit updatePipelineJobStatus')
                     
    # Method to update Delete Deployment Job Status
    def updateDeleteDeploymentJobStatus(self, jobDetails: PipelineJobResponse):
        self.log.info('Enter updateDeleteDeploymentJobStatus')
        print('Enter updateDeleteDeploymentJobStatus')
        if jobDetails.jobId is None or jobDetails.jobId =='':
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        
        else:
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            print(row)
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if jobDetails.jobStatus.strip().lower() == "success":
                deployCol1 = self.db.database['deployment']
                deployfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                deployObj=deployCol1.find_one({'jobId': jobDetails.jobId})
                if deployObj is not None:
                    newValues = {'$set': {'status': DeploymentStatusEnum.Deleted, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "true")}}
                    result = deployCol1.update_one(deployfilter, newValues)
                    
                    self.log.info("updated deployment table for deployment Id "+ str(deployObj['_id']) +" with status UNDEPLOYED")
                    modelId= deployObj['modelId']
                    version= deployObj['version']
                    modelCol1 = self.db.database['model']
                    
                    modelfilter = {'id': modelId, 'version':version,'isDeleted': pydantic.parse_obj_as(bool, "false")}
                    modelObj=modelCol1.find_one(modelfilter)
                    if modelObj is not None and row['jobName']=="delete_model_deployment":
                        newValues = {'$set': {'status': MODEL_STATUS_UNDEPLOYED, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at}}
                    elif modelObj is not None and row['jobName']=="delete_model":
                        newValues = {'$set': {'status': ModelStatusEnum.Deleted, 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,"isDeleted":pydantic.parse_obj_as(bool, "true")}}
                result = modelCol1.update_one(modelfilter, newValues)
                """ delete endpoint details from deployed models start"""
                endpointcoll=self.db.database['endpoint']
                endpointFilter={'id':deployObj['endpointId']}
                endpointObj=endpointcoll.find_one(endpointFilter)
                for index,endpoint in enumerate(endpointObj['deployedModels']):
                    if endpoint['deploymentId'] == deployObj['id']:
                        endpointObj['deployedModels'].pop(index)
                        break
                endpointcoll.update_one(endpointFilter,{'$set':{'deployedModels':endpointObj['deployedModels']}})

                """ delete endpoint details from deployed models end"""
                flag="deallocate"
                reqResourceQuota=deployObj['inferenceConfig']['inferenceSpec']['containerResourceConfig']
                userId=deployObj['createdBy']
                resp=GlobalValidations.updateResourceUsage(userId,modelObj['projectId'],reqResourceQuota,flag)
                self.log.info("updated Model table for Model Id "+modelId +" with status UNDEPLOYED")
                self.log.info('Exit updateDeleteDeploymentJobStatus')
            return idpmodel 
        
    # Method to get authsession token
    def get_auth_session_token(self) ->dict:
        """
        Determine if the specified URL is secured by Dex and try to obtain a session cookie.
        WARNING: only Dex `staticPasswords` and `LDAP` authentication are currently supported
                (we default default to using `staticPasswords` if both are enabled)

        :param url: Kubeflow server URL, including protocol
        :param username: Dex `staticPasswords` or `LDAP` username
        :param password: Dex `staticPasswords` or `LDAP` password
        :return: auth session information
        """

        url=os.getenv("KFP_ENDPOINT")
        username=os.getenv("KFP_USERNAME")
        password=os.getenv("KFP_PASSWORD")

        # define the default return object
        auth_session = {
            "endpoint_url": url,    # KF endpoint URL
            "redirect_url": None,   # KF redirect URL, if applicable
            "dex_login_url": None,  # Dex login URL (for POST of credentials)
            "is_secured": None,     # True if KF endpoint is secured
            "session_cookie": None  # Resulting session cookies in the form "key1=value1; key2=value2"
        }

        # use a persistent session (for cookies)
        with requests.Session() as s:

            ################
            # Determine if Endpoint is Secured
            ################
            resp = s.get(url, allow_redirects=True)
            if resp.status_code != 200:
                raise RuntimeError(f"HTTP status code '{resp.status_code}' for GET against: {url}")

            auth_session["redirect_url"] = resp.url

            # if we were NOT redirected, then the endpoint is UNSECURED
            if len(resp.history) == 0:
                auth_session["is_secured"] = False
                return auth_session
            else:
                auth_session["is_secured"] = True

            ################
            # Get Dex Login URL
            ################
            redirect_url_obj = urlsplit(auth_session["redirect_url"])

            # if we are at `/auth?=xxxx` path, we need to select an auth type
            if re.search(r"/auth$", redirect_url_obj.path): 
                
                #######
                # TIP: choose the default auth type by including ONE of the following
                #######
                
                # OPTION 1: set "staticPasswords" as default auth type
                redirect_url_obj = redirect_url_obj._replace(path=re.sub(r"/auth$", "/auth/local", redirect_url_obj.path))
                # OPTION 2: set "ldap" as default auth type 
                # redirect_url_obj = redirect_url_obj._replace(path=re.sub(r"/auth$", "/auth/ldap", redirect_url_obj.path))
                
            # if we are at `/auth/xxxx/login` path, then no further action is needed (we can use it for login POST)
            if re.search(r"/auth/.*/login$", redirect_url_obj.path):
                auth_session["dex_login_url"] = redirect_url_obj.geturl()

            # else, we need to be redirected to the actual login page
            else:
                # this GET should redirect us to the `/auth/xxxx/login` path
                resp = s.get(redirect_url_obj.geturl(), allow_redirects=True)
                if resp.status_code != 200:
                    raise RuntimeError(f"HTTP status code '{resp.status_code}' for GET against: {redirect_url_obj.geturl()}")

                # set the login url
                auth_session["dex_login_url"] = resp.url

            ################
            # Attempt Dex Login
            ################
            resp = s.post(
                auth_session["dex_login_url"],
                data={"login": username, "password": password},
                allow_redirects=True
            )
            if len(resp.history) == 0:
                raise RuntimeError(
                    f"Login credentials were probably invalid - "
                    f"No redirect after POST to: {auth_session['dex_login_url']}"
                )

            # store the session cookies in a "key1=value1; key2=value2" string
            auth_session["session_cookie"] = "; ".join([f"{c.name}={c.value}" for c in s.cookies])

        return auth_session
    
    # Method to update Pipeline Status
    def updatePipelineStatus(self, jobDetails: PipelineJobResponse):
        self.log.info('Enter updatePipelineStatus')
        print('Enter updatePipelineStatus')
        if jobDetails.jobId is None:
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        else:
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            print(row)
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if row['jobName'] == "Pipeline execution":
                trialColl = self.db.database['pipeline_execution']
                trialfilter = {'jobId': jobDetails.jobId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                trialObj=trialColl.find_one(trialfilter)
                if trialObj is not None:
                        newValues = {'$set': {'status': "INPROGRESS", 'updatedBy': 'jenkins',
                                'modifiedOn': last_modified_at,'runId':jobDetails.runId}}
                        result = trialColl.update_one(trialfilter, newValues)
                        self.log.info("updated pipeline execution table with kubeflowRunID"+jobDetails.runId +"For execution: "+ row['requestJson']['inputData']['executionId'])
                        self.log.info('Exit updatePipelineJobStatus')
                else:
                        self.log.info("Not able to update the Kubeflow Run Reference Id For execution: "+ row['requestJson']['inputData']['executionId']+" in DB.Please connect the administrator for the same")
                        idpmodel={"message: Not able to update the Kubeflow Run Reference Id in DB.Please connect the administrator for the same " }
            return idpmodel
                
    # Method to update Endpoint Job Status
    def updateEndpointJobStatus(self, jobDetails: DeleteEndpointJobResponse):
        self.log.info('Enter updateEndpointJobStatus')
        # print('Enter updateDeleteDeploymentJobStatus')
        if jobDetails.jobId is None or jobDetails.jobId =='':
            raise JobDetailsNotFoundError(1056,JOB_ID_NOT_EMPTY)
        endpointColl = self.db.database['endpoint']
        deployColl =   self.db.database['deployment']
        # idpColl = self.db.database['idp_job_details']
        diplist =[]
        count =0
        endpointObj = endpointColl.find_one({"id": jobDetails.enpointId, "isDeleted": False}, {"_id":0})
        deployModels=endpointObj['deployedModels']
        for deploy in deployModels:
                    deploymentId=deploy['deploymentId']
                    diplist.append(deploymentId)
                    deployObj = deployColl.find_one({'id':deploymentId,'isDeleted':True,'status':DeploymentStatusEnum.Deleted},{"_id":0})
                    if deployObj != None:
                        count=count+1
                    
        if count==len(diplist):
            filter = {'_id': ObjectId(jobDetails.jobId.strip()), 'isDeleted': pydantic.parse_obj_as(bool, "false")}
            last_modified_at=datetime.utcnow()
            jobDetailsColl = self.db.database['idp_job_details']
            row=jobDetailsColl.find_one(filter)
            print(row)  
            if row is None:
                raise JobDetailsNotFoundError(1055,JOB_DETAILS_NOT_FOUND)
            respDict = jobDetails.__dict__
            newValues = {'$set': {'status': jobDetails.jobStatus.strip(), 'responseJson': respDict,
                'modifiedOn': last_modified_at, 'updatedBy': "jenkins"}}
            jobDetailsColl.update_one(filter, newValues)
            row=jobDetailsColl.find_one(filter)
            idpmodel=IdpJobDetailsModel(**row)
            if jobDetails.jobStatus.strip().lower() == "success":
                endpointfilter = {'id':jobDetails.enpointId, 'isDeleted': pydantic.parse_obj_as(bool, "false")}
                newValues = {'$set': {'status': 'Deleted', 'updatedBy': 'jenkins',
                            'modifiedOn': last_modified_at,'isDeleted': pydantic.parse_obj_as(bool, "true")}}  
                endpointColl.update_one(endpointfilter,newValues)   
                self.log.info('Exit updateDeleteDeploymentJobStatus')
        else:
                raise DeploymentNotDeletedError(1059,DEPLOYMENT_NOT_DELETED)
        return idpmodel
    
    # Method to push Data to ElasticSearch
    def pushDatatoES(self,esdata: ESBulkData):
        self.log.info('pushDatatoES')
        res={}

        es_host = os.getenv("ES_HOST")
        es_port = os.getenv("ES_PORT")
        es_scheme = os.getenv("ES_SCHEME")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")

        es_indexName= esdata.esindex
        data= esdata.data

        if data !=None and len(data)==0:
            res["status"]="Failure"
            res["message"]="ES Bulk Data is empty."
        elif  data !=None and len(data)>0:
            try:
               _elasticsearch = Elasticsearch([{'host': str(es_host), 'port': int(es_port), 'scheme': str(es_scheme)}], basic_auth = (str(es_username), str(es_password)),verify_certs=False)

               bulk_data=[]

               for item in data:
                   item["@timestamp"]=datetime.utcnow()
                   bulk_data.append({"_index": es_indexName,"_source": item})

               self.log.info("ES Data ********")
               self.log.info(bulk_data)
               self.log.info("ES Data ********")
               if len(bulk_data)>0:
                    uploadData = bulk(_elasticsearch,bulk_data)
               else:
                   self.log.info("empty data")

               res["status"]="Success"
               res["message"]="Data pushed into ES successfully"
            except(Exception) as e:
                self.log.error(e)
                res["status"]="Failure"
                res["message"]="Some error occurred while pushing data ito ES"
                return res
        return res

    # Method to search in elasticsearch index with modality
    def searchDataES(self,modality:str,reqType:str, body:dict):
        self.log.info('searchDataES')
        start_time = time.time()
        date = datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())
        date_time_stamp = datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
        res={}

        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")

        try:
            modality=modality.upper()

            if modality == "CODE":
                indexName = os.getenv("CODE_ES_INDEX")
            elif modality== "TEXT":
                indexName = os.getenv("TEXT_ES_INDEX")
            else:
                indexName = os.getenv("EMBEDDING_ES_INDEX")

            print("***indexName***",indexName)
            esUrl=os.getenv("ES_SCHEME")+"://"+os.getenv("ES_HOST")+":"+os.getenv("ES_PORT")+"/{index}"
            url= esUrl.replace(INDEX_PLACEHOLDER,indexName) + "/"+ reqType
            body = jsonable_encoder(body)
            response = requests.get(url, auth = HTTPBasicAuth(str(es_username), str(es_password)),verify=False, json=body)
            res['status']="Success"
            res['data']=response.json()
        except(Exception) as e:
                self.log.error(e)
                res["status"]="Failure"
                res["message"]="Some error occurred while pushing data ito ES"
                return res
        return res