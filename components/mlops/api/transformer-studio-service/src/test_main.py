# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from fastapi.testclient import TestClient
import pytest
from .main import app
# , startup_db_client
from fastapi import Request
import logging
from src.endpoints import pipeline_formdata  as formdata
from src.endpoints import user_controller as user_controller

client = TestClient(app)
logger = logging.getLogger('custom_logger')
logger.setLevel(logging.DEBUG)

# startup_db_client()
# logger.debug("Connected to the MongoDB database!")

formData = {
    "flow": {
      "dataExtraction": {
        "type": "generic",
        "dependsOn": [],
        "input": {
          "config_file_path": "{{pipeline.variables.config_file_path}}",
          "orig_doc_root_path": "{{pipeline.variables.orig_doc_root_path}}",
          "work_root_path": "{{pipeline.variables.work_root_path}}"
        },
        "output": {
          "request_file_path": "./request_file_path.txt"
        },
        "stepConfig": {
          "entryPoint": [
            "python",
            "./downloader/src/extraction_container.py"
          ],
          "stepArguments": [],
          "imageUri": "artifactory.jfrog.io/pipeline/document-extraction-processors:v3"
        },
        "resourceConfig": {
          "computes": [
            {
              "type": "CPU",
              "maxQty": 5,
              "memory": 1,
              "minQty": 1
            }
          ]
        }
      }
    }
}

# test case for post form data with valid testing data
def test_post_form_data():
    logger.debug("Inside test_post_form_data")
    response = formdata.post_form_data(formData, "test_user")
    assert response != None

    
# test case for get form data with valid testing data
def test_get_form_data():
    logger.debug("Inside test_get_form_data")
    pipelineid = "8f347b8e-3a09-425b-b6af-c36b0cc044c9"
    response = formdata.get_form_data(pipelineid)
    assert response != None

#test case for get session data with valid testing data
def test_get_session_data():
    logger.debug("Inside test_get_session_data")
    userId = "test_user"
    response = user_controller.get_session_data(userId)
    assert response != None
