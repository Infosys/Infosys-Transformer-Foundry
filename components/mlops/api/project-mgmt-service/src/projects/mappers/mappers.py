# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: mappers.py
description: A Pydantic model object for project entity model 
             which maps the data model to the project entity schema
"""
from projects.exception.exception import *
import uuid 
 
def ResponseModel(code,data):
    return {
        "code": code,
        "status": "SUCCESS", 
        "data": data
    }

def ErrorResponseModel(code, message):
    return {
        "code": code,
        "status": "FAILURE", 
        "message": message
        }

#To check whether the uuid is valid or not.
def is_valid_uuid(val):
     try:
        uuid.UUID(str(val))
        return True
     except ValueError:
        return False