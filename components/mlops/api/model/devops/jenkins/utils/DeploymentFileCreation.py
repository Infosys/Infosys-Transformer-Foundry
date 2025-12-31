# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import json
import sys
import requests
import glob
import os

VALUE_SEPARATOR = "-"
AICLOUD_MODEL_BASE_PATH="/mnt/models"
AICLOUD_BASE_PATH="/base/models"
TRITON_MDL_VERSION = "v2"
MINIO_URL = "${MINIO_URL}"
NUTANIX_URL = "${NUTANIX_URL}"

## TEMPLATES FOR CUSTOM MODEL DEPLOYMENT
CUSTOM_DESTRULE_TEMPLATE = "/KNS_DESTRULE_TEMPLATE_PROD.json"
CUSTOM_DEPLOY_NUTANIX_TEMPLATE = "/KNS_S3_NUTANIX_Template_PROD.json"
CUSTOM_DEPLOY_MINIO_TEMPLATE = "/KNS_S3_Template_PROD.json"
CUSTOM_SERVICE_TEMPLATE = "/KNS_SERVICE_TEMPLATE_PROD.json"
CUSTOM_SERVRULEBIND_TEMPLATE = "/KNS_SERVRULEBIND_TEMPLATE_PROD.json"
CUSTOM_SERVRULE_TEMPLATE = "/KNS_SERVRULE_TEMPLATE_PROD.json"
CUSTOM_DEPLOY_TEMPLATE = "/KNS_Template_PROD.json"
CUSTOM_VS_TEMPLATE = "/KNS_VS_TEMPLATE_PROD.json"
DJL_DEPLOY_TEMPLATE = "/DJL_S3_NUTANIX_Template_PROD.json"
DJL_VS_TEMPLATE = "/DJL_VS_TEMPLATE_PROD.json"

## TEMPLATES FOR TRITON MODEL DEPLOYMENT WITHOUT PYTHON BACKEND ###
TRITON_NT_DEPLOYMENT_TEMPLATE = "/TRITON_NT_DEPLOYMENT_TEMPLATE_PROD.json"
TRITON_NT_SERVICE_TEMPLATE = "/TRITON_NT_SERVICE_TEMPLATE_PROD.json"
TRITON_NT_VS_TEMPLATE_PROD = "/TRITON_NT_VS_TEMPLATE_PROD.json"
CUSTOM_DEPLOY_NUTANIX_TEMPLATE = "/KNS_S3_NUTANIX_Template_PROD.json"
TRITON_NT_PYTHON_DEPLOYMENT_TEMPLATE = "/TRITON_NT_PYTHON_DEPLOYMENT_TEMPLATE_PROD.json"

