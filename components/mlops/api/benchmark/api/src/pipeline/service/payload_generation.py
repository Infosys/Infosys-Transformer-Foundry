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
            payload = pipeline_data,
            arg_values = model_arg,
            projectId = projectId,
            indexName=indexName,
            taskImage=taskImage,
            consolidatedImage=consolidatedImage,
            esImage=esImage
        )
        return kueflow_code