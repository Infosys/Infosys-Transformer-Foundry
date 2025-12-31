# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import requests
from common.ainauto_logger_factory import AinautoLoggerFactory

logger = AinautoLoggerFactory().get_logger()

JENKINS_AUTH_URL = os.environ.get('JENKINS_AUTH_URL')
JENKINS_MULTI_STEP_PIPELINE_JOB_URL = os.environ.get('JENKINS_MULTI_STEP_PIPELINE_JOB_URL')
JENKINS_CREATE_PIPELINE_MULTI_STEP= os.environ.get('JENKINS_CREATE_PIPELINE_MULTI_STEP')
JENKINS_DEPLOY_ENV = os.environ.get('JENKINS_DEPLOY_ENV')
JENKINS_API_TOKEN = os.environ.get('JENKINS_API_TOKEN')
JENKINS_USER = os.environ.get('JENKINS_USER')

class JenkinHandler():
    def __init__(self, job_id):
        self.__config = {"JENKINS_AUTH_URL": JENKINS_AUTH_URL,
                         "JENKINS_MULTI_STEP_PIPELINE_JOB_URL": JENKINS_MULTI_STEP_PIPELINE_JOB_URL,
                         "JENKINS_CREATE_PIPELINE_MULTI_STEP" : JENKINS_CREATE_PIPELINE_MULTI_STEP,
                         "JENKINS_API_TOKEN": JENKINS_API_TOKEN,
                         "JENKINS_USER": JENKINS_USER,
                         "JENKINS_DEPLOY_ENV": JENKINS_DEPLOY_ENV}
        logger.info("JENKINS_MULTI_STEP_PIPELINE_JOB_URL = ",JENKINS_MULTI_STEP_PIPELINE_JOB_URL)
        self.__job_id = job_id

    # Create job parameters
    def _createJobParams(self) -> dict:
        jobParams = {'token': self.__config['JENKINS_API_TOKEN'],
                     'jobId': self.__job_id, 'deployEnv': self.__config['JENKINS_DEPLOY_ENV']}

        return jobParams

    # Get Jenkins crumb data
    def _getJenkinsCrumbData(self):
        jobHeaders = {'content-type': 'application/json'}
        jobAuth = (self.__config['JENKINS_USER'], self.__config['JENKINS_API_TOKEN'])
        crumb_data = requests.get(self.__config['JENKINS_AUTH_URL'], auth=jobAuth, headers=jobHeaders)
        return crumb_data

    # Invoke Jenkins pipeline
    def invokeJenkinsPipeline(self):
        statusCode = ''
        jobAuth = (self.__config['JENKINS_USER'], self.__config['JENKINS_API_TOKEN'])
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json', 'Jenkins-Crumb': crumbData.json()['crumb']}

            jobParams = self._createJobParams()
            try:
                data = requests.get(self.__config['JENKINS_MULTI_STEP_PIPELINE_JOB_URL'], auth=jobAuth,
                                    params=jobParams, headers=jobHeaders, timeout=30)
                statusCode = str(data.status_code)
            except requests.exceptions.Timeout:
                print('Jenkin call request timed out')
            if statusCode == "201":
                print("Jenkins job is triggered")
            else:
                print("Either Failed to trigger the Jenkins job or Timeout")
        return statusCode

    # Invoke Jenkins multi pipeline
    def invokeJenkinsMultiPipeline(self):
        statusCode = ''
        jobAuth = (self.__config['JENKINS_USER'], self.__config['JENKINS_API_TOKEN'])
        crumbData = self._getJenkinsCrumbData()
        if str(crumbData.status_code) == "200":
            jobHeaders = {'content-type': 'application/json', 'Jenkins-Crumb': crumbData.json()['crumb']}

            jobParams = self._createJobParams()
            try:
                data = requests.get(self.__config['JENKINS_CREATE_PIPELINE_MULTI_STEP'], auth=jobAuth,
                                    params=jobParams, headers=jobHeaders, timeout=30)
                statusCode = str(data.status_code)
            except requests.exceptions.Timeout:
                print('Jenkin call request timed out')
            if statusCode == "201":
                print("Jenkins job is triggered")
            else:
                print("Either Failed to trigger the Jenkins job or Timeout")
        return statusCode