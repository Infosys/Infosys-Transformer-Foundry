# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import requests
import sys
import time

jobAuth = ('${JENKINS_USERNAME}','${JENKINS_API_TOKEN}')
jobHeaders = {'content-type': 'application/json'}

def _getJenkinsCrumbData():
        
        crumb_data = requests.get("http://${JENKINS_HOST}:${JENKINS_PORT}/crumbIssuer/api/json", auth=jobAuth, headers=jobHeaders)
        return crumb_data,crumb_data.status_code

def endpointFile(endpointDetFetchUrl):
    resp = requests.get(endpointDetFetchUrl).json()
    crumbData,statusCode = _getJenkinsCrumbData()
    print(resp)

    if str(statusCode) == "200":
            jobHeaders = {'content-type': 'application/json','Jenkins-Crumb': crumbData.json()['crumb']}
            jenkinsParam = {}
            depjobidlist=resp['data']['inputData']['depjobidlist']
            modelNameList=resp['data']['inputData']['modelNameList']
            modelVersionList=resp['data']['inputData']['modelVersionList']
            depFrameworkList=resp['data']['inputData']['depFrameworkList']
            projectIdList=resp['data']['inputData']['projectIdList']
          
            for i in range(0,len(depFrameworkList)):
                jenkinsParam['jobId'] = depjobidlist[i]
                jenkinsParam['deployEnv'] = 'PRODUCTION'
                jenkinsParam['projectId'] = projectIdList[i]
                jenkinsParam['modelName'] = modelNameList[i]
                jenkinsParam['modelVersion'] = modelVersionList[i]
                jenkinsParam['deployFramework']=depFrameworkList[i]
                print(jenkinsParam)

                jobAuth = ('${JENKINS_USERNAME}','${JENKINS_API_TOKEN}')
                jobHeaders = {'content-type': 'application/json'}
                data = requests.post("http://${JENKINS_HOST}:${JENKINS_PORT}/job/${JENKINS_JOB_NAME}/buildWithParameters", auth=jobAuth, params=jenkinsParam, headers=jobHeaders)
                statusCode = str(data.status_code)
                print(data)

    time.sleep(10)
  
    succ ={
        "enpointId": resp['data']['endpointId'],
        "jobId": resp['data']['jobId'] ,
        "jobStatus":'SUCCESS',
        "message" : 'Endpoint is deleted successfully',
        "errorMsg" :''
    }
    
    fail={
        "enpointId": resp['data']['endpointId'],
        "jobId": resp['data']['jobId'],
        "jobStatus":'FAILURE',
        "message" : '',
        "errorMsg" : 'Endpoint not deleted'
    }
    
    for count in range(4):
        result = requests.post("http://${UTILITY_SERVICE_HOST}:${UTILITY_SERVICE_PORT}/api/v1/utilities/update/deleteEndpointjobstatus",json=succ).json()
        if result['status'] == "SUCCESS":
                break
    
        time.sleep(5)
        continue
    if result['status'] == "FAILURE":
        requests.post("http://${UTILITY_SERVICE_HOST}:${UTILITY_SERVICE_PORT}/api/v1/utilities/update/deleteEndpointjobstatus",json=fail).json()   
          
      
if __name__=="__main__":
    endpointDetFetchUrl = sys.argv[1]
    endpointFile(endpointDetFetchUrl)