class DeploymentFileCreation(object):

    def createDeploymentFiles(self, deplFilesFolder, dataFetchUrl, namespace:str, servingFramework:str) :
        
        resp = requests.get(dataFetchUrl).json()
        print (resp)
        inputData = resp['data']['inputData']
        projectId = inputData.get('projectId')
        endpointId = inputData.get('endpointId')
        tenantName = inputData.get('tenantName')
        print(endpointId)
        jobId = inputData.get('jobId')
        userName = inputData.get('userName')
        modelName = inputData.get('modelName')
        containerImage = inputData.get('containerImage')
        modelVersion = str(inputData.get('modelVersion'))
        modelS3RepoPath = inputData.get('modelS3RepoPath')
        inputMode = inputData.get('inputMode')
        healthProbeUri = inputData.get('healthProbeUri')
        ports = inputData.get('ports') if inputData.get('ports') is not None else []
        envVariables = inputData.get('envVariables') if inputData.get('envVariables') is not None else []
        labels = inputData.get('labels') if inputData.get('labels') is not None else []
        commands = inputData.get('command') if inputData.get('command') is not None else []
        args = inputData.get('args') if inputData.get('args') is not None else []
        tritonLogLevel = inputData.get('tritonLogLevel')

        inferenceSpec = inputData.get('inferenceSpec')
        minReplicaCount = inferenceSpec.get('minReplicaCount')
        maxReplicaCount = inferenceSpec.get('maxReplicaCount')
        containerResourceConfig = inferenceSpec.get('containerResourceConfig')
        modelSpecs = inferenceSpec.get('modelSpec') if inferenceSpec.get('modelSpec') is not None else []
        
        computes = containerResourceConfig.get('computes')
        volumeSizeinGB = containerResourceConfig.get('volumeSizeinGB')
        
        model_s3_path:str = modelS3RepoPath
        if(model_s3_path != "") :
            if(model_s3_path.startswith(MINIO_URL)) :
                model_s3_path = model_s3_path.replace(MINIO_URL, "s3://")
            elif(model_s3_path.startswith(NUTANIX_URL)) :
                model_s3_path = model_s3_path.replace(NUTANIX_URL, "s3://")
        
        contextUri = inputData.get('contextUri')
        endpointVersion = inputData.get('endpointVersion')
        urlCustomPart = '/models/' + modelName + '/versions/' + modelVersion
        
        deploymentJson = None
        deployName = modelName+VALUE_SEPARATOR+modelVersion+VALUE_SEPARATOR+projectId
        destServiceName = deployName + '.' + namespace + '.svc.cluster.local'
        if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
            s3Args = AICLOUD_MODEL_BASE_PATH + '/' + modelName + '/' + modelVersion
        else :
            s3Args = AICLOUD_MODEL_BASE_PATH + '/' + modelName
            s3ArgsBase = AICLOUD_BASE_PATH + '/' + modelName
        vsExposedPort = ''

        jsonFilePath = ''
        if ("custom"==servingFramework.lower() ) :
            if ("INFY_AICLD_MINIO" == inputMode) : 
                jsonFilePath = deplFilesFolder + CUSTOM_DEPLOY_MINIO_TEMPLATE
            if ("INFY_AICLD_NUTANIX" == inputMode): 
                jsonFilePath = deplFilesFolder + CUSTOM_DEPLOY_NUTANIX_TEMPLATE  
                print(jsonFilePath) 
                print("In Nutanix Template")
        elif ("triton"==servingFramework.lower()) :
            if ("INFY_AICLD_NUTANIX" == inputMode) : 
                jsonFilePath = deplFilesFolder + TRITON_NT_DEPLOYMENT_TEMPLATE
                print("template without python")
        elif ("djl"==servingFramework.lower()) :
            if ("INFY_AICLD_NUTANIX" == inputMode) : 
                jsonFilePath = deplFilesFolder + DJL_DEPLOY_TEMPLATE
                print(jsonFilePath)
                print("DJL")
        
        for modelSpec in modelSpecs:
            tritonServingConfig = modelSpec.get('tritonServingConfig')
            if tritonServingConfig is not None and tritonServingConfig.get('dependencyFileRepo') is not None:
                dependencyFileRepo = tritonServingConfig.get('dependencyFileRepo')
                model_s3_repo_path = dependencyFileRepo.get('uri')
                if ("INFY_AICLD_NUTANIX" == inputMode) : 
                    jsonFilePath = deplFilesFolder + TRITON_NT_PYTHON_DEPLOYMENT_TEMPLATE
                    print("template with python")
                    break
                    
        with open(jsonFilePath, 'r') as fp:
            deploymentJson = json.load(fp)
        if deploymentJson is not None :
            
            deploymentJson['metadata']['name'] = deployName
            deployLabels = deploymentJson['metadata']['labels']
            for label in labels :
                deployLabels[label['name']] = label['value']
            deployLabels['app'] = deployName
            deployLabels['endpointId'] = endpointId
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                deployLabels['version'] = modelVersion
                deployLabels['project-id'] = projectId
                deployLabels['user'] = userName
            deploymentJson['metadata']['labels'] = deployLabels
            
            deploymentJson['spec']['replicas'] = minReplicaCount
            deploymentJson['spec']['selector']['matchLabels']['app'] = deployName
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                deploymentJson['spec']['selector']['matchLabels']['version'] = modelVersion
            deploymentJson['spec']['template']['metadata']['labels']['app'] = deployName
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                deploymentJson['spec']['template']['metadata']['labels']['version'] = modelVersion

            #Logic added for Haystack Pipeline Deployments
            if "custom"==servingFramework.lower() or "djl"==servingFramework.lower() :
                for envVar in envVariables :
                    if envVar['name']=='HAYSTACK_BASE_PATH' :
                        s3Args = envVar['value']
                        break
                        
            initContainerArr = deploymentJson['spec']['template']['spec']['initContainers']
            if "triton"==servingFramework.lower() and tritonServingConfig is not None and tritonServingConfig.get('dependencyFileRepo') is not None :
                print("-----Inside triton with python initCont-----")
                for idx,initCont in enumerate(initContainerArr) :
                    if idx == 0:
                        initCont['args'].append(model_s3_path)
                        initCont['args'].append(s3ArgsBase)
                        if "INFY_AICLD_NUTANIX" == inputMode:
                            initCont['volumeMounts'][1]['mountPath'] = s3ArgsBase
                    else :
                        initCont['args'].append(model_s3_repo_path)
                        initCont['args'].append(s3Args)
                        if "INFY_AICLD_NUTANIX" == inputMode:
                            initCont['volumeMounts'][1]['mountPath'] = s3Args
                    
                deploymentJson['spec']['template']['spec']['initContainers'] = initContainerArr
            else :
                for idx,initCont in enumerate(initContainerArr) :
                    initCont['args'].append(model_s3_path)
                    initCont['args'].append(s3Args)
                    if "custom"==servingFramework.lower() or "djl"==servingFramework.lower():
                        initCont['volumeMounts'][0]['mountPath'] = s3Args
                    if ("triton"==servingFramework.lower() and "INFY_AICLD_NUTANIX" == inputMode) :
                        initCont['volumeMounts'][1]['mountPath'] = s3Args
                deploymentJson['spec']['template']['spec']['initContainers'] = initContainerArr
            
            firstContainer = deploymentJson['spec']['template']['spec']['containers'][0]
            firstContainer['image'] = containerImage
            firstContainer['name'] = deployName
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                firstContainer['volumeMounts'][0]['mountPath'] = s3Args
            elif ("triton"==servingFramework.lower() and "INFY_AICLD_NUTANIX" == inputMode and tritonServingConfig is not None and tritonServingConfig.get('dependencyFileRepo') is not None) :
                firstContainer['volumeMounts'][2]['mountPath'] = s3ArgsBase
                firstContainer['volumeMounts'][3]['mountPath'] = s3Args
            elif ("triton"==servingFramework.lower() and "INFY_AICLD_NUTANIX" == inputMode) :
                firstContainer['volumeMounts'][1]['mountPath'] = s3Args
            
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower() ) :
                firstContainer['env'][0]['name'] = 'AI_CLD_MDL_PATH'
                firstContainer['env'][0]['value'] = s3Args
                if "djl"==servingFramework.lower() and not tenantName == "llmcode-test":
                    firstContainer['env'][1]['name'] = 'SERVING_OPTS'
                    firstContainer['env'][1]['value'] = "-Dai.djl.logging.level=debug"
                    firstContainer['env'][2]['name'] = "SERVING_LOAD_MODELS"
                    firstContainer['env'][2]['value'] = "["+modelName+"-"+modelVersion+"]="+s3Args
                if "djl"==servingFramework.lower() and  tenantName == "llmcode-test":
                    firstContainer['env'][1]['name'] = 'SERVING_OPTS'
                    firstContainer['env'][1]['value'] = "-Dai.djl.logging.level=debug"
                    firstContainer['env'].pop(2)
                for envVar in envVariables :
                    pair = {'name':envVar['name'], 'value':envVar['value']}
                    firstContainer['env'].append(pair)
                for port in ports :
                    portName = port['name']
                    portNumber = int(port['value'])
                    if portName.lower()=='http' or portName.lower()=='containerport' :
                        pair = { 'containerPort': portNumber }
                        vsExposedPort = portNumber
                    else :
                        pair = {portName: port['value']}
                    firstContainer['ports'].append(pair)
                for command in commands :
                    firstContainer['command'].append(command)
                for arg in args :
                    firstContainer['args'].append(arg)
            
            elif ("triton"==servingFramework.lower()) :
                if not ports:
                    portJson = {"containerPort": 8000, "name": "http-triton"},{"containerPort": 8001, "name": "grpc-triton"},{"containerPort": 8002, "name": "metrics-triton"}
                    firstContainer['ports'].append(portJson)
                    vsExposedPort = 8000
                else :
                    enteredPorts = []
                    for port in ports :
                        portName = port['name']
                        portNumber = int(port['value'])
                        if(portName.lower() =='http' or portName.lower() =='http-triton'):
                            portJson = {"containerPort": portNumber, "name": "http-triton"}
                            firstContainer['ports'].append(portJson)
                            enteredPorts.append('http-triton')
                            vsExposedPort = portNumber
                        elif(portName.lower() =='grpc' or portName.lower() =='grpc-triton'):
                            portJson = {"containerPort": portNumber, "name": "grpc-triton"}
                            firstContainer['ports'].append(portJson)
                            enteredPorts.append('grpc-triton')
                        elif(portName.lower() =='metrics' or portName.lower() =='metrics-triton'):
                            portJson = {"containerPort": portNumber, "name": "metrics-triton"}
                            firstContainer['ports'].append(portJson)
                            enteredPorts.append('metrics-triton')
                        else :
                            portJson = {"containerPort": portNumber, "name": portName}
                            firstContainer['ports'].append(portJson)
                    if 'http-triton' not in enteredPorts :
                        portJson = {"containerPort": 8000, "name": 'http-triton'}
                        firstContainer['ports'].append(portJson)
                        vsExposedPort = 8000
                    if 'grpc-triton' not in enteredPorts :
                        portJson = {"containerPort": 8001, "name": 'grpc-triton'}
                        firstContainer['ports'].append(portJson)
                    if 'metrics-triton' not in enteredPorts :
                        portJson = {"containerPort": 8002, "name": 'metrics-triton'}
                        firstContainer['ports'].append(portJson)


                command = ""
                cmdTritonWithoutPython = "tritonserver --model-store={args} --allow-gpu-metrics=false --strict-model-config=false --log-info={info} --log-warning={warn} --log-error={error}"
                cmdTritonWithPython = "chmod -R 777 {modelBasePath}; cp /s3util/install_dependancy.sh {modelBasePath}/install_dependancy.sh; chmod 777 {modelBasePath}/install_dependancy.sh; cd {modelBasePath}; ./install_dependancy.sh; tritonserver --model-store={modelRepoPath} --allow-gpu-metrics=false --strict-model-config=false --log-info={info} --log-warning={warn} --log-error={error}"
                if ("triton"==servingFramework.lower() and tritonServingConfig is None):
                    print("-----Inside triton without python cmd-----")
                    if tritonLogLevel.lower() == "error":
                        command = cmdTritonWithoutPython.format(args=s3Args, info=0, warn=0, error=1)
                    if tritonLogLevel.lower() == "info":
                        command = cmdTritonWithoutPython.format(args=s3Args, info=1, warn=0, error=1)
                    if tritonLogLevel.lower() == "warning":
                        command = cmdTritonWithoutPython.format(args=s3Args, info=1, warn=1, error=1)
                    firstContainer['command'].append(command)
                ### WITH PYTHON TRITON ###
                elif ("triton"==servingFramework.lower() and tritonServingConfig is not None):
                    print("-----Inside triton with python cmd-----")
                    if tritonLogLevel.lower() == "error":
                        command = cmdTritonWithPython.format(modelBasePath=s3ArgsBase, modelRepoPath=s3Args, info=0, warn=0, error=1)
                    if tritonLogLevel.lower() == "info":
                        command = cmdTritonWithPython.format(modelBasePath=s3ArgsBase, modelRepoPath=s3Args, info=1, warn=0, error=1)
                    if tritonLogLevel.lower() == "warning":
                        command = cmdTritonWithPython.format(modelBasePath=s3ArgsBase, modelRepoPath=s3Args, info=1, warn=1, error=1)
                    firstContainer['command'].append(command)
                

            if (healthProbeUri is not None and healthProbeUri!='') :
                firstContainer['livenessProbe']['httpGet']['path'] = healthProbeUri
                firstContainer['livenessProbe']['httpGet']['port'] = vsExposedPort
                firstContainer['readinessProbe']['httpGet']['path'] = healthProbeUri
                firstContainer['readinessProbe']['httpGet']['port'] = vsExposedPort
            else :
                firstContainer.pop('livenessProbe')
                firstContainer.pop('readinessProbe')

            resrequests = {}
            limits = {}
            for compute in computes :
                type = compute['type']
                maxQty = compute['maxQty']
                minQty = compute['minQty']
                memory = compute['memory']
                if type.lower()=='cpu' :
                    resrequests['cpu'] = minQty
                    if 'gb' in memory.lower() :
                        newMem = memory.lower().replace('gb','')
                        newMem = float(newMem) * 0.93
                        newMem = str(newMem)+'Gi'
                    elif 'gi' in memory.lower() :
                        newMem = memory
                    resrequests['memory'] = newMem
                    limits['cpu'] = maxQty
                elif type.lower()=='gpu' :
                    if memory.lower() =='20gb':
                        resrequests['nvidia.com/mig-3g.20gb'] = minQty
                        limits['nvidia.com/mig-3g.20gb'] = maxQty
                    elif memory.lower()=='40gb':
                        resrequests['nvidia.com/mig-7g.40gb'] = minQty
                        limits['nvidia.com/mig-7g.40gb'] = maxQty
                    elif memory.lower()=='80gb':
                        resrequests['nvidia.com/gpu'] = minQty
                        limits['nvidia.com/gpu'] = maxQty

            firstContainer['resources'] = {'requests': resrequests, 'limits': limits}

            deploymentJson['spec']['template']['spec']['containers'][0] = firstContainer
        
        ### Service File Creation ###
        serviceJson = None
        if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
            jsonFilePath = deplFilesFolder + CUSTOM_SERVICE_TEMPLATE
        elif ("triton"==servingFramework.lower()) :
            if ("INFY_AICLD_NUTANIX" == inputMode) : 
                jsonFilePath = deplFilesFolder + TRITON_NT_SERVICE_TEMPLATE

        with open(jsonFilePath, 'r') as fp:
            serviceJson = json.load(fp)
        if serviceJson is not None :
            serviceJson['metadata']['name'] = deployName
            serviceLabels = serviceJson['metadata']['labels']
            for label in labels :
                serviceLabels[label['name']] = label['value']
            serviceLabels['app'] = deployName
            serviceLabels['endpointId'] = endpointId
            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                serviceLabels['project-id'] = projectId
                serviceLabels['user'] = userName
            serviceJson['metadata']['labels'] = serviceLabels
            serviceJson['spec']['selector']['app'] = deployName

            if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                if ports :
                    for port in ports :
                        portJson = { 'port': portNumber, 'targetPort': portNumber, 'name': portName }
                        serviceJson['spec']['ports'].append(portJson)
            
            elif ("triton"==servingFramework.lower()) :
                if not ports:
                    portJson = [{"protocol": "TCP", "port": 8000, "name": "http-triton", "targetPort": 8000},{"protocol": "TCP", "port": 8001, "name": "grpc-triton", "targetPort": 8001},{"protocol": "TCP", "port": 8002, "name": "metrics-triton", "targetPort": 8002}]
                    serviceJson['spec']['ports'] = portJson
                else :
                    enteredPorts = []
                    for port in ports :
                        portName = port['name']
                        portNumber = int(port['value'])
                        if(portName.lower() =='http' or portName.lower() =='http-triton'):
                            portJson = { 'protocol': "TCP", 'port': portNumber, 'name': 'http-triton', 'targetPort': portNumber }
                            serviceJson['spec']['ports'].append(portJson)
                            enteredPorts.append('http-triton')
                        elif(portName.lower() =='grpc' or portName.lower() =='grpc-triton'):
                            portJson = { 'protocol': "TCP", 'port': portNumber, 'name': 'grpc-triton', 'targetPort': portNumber }
                            serviceJson['spec']['ports'].append(portJson)
                            enteredPorts.append('grpc-triton')
                        elif(portName.lower() =='metrics' or portName.lower() =='metrics-triton'):
                            portJson = { 'protocol': "TCP", 'port': portNumber, 'name': 'metrics-triton', 'targetPort': portNumber }
                            serviceJson['spec']['ports'].append(portJson)
                            enteredPorts.append('metrics-triton')
                        else :
                            portJson = { 'protocol': "TCP", 'port': portNumber, 'name': portName, 'targetPort': portNumber }
                            serviceJson['spec']['ports'].append(portJson)
                    if 'http-triton' not in enteredPorts :
                        portJson = { 'protocol': "TCP", 'port': 8000, 'name': 'http-triton', 'targetPort': 8000 }
                        serviceJson['spec']['ports'].append(portJson)
                    if 'grpc-triton' not in enteredPorts :
                        portJson = { 'protocol': "TCP", 'port': 8001, 'name': 'grpc-triton', 'targetPort': 8001 }
                        serviceJson['spec']['ports'].append(portJson)
                    if 'metrics-triton' not in enteredPorts :
                        portJson = { 'protocol': "TCP", 'port': 8002, 'name': 'metrics-triton', 'targetPort': 8002 }
                        serviceJson['spec']['ports'].append(portJson)


        if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
            
            ### Service Role File Creation ###
            serviceRuleJson = None
            jsonFilePath = deplFilesFolder + CUSTOM_SERVRULE_TEMPLATE
            with open(jsonFilePath, 'r') as fp:
                serviceRuleJson = json.load(fp)
            if serviceRuleJson is not None :
                serviceRuleJson['metadata']['name'] = deployName
                serviceRuleJson['metadata']['labels']['endpointId'] = endpointId
                for rule in serviceRuleJson['spec']['rules'] :
                    rule['services'].append(destServiceName)

            ### Service Role Binding File Creation ###
            servRuleBindJson = None
            jsonFilePath = deplFilesFolder + CUSTOM_SERVRULEBIND_TEMPLATE
            with open(jsonFilePath, 'r') as fp:
                servRuleBindJson = json.load(fp)
            if servRuleBindJson is not None :
                servRuleBindJson['metadata']['name'] = deployName
                servRuleBindJson['metadata']['labels']['endpointId'] = endpointId
                servRuleBindJson['spec']['roleRef']['name'] = deployName
            
            ### Destination Rule File Creation ###
            destRuleJson = None
            jsonFilePath = deplFilesFolder + CUSTOM_DESTRULE_TEMPLATE
            with open(jsonFilePath, 'r') as fp:
                destRuleJson = json.load(fp)
            if destRuleJson is not None :
                destRuleJson['metadata']['name'] = deployName
                destRuleJson['metadata']['labels']['endpointId'] = endpointId
                destRuleJson['spec']['host'] = destServiceName
                for subset in destRuleJson['spec']['subsets'] :
                    subset['name'] = modelVersion
                    subset['labels']['version'] = modelVersion

        ### Virtual Service File Creation ###
        vsJson = []
        jsonFilePath = deplFilesFolder + CUSTOM_VS_TEMPLATE
        if "djl"==servingFramework.lower():
            jsonFilePath = deplFilesFolder + DJL_VS_TEMPLATE
        for idx,modelSpec in enumerate(modelSpecs) :
            prefixUri = modelSpec.get('modelUris').get('prefixUri')
            predictUri = modelSpec.get('modelUris').get('predictUri')
            
            endpointUri = '/'+endpointVersion + (contextUri if contextUri.startswith('/') else ('/'+contextUri))
            endpointUri += prefixUri if prefixUri.startswith('/') else ('/'+prefixUri)
            endpointUri += urlCustomPart
            endpointUri += predictUri if predictUri.startswith('/') else ('/'+predictUri)

            if ("custom"==servingFramework.lower()):
                rewriteUri = predictUri if predictUri.startswith('/') else ('/'+predictUri)
            elif ("triton"==servingFramework.lower()) :
                rewriteUri = '/' + TRITON_MDL_VERSION + urlCustomPart + '/infer'
            elif ("djl"==servingFramework.lower()) :
                rewriteUri = '/predictions/' + modelName+"-"+modelVersion
            print('==rewriteUri==', rewriteUri)
            print('==endpointUri==', endpointUri)
            
            with open(jsonFilePath, 'r') as fp:
                vsJson.append(json.load(fp))
            if vsJson[idx] is not None :
                vsJson[idx]['metadata']['name'] = deployName+'-'+str(idx)
                vsLabels = vsJson[idx]['metadata']['labels']
                if vsLabels is not None:
                    vsLabels['app'] = deployName
                    vsLabels['endpointId'] = endpointId
                for http in vsJson[idx]['spec']['http'] :
                    for match in http['match'] :
                        match['uri']['prefix'] = endpointUri
                    http['rewrite']['uri'] = rewriteUri
                    for route in http['route'] :
                        route['destination']['host'] = destServiceName
                        if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
                            route['destination']['subset'] = modelVersion
                        route['destination']['port']['number'] = vsExposedPort

        print('deploymentJson===',deploymentJson)
        with open("deployment.json", "w") as outfile:
            json.dump(deploymentJson, outfile)
        with open("service.json", "w") as outfile:
            json.dump(serviceJson, outfile)
        print('vsJson===',vsJson)
        for idx, jsonF in enumerate(vsJson) :
            fileName: str = "virtualservice{}.json".format(idx)
            with open(fileName, "w") as outfile:
                json.dump(jsonF, outfile)

        if ("custom"==servingFramework.lower() or "djl"==servingFramework.lower()) :
            with open("serviceRole.json", "w") as outfile:
                json.dump(serviceRuleJson, outfile)
            with open("destinationRule.json", "w") as outfile:
                json.dump(destRuleJson, outfile)
            with open("serviceRoleBinding.json", "w") as outfile:
                json.dump(servRuleBindJson, outfile)


if __name__=="__main__":
    deplTemplatesPath = sys.argv[1]
    dataFetchUrl = sys.argv[2]
    namespace = sys.argv[3]
    servingFramework = sys.argv[4]
    fileUtil = DeploymentFileCreation()
    fileUtil.createDeploymentFiles(deplTemplatesPath, dataFetchUrl, namespace, servingFramework)