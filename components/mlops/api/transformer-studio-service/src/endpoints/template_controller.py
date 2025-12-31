# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from fastapi import APIRouter, Header
from pydantic import BaseModel, validate_model
from common.app_config_manager import AppConfigManager
from service.mongo_db_handler import MongoDbHandler
from .pipeline_base import *
import re

app_config = AppConfigManager().get_app_config()


# APIRouter creates path operations for module
router = APIRouter(prefix="/tfstudioservice/api/v2/pipelines/global",
                   responses={404: {"description": "Not found"}})

class TemplateHistoryRecord(BaseModel):
    projectId: str
    templateId: str
    createdOn: str = ""
    createdBy: str = ""
    updatedOn: str = "null"
    updatedBy: str = "null"

# GET for fetching the list of global templates
@router.get("/",tags=["TemplateData"],summary="Fetch the list of global templates", include_in_schema=True)
async def get_template_list():
    try:
        mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
        documents = mongo_db_handler.get_documents(GLOBAL_TEMPLATES, {})

        res_list = []
        for document in documents:
            document['id'] = str(document.pop('_id', None))
            # print(f"Y {document}")
            res_list.append(document)
        if len(res_list) == 0:
            mongo_db_handler.disconnect()
            return {"code": 200, "status": "success", "data": []}

        return {"code": 200, "status": "success", "data": {"pipelines": res_list}}
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"Error: {e}")
        return {"code": 1017, "status": "FAILED", "message": "Internal Server Error"}

# POST for registering templateID and projectID in the template history table
@router.post("/", tags=["TemplateData"], summary="Register a global template and Project", include_in_schema=True)
async def add_template_history(template: TemplateHistoryRecord, userId: str = Header(...)):
    # Validate userId email format (assuming validate_email_format function exists)
    if not validate_email_format(userId):
        # If validation fails, return an error response
        return {
            "error": {
                "code": 1001,
                "status": "FAILED",
                "message": "Invalid email format for userId"
            }
        }

    mongo_db_handler = MongoDbHandler(**CONFIG_DICT)
    doc = template.dict()
    datetime = datetime.datetime.utcnow()

    doc['createdOn'] = datetime.strftime("%Y-%m-%d %H:%M:%S")
    doc['createdBy'] = userId

    try:
        # Assuming validate_model function exists and raises an exception on failure
        validate_model(doc)
        result = mongo_db_handler.insert_document(GLOBAL_TEMPLATES_IMPORT_HISTORY, doc)
        if not result:
            raise Exception("Failed to insert document")
    except Exception as e:
        # Log the error or handle it as needed
        return {
            "error": {
                "code": 1017,
                "status": "FAILED",
                "message": str(e)
            }
        }

    # If everything is successful, return a success response
    return {
        "success": {
            "code": 200,
            "status": "SUCCESS",
            "message": "Document inserted successfully"
        }
    }

def validate_email_format(user_id: str) -> bool:
    # Regular expression for validating an Email
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    # Return True if the email matches the pattern, False otherwise
    return re.match(regex, user_id, re.IGNORECASE) is not None