# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
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

TEMPLATE_PATH = os.getcwd()+"/rag/service"


class PayloadGenerationKubeflow:
  def __init__(self) -> None: 
      self.__env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
      TEMPLATE_NAME = "RAG_TEMPALTE.j2"
      self.__kubeflow_template = self.__env.get_template(TEMPLATE_NAME)

  def get_kubeflow_code(self,payload, config_path_var, ragImageName, ragDppImage):
      
    kueflow_code = self.__kubeflow_template.render(
        payload = payload,
        config_path_var = config_path_var,
        ragImageName = ragImageName,
        ragDppImage = ragDppImage
    )
    return kueflow_code


if __name__ == "__main__":
  # Initialize the class
  kubeflw_obj = PayloadGenerationKubeflow()
  
  pipeline_data ={
    "projectId": "0042088b75364b2db1e5672d2911676e",
    "name": "embedding",
    "description": "benchmark embedding",
    "type": "embedding",
    "configuration": {
      "model": [
        {
          "modelName" : "msmarco-distilbert-base-tas-b",
          "modelPathorId": "${MODEL_PATH}",
          "datatype": "fp16",
          "quantizeMethod": "static",
          "args": [
            ]
        },
          {
          "modelName" : "all-MiniLM-L6-v2",
          "modelPathorId": "${MODEL_PATH}",
          "datatype": "fp32",
          "quantizeMethod": "NA",
          "args": [
                
          ]
        },
        {
          "modelName" : "gte-tiny",
          "modelPathorId": "${MODEL_PATH}",
          "datatype": "fp32",
          "quantizeMethod": "NA",
          "args": [
          
          ]
        }
      ],
      "data": [
        {
          "name": "multiple",
          "scope": "public",
          "language": "java",
          "batchSize": 1,
          "limit": 1
        }
      ],
      "task": "Reranking",
      "dataStorage": {
        "storageType": "INFY_AICLD_NUTANIX",
        "uri": "${DATA_STORAGE_URI}"
      }
    },
    "resourceConfig": {
      "gpuQty": 1,
      "gpuMemory": "80GB",
      "volume": {
        "name": "pvc-model-repo",
        "mountPath": "/mnt/models"
      }
    }
  }
  kubeflow_code = kubeflw_obj.get_kubeflow_code(pipeline_data)

  # save rendered data to file
  with open('word_count_kubeflow_pipeline_v555.py', 'w') as f:
    f.write(kubeflow_code)