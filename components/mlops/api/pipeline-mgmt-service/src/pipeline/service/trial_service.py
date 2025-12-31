# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: service.py
description: handles the CRUD operation for  Usecase module

"""
from bson import ObjectId
from dotenv import dotenv_values, find_dotenv
import json
from fastapi import Request, status
import random
import re
import requests
import time
import pydantic
import uuid
from fastapi import HTTPException
from aicloudlibs.exceptions.global_exception import MLOpsException
from aicloudlibs.schemas.pipeline_mappers import *
from aicloudlibs.constants.util_constants import EXECUTE_PIPELINE, WORKSPACEADMIN, VIEW
from aicloudlibs.validations.global_validations import GlobalValidations as globalValidations
from aicloudlibs.utils.apiUtils import convertGBtoGIB
from aicloudlibs.exceptions.global_exception import ForbiddenException, NotFoundException, InternalServerException, MLOpsException
from pipeline.exception.exception import *
from pipeline.exception.exception import *
from pipeline.service.pipeline_service import BaseService
import pipeline.constants.local_constants as local_errors
import math

dotenv_path = find_dotenv()
config = dotenv_values(dotenv_path)

class PipelineTrialService(BaseService):

    def __init__(self, app):
        super(PipelineTrialService, self).__init__(app)
        self.metric_output = {"name": None, "value": None}

    def _convert_float_int(self, number, d_type):
        try:
            return d_type(number)
        except ValueError:
            return False

    def _validate_run_arg_data_type(self, runArgument, pipeline_job_obj):
        pipeline_job_argument = [p for p in pipeline_job_obj if p['name'] == runArgument['name']]
        pipeline_data_type = pipeline_job_argument[0]['dataType']

        if pipeline_data_type == 'string' and isinstance(runArgument['argValue'], str) and runArgument[
            'argValue'].lower() in {'true', 'false'}:
            raise InvalidValueError(local_errors.ErrorCode.INVALID_RUNARG_VALUE_ERROR)
        if pipeline_data_type == 'bool' and not (str(runArgument['argValue']).lower() in ('true', 'false')):
            raise InvalidValueError(local_errors.ErrorCode.INVALID_RUNARG_VALUE_ERROR)
        if pipeline_data_type == 'int' and not (self._convert_float_int(runArgument['argValue'], int)):
            raise InvalidValueError(local_errors.ErrorCode.INVALID_RUNARG_VALUE_ERROR)
        if pipeline_data_type == 'float' and not (self._convert_float_int(runArgument['argValue'], float)):
            raise InvalidValueError(local_errors.ErrorCode.INVALID_RUNARG_VALUE_ERROR)

    # trigger a trail based on pipelineId and userId
    def trial_pipeline(self, payload: PipelineTrial, userId) -> TrialResponseData:

        payload = jsonable_encoder(payload)

        if len(payload['projectId']) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        if len(payload['pipelineId']) != 32:
            raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

        projectObj = self.app.database["project"].find_one({"id": payload['projectId'], "isDeleted": pydantic.parse_obj_as(bool, "false")})

        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        project_id = projectObj['id']
        tenant_id = projectObj['tenantId']
        resource_config = payload['resourceConfig']

        has_access = globalValidations.hasAccess(userId, project_id, EXECUTE_PIPELINE) or globalValidations.hasAccess(userId, project_id, WORKSPACEADMIN)

        if has_access:
            check_pipeline_exists = self.app.database["pipeline"].find(
                {"id": payload['pipelineId'], 'projectId': payload['projectId'],
                 "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()

            if check_pipeline_exists == 0:
                raise InvalidValueError(local_errors.ErrorCode.PIPELINE_NOT_FOUND_ERROR)

            randomJobId = ''.join(random.choices('0123456789abcdef', k=int(config['RANDOM_JOB_ID_CHARACTERS'])))
            payload['jobId'] = randomJobId

            pipeline_object = self.app.database["pipeline"].find_one(
                {"id": payload['pipelineId'], 'projectId': payload['projectId'],
                 "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0})

            pipelineObj = jsonable_encoder(pipeline_object)

            arg_mismatch = False
            trial_runArg_list = []
            name_ArgValue_dict = {}

            pipeline_JobArgs = [n['name'] for n in pipelineObj['jobArguments']]
            pipelineJob_dataType = [n['dataType'] for n in pipelineObj['jobArguments']]
            pipelineDefault_value = [n['defaultVal'] for n in pipelineObj['jobArguments']]
            pipeline_job_obj = pipelineObj['jobArguments']

            for runArg in payload['runArguments']:
                if runArg['name'] not in pipeline_JobArgs:
                    arg_mismatch = True
                    break
               
                trial_runArg_list.append(runArg)
                name_ArgValue_dict[runArg['name']] = runArg['argValue']

                self._validate_run_arg_data_type(runArg, pipeline_job_obj)

            runargu = list(name_ArgValue_dict.keys())    
            i = 0
            for step in pipeline_JobArgs:
                found = False
                for stepArg in runargu:  
                    if step == stepArg:
                        found = True
                        break
                    else:
                        continue
                if found:
                    continue
                else:
                    if pipelineDefault_value[i] != '':
                        payload['runArguments'].append({'name':step,'argValue':pipelineDefault_value[i]})
                        #i += 1
                    else:
                        arg_mismatch = True
                        break
                i += 1
            
            if arg_mismatch:
                raise InvalidValueError(local_errors.ErrorCode.RUNARG_MISMATCH_ERROR)

            for i in payload['resourceConfig']['computes']:
                i['type'] = i['type'].upper()
                if not (i['type'] == "CPU" or i['type'] == "GPU"):
                    raise InvalidValueError(local_errors.ErrorCode.COMPUTE_TYPE_VALUE_ERROR)

                if i['minQty'] > i['maxQty']:
                    raise InvalidValueError(local_errors.ErrorCode.MINMAX_QTY_ERROR)

                if i['type'] == "CPU":
                    memoryTxt = i['memory']
                    if re.search(r'\d+', memoryTxt) is None:
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_ERROR)
                    else:
                        memoryValue = int(re.search(r'\d+', memoryTxt).group())
                        i['memory'] = str(memoryValue) + "GB"

                elif i['type'] == "GPU":

                    if i['minQty'] > i['maxQty']:
                        raise InvalidValueError(local_errors.ErrorCode.MINMAX_QTY_ERROR)

                    if int(i['maxQty']) > 20:
                        raise InvalidValueError(local_errors.ErrorCode.MAXQTY_VALUE_ERROR)

                    if int(i['minQty']) < 1:
                        raise InvalidValueError(local_errors.ErrorCode.MINQTY_VALUE_ERROR)

                    memoryTxt = i['memory']
                    if re.search(r'\d+', memoryTxt) is None:
                        raise InvalidValueError(local_errors.ErrorCode.INVALID_VALUE_ERROR)
                    else:
                        memoryValue = int(re.search(r'\d+', memoryTxt).group())
                        i['memory'] = str(memoryValue) + "GB"

            experimentConfigNameTxt = payload['experimentConfig']['name']

            if not bool(re.search('^[a-zA-Z0-9-]*$', experimentConfigNameTxt)):
                raise InvalidValueError(local_errors.ErrorCode.INVALID_EXPERIMENTNAME_ERROR)

            trial_object = self.app.database['trial']
            check_trial_exists = trial_object.find(
                {"name": payload['name'].strip(), "pipelineId": payload['pipelineId'].strip(),
                 "isDeleted": pydantic.parse_obj_as(bool, "false")}).count()

            if check_trial_exists != 0:
                raise TrialAlreadyExistsError(local_errors.ErrorCode.TRIAL_ALREADY_EXISTS_ERROR)

            payload['status'] = TrialStatusEnum.Initiated
            payload['createdOn'] = datetime.utcnow()
            payload['createdBy'] = userId
            payload['modifiedOn'] = None
            payload['updatedBy'] = None
            payload['isDeleted'] = False
            payload["id"] = str(uuid.uuid4().hex)

            # new currentResourceUsage_Addition
            globalValidations.updateResourceUsage(userId, project_id, resource_config, "allocate")

            trial_info = trial_object.insert_one(payload)

            created_trial = self.app.database['trial'].find_one({"_id": trial_info.inserted_id}, {"_id": 0})
            trial_id = created_trial['id']

            tenantId = projectObj['tenantId']
            tenantData = self.app.database["tenant"]
            tenantObj = tenantData.find_one({"id": tenantId, "isDeleted": pydantic.parse_obj_as(
            bool, "false")})
            tenantName = tenantObj['name']

            trialJobObj = {}
            trialJobObj['jobId'] = payload['jobId']
            trialJobObj['inputData'] = {}
            trialJobObj['inputData']['pipelineName'] = pipelineObj['name']
            trialJobObj['inputData']['pipelineVersion'] = pipelineObj['version']
            trialJobObj['inputData']['runId'] = str(trial_id)
            piplrunName = payload['name']
            trialJobObj['inputData']['runName'] = piplrunName
            trialJobObj['inputData']['projectId'] = payload['projectId']

            if (payload['experimentConfig'] is None or (payload['experimentConfig'] is not None and payload['experimentConfig']['name'] is '')):
                trialJobObj['inputData']['experimentName'] = "mms-experiment"
            else:
                trialJobObj['inputData']['experimentName'] = payload['experimentConfig']['name']

            trialJobObj['inputData']['pipelineId'] = payload['pipelineId']

            artificatStorageType = pipelineObj['steps'][0]['trainingStep']['inputArtifacts']['storageType']

            stepName = pipelineObj['steps'][0]['trainingStep']['name']
            containerImage = pipelineObj['steps'][0]['trainingStep']['container']['imageUri']
            metricDetails = pipelineObj['steps'][0]['trainingStep']['metricDetails']
            inputArtifacts = pipelineObj['steps'][0]['trainingStep']['inputArtifacts']
            if inputArtifacts is None:
                inputArtifacts = "NA"
            outputArtifacts = pipelineObj['steps'][0]['trainingStep']['outputArtifactBaseUri']
            if outputArtifacts is None:
                outputArtifacts = "NA"

            preTrainedMdl = pipelineObj['steps'][0]['trainingStep']['preTrainedModelDetails'] 
            trialJobObj['inputData']['storageType'] = artificatStorageType
            trialJobObj['inputData']['stepName'] = stepName
            trialJobObj['inputData']['containerImage'] = containerImage
            trialJobObj['inputData']['metricDetails'] = metricDetails
            trialJobObj['inputData']['inputArtifacts'] = inputArtifacts
            trialJobObj['inputData']['outputArtifacts'] = outputArtifacts
            #if preTrainedMdl is not None:
            trialJobObj['inputData']['preTrainedMdl'] = preTrainedMdl
        
            for s in range(0, len(payload['resourceConfig']['computes'])):
                if payload['resourceConfig']['computes'][s]['type'] == 'CPU':
                    memoryTxt = payload['resourceConfig']['computes'][s]['memory']
                    memoryTxt = [int(s) for s in re.findall(r'-?\d+\.?\d*', memoryTxt)][0]
                    memory_GIB_conversion = convertGBtoGIB(memoryTxt)
                    memory_GIB_conversion = str(memory_GIB_conversion) + "Gi"
                    payload['resourceConfig']['computes'][s]['memory'] = memory_GIB_conversion

            volumeSizeinGB_converted = convertGBtoGIB(payload['resourceConfig']['volumeSizeinGB'])
            volumeSizeinGB_converted = int(math.ceil(volumeSizeinGB_converted))
            payload['resourceConfig']['volumeSizeinGB'] = volumeSizeinGB_converted

            trialJobObj['inputData']['resourceConfig'] = payload['resourceConfig']
            trialJobObj['inputData']['runArguments'] = payload['runArguments']
            trialJobObj['inputData']['mainScriptFile'] = \
                pipelineObj['steps'][0]['trainingStep']['container']["command"][0]
            trialJobObj['inputData']['tenantName'] = tenantName
            statusCode = self._invokeJenkinsPipeline(payload, trialJobObj)
            if int(statusCode) == status.HTTP_201_CREATED:
                trialResp = self.app.database["trial"].find_one({"_id": trial_info.inserted_id})
                trialResp['_id'] = str(trial_id)
            else:
                raise JenkinsTriggerError(local_errors.ErrorCode.JENKINS_TRIGGER_ERROR)

            return TrialResponseData(**created_trial)
        else:
            raise ForbiddenException()

    # create job params for triggering jenkins pipeline
    def _createJobParams(self, body: dict, trialJobObj) -> dict:

        jobId = body['jobId']
        jobParams = {'token': config['JENKINS_API_TOKEN'], 'jobId': jobId, 'deployEnv': config['JENKINS_DEPLOY_ENV']}
        return jobParams

    # get the jenkins crumb data
    def _getJenkinsCrumbData(self):

        jobHeaders = {'content-type': 'application/json'}
        jobAuth = (config['JENKINS_USER'], config['JENKINS_API_TOKEN'])
        crumb_data = requests.get(config['JENKINS_AUTH_URL'], auth=jobAuth, headers=jobHeaders)
        return crumb_data

    # invoke jenkins pipeline
    def _invokeJenkinsPipeline(self, body, trialJobObj):

        jobAuth = (config['JENKINS_USER'], config['JENKINS_API_TOKEN'])

        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json', 'Jenkins-Crumb': crumbData.json()['crumb']}

            jobParams = self._createJobParams(body, trialJobObj)
            print(config['JENKINS_PIPELINE_JOB_URL'])
            print(jobParams)
            data = requests.get(config['JENKINS_PIPELINE_JOB_URL'], auth=jobAuth, params=jobParams, headers=jobHeaders)

            statusCode = str(data.status_code)

            if statusCode == "201":
                print("Jenkins job is triggered")
                self._insertIdpJobDetails(body, trialJobObj)
            else:
                print("Failed to trigger the Jenkins job")

        return statusCode

    # insert record in idp_job_details collection
    def _insertIdpJobDetails(self, body: dict, request_json: dict):

        idpLogColl = self.app.database['idp_job_details']
        jobId = body['jobId']

        jobName = "Run_Trial_Pipeline"
        body['updatedBy'] = None

        idpLogDict = {'_id': ObjectId(jobId), 'jobName': jobName, 'status': "InProgress", 'requestJson': request_json, 'responseJson': {}, 'createdOn': body['createdOn'], 'createdBy': body['createdBy'], 'modifiedOn': body['modifiedOn'], 'updatedBy': body['updatedBy'], 'isDeleted': False, 'id': str(uuid.uuid4().hex)}

        idpLogId = idpLogColl.insert_one(idpLogDict).inserted_id
        return idpLogId

    # set the run status to the trail table
    def set_run_status(self, runId, status) -> dict:
        '''
        Service to update status in Mongo DB 'Trail' table
        '''

        if (runId is None or runId == ""):
            raise RequiredFieldEmptyError(KUBEFLOW_JOB_ID_ERROR)
        if (status is None or status == ""):
            raise RequiredFieldEmptyError(JOB_STATUS_ERROR)
        kubeflow_query = {"kubeflowRunID": runId}
        update_query = {"status": status, "modifiedOn": datetime.utcnow(), "modifiedBy": 'Kubeflow'}
        trail_doc = self.app.database["trial"].find_one(kubeflow_query)
        if trail_doc:
            update_result = self.app.database["trial"].update_one(kubeflow_query, {'$set': update_query})
            updated_pipeline = self.app.database["trial"].find_one(kubeflow_query)
            updated_pipeline["_id"] = updated_pipeline["_id"].__str__()

            projectId = updated_pipeline["projectId"]
            userId = updated_pipeline["createdBy"]
            resource_config = updated_pipeline["resourceConfig"]
            globalValidations.updateResourceUsage(userId, projectId, resource_config, "deallocate")

            return updated_pipeline, 200
        return f"Run Id {runId} not found", 404

    # set metrics output to the trail table
    def set_metrics_output(self, runId: str, metrics: str) -> dict:
        '''
        Service to update status in Mongo DB 'Trail' table
        '''
        metrics = json.loads(metrics.replace("'", "\""))
        for k, v in metrics.items():
            name = k
            value = v
        if (runId is None or runId == ""):
            raise RequiredFieldEmptyError(KUBEFLOW_JOB_ID_ERROR)
        if (name is None or name == ""):
            raise RequiredFieldEmptyError(METRIC_NAME_ERROR)
        if (value is None or value == ""):
            raise RequiredFieldEmptyError(METRIC_VALUE_ERROR)
        kubeflow_query = {"kubeflowRunID": runId}
        update_query = {"metricOutput.name": name, "metricOutput.value": value, "modifiedOn": datetime.utcnow(), "modifiedBy": "Kubeflow"}
        trail_doc = self.app.database["trial"].find_one(kubeflow_query)
        if trail_doc:
            if 'metricOutput' not in trail_doc:
                update_metric_output = {"metricOutput": {}}
                self.app.database["trial"].update_one(kubeflow_query, {'$set': update_metric_output})
            update_result = self.app.database["trial"].update_one(kubeflow_query, {'$set': update_query})
            updated_pipeline = self.app.database["trial"].find_one(kubeflow_query)
            updated_pipeline["_id"] = updated_pipeline["_id"].__str__()
            return updated_pipeline, 200
        return f"Run Id {runId} not found", 404

    # get the trial details based on trialId and userId
    def get_trial_details(self, trialId: str, userId: str) -> GetTrialResponseData:

        if (trialId is None) or (trialId == ''):
            raise RequiredFieldEmptyError(local_errors.ErrorCode.TRIAL_ID_EMPTY_ERROR)

        trial_detail = self.app.database["trial"].find_one({"id": trialId, "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0})

        if trial_detail is None:
            raise InvalidValueError(local_errors.ErrorCode.TRIAL_DETAILS_NOT_FOUND_ERROR)

        projectId = trial_detail['projectId']

        projectObj = self.app.database["project"].find_one({"id": projectId, "isDeleted": pydantic.parse_obj_as(bool, "false")})

        if projectObj is None:
            raise InvalidValueError(local_errors.ErrorCode.PROJECT_NOT_FOUND_ERROR)

        project_id = projectObj['id']

        permissions_available = [EXECUTE_PIPELINE, WORKSPACEADMIN, VIEW]
        has_access = False

        for permission in permissions_available:
            has_access = globalValidations.hasAccess(userId, project_id, permission)
            if has_access:
                break

        if has_access:
            trial_detail['id'] = str(trialId)

            projectId = trial_detail["projectId"]
            resource_config = trial_detail["resourceConfig"]

            jobId = trial_detail['jobId']

            jobDetail = self.app.database["idp_job_details"].find_one({"_id": ObjectId(jobId), "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0})

            if jobDetail is not None:
                if len(jobDetail['responseJson']) > 0:
                    jobStatus = jobDetail['responseJson']['jobStatus']
                    if jobStatus.strip().lower() == "success":
                        trial_response={}
                        trial_response['trial']=trial_detail
                        return GetTrialResponseData(**trial_response)
                    elif jobStatus.strip().lower() == "failure":
                        errorMsg = jobDetail['responseJson']['errorMsg']
                        raise JenkinsJobError(errorMsg)
                else:
                    trial_response={}
                    trial_response['trial']=trial_detail
                    return GetTrialResponseData(**trial_response)
            else:
                trial_response={}
                trial_response['trial']=trial_detail
                return GetTrialResponseData(**trial_response)
        else:
            raise ForbiddenException()

    # terminate the trail based on trailId and userId
    def terminate_pipeline(self, trailId, userId):
        
        trialObj = self.app.database["trial"].find_one({"id": trailId, "isDeleted": pydantic.parse_obj_as(bool, "false")}, {'_id': 0})
        if trialObj is None:
            raise InvalidValueError(local_errors.ErrorCode.TRIAL_DETAILS_NOT_FOUND_ERROR)

        projectId = trialObj['projectId']
        kubeflowRunID = trialObj['kubeflowRunID']
        permissions_available = [EXECUTE_PIPELINE, WORKSPACEADMIN]
        has_access = False
        for permission in permissions_available:
            has_access = globalValidations.hasAccess(userId, projectId, permission)
            if has_access:
                break
            else:
                raise ForbiddenException()
    
        jobHeaders = {'content-type': 'application/json'}
        authTokenRequest = requests.get(config['GET_AUTHSESSION_URL'], headers=jobHeaders)
        authTokenText = authTokenRequest.text

        jobHeaders['cookie'] = authTokenText.replace("\"","")
        kubeflowUrl = config['KUBEFLOW_TERMINATE_URL'].format(kubeflowRunID)
        data = requests.post(kubeflowUrl, headers=jobHeaders)

        if data.status_code == 200:
            kubeflowStatusUrl = config['KUBEFLOW_STATUS_URL'].format(kubeflowRunID)
            count = 0
            while (count < 3):
                statusUrlData = requests.get(kubeflowStatusUrl, headers=jobHeaders)
                statusUrlData = statusUrlData.json()
                if(statusUrlData['run']['status'] == TrialStatusEnum.Failed or statusUrlData['run']['status'] == "Terminating"):
                    break
                time.sleep(config['RETRY_INTERVAL'])
                count = count + 1 
            if(statusUrlData['run']['status'] != TrialStatusEnum.Failed and statusUrlData['run']['status'] != "Terminating"):
                raise InvalidValueError(local_errors.ErrorCode.ERROR_OCCURED)

            pipeline_trail, code = self.set_run_status(kubeflowRunID, TrialStatusEnum.Failed)
            if code == 200:
                response = trailId+" terminated successfully"
        else:
            raise InternalServerException()

        return response