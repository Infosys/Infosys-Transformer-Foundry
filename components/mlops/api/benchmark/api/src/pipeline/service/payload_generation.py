# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import uuid
import jinja2
import argparse
import json
import urllib.request
import sys

TEMPLATE_PATH = "/src/pipeline/service/"

# Method to frame the pipeline request format to trigger and execute the pipeline
class CodeGenerationKubeflow:
    def __init__(self, type) -> None:
        
        self.__env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
        if(type=="code"):
            TEMPLATE_NAME = "CODE_TEMPALTE.j2"
        elif(type=="text"):
            TEMPLATE_NAME = "TEXT_TEMPLATE.j2"
        elif(type=="embedding"):
            TEMPLATE_NAME = "EMBEDDING_TEMPALTE.j2"
            
          
        self.__kubeflow_template = self.__env.get_template(TEMPLATE_NAME)

    def get_kubeflow_code(self, pipeline_data,projectId,metadataObj,indexName,taskImage,consolidatedImage,esImage):
        # render template
        model_arg = []
        for i in range(len(pipeline_data['configuration']['model'])):
          if pipeline_data['configuration']['model'][i]['args'] != None:
            arglist= pipeline_data['configuration']['model'][i]['args']
            argstring=""
            userList=[]
            for arg in arglist:
                floatval = arg['value'].replace('.','')
                if arg['value'] != "true" and arg['value'] != "false" and arg['value'].isdigit()==False and floatval.isdigit()==False:
                  argstring = argstring + arg['name'] + "':'" + arg['value'] + "','"
                  
                else:
                  argstring = argstring + arg['name'] + "':" + arg['value'] + ",'" 
                userList.append(arg['name'])
            if(len(metadataObj)!=0):
              for v in metadataObj:
                print(v)
                if v['model gen args name'] not in userList:
                  if v['model gen args name']=="eos":
                    argstring = argstring + v['model gen args name'] + "':'" + v['model arg defult value'] +"','"
                  else:
                    argstring = argstring + v['model gen args name'] + "':" + v['model arg defult value'] + ",'" 
            model_arg.append(argstring)
            print(model_arg)
        print(model_arg)
        kueflow_code = self.__kubeflow_template.render(
            # project_name=pipeline_data['name'],
            payload = pipeline_data,
            arg_values = model_arg,
            projectId = projectId,
            indexName=indexName,
            taskImage=taskImage,
            consolidatedImage=consolidatedImage,
            esImage=esImage
        )
        return kueflow_code


# if __name__ == "__main__":
#     # Initialize the class
#     kubeflw_obj = CodeGenerationKubeflow()

  
#     pipeline_data ={
#   "projectId": "t7567657",
#   "name": "embedding",
#   "description": "benchmark embedding",
#   "type": "embedding",
#   "configuration": {
#     "model": [
#       {
#         "modelName" : "msmarco-distilbert-base-tas-b",
#         "modelPathorId": "${REPO_NAME}/msmarco-distilbert-base-tas-b",
#         "datatype": "fp16",
#         "quantizeMethod": "static",
#         "args": [
#           ]
#       },
#        {
#         "modelName" : "all-MiniLM-L6-v2",
#         "modelPathorId": "${REPO_NAME}/all-MiniLM-L6-v2",
#         "datatype": "fp32",
#         "quantizeMethod": "NA",
#         "args": [
             
#         ]
#       },
#       {
#         "modelName" : "gte-tiny",
#         "modelPathorId": "${REPO_NAME}/gte-tiny",
#         "datatype": "fp32",
#         "quantizeMethod": "NA",
#         "args": [
        
#         ]
#       }
#     ],
#     "data": [
#       {
#         "name": "multiple",
#         "scope": "public",
#         "language": "java",
#         "batchSize": 1,
#         "limit": 1
#       }
#     ],
#     "task": "Reranking",
#     "dataStorage": {
#       "storageType": "INFY_AICLD_NUTANIX",
#       "uri": "${REPO_NAME}/testpipeline/10/input"
#     }
#   },
#   "resourceConfig": {
#     "gpuQty": 1,
#     "gpuMemory": "80GB",
#     "volume": {
#       "name": "pvc-model-repo",
#       "mountPath": "/mnt/models"
#     }
#   }
# }
#     kubeflow_code = kubeflw_obj.get_kubeflow_code(pipeline_data)

#     # save rendered data to file
#     with open('word_count_kubeflow_pipeline_v555.py', 'w') as f:
#         f.write(kubeflow_code)
