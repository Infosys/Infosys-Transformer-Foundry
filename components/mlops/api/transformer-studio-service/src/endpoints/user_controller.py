# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

import calendar
import datetime
import time
from fastapi import APIRouter, File, UploadFile, Header
import json

from pydantic import BaseModel
from common.app_config_manager import AppConfigManager
from data.api_schema_data import ResponseData
from service.project_management_service import ProjectManagementService
from .pipeline_base import *

app_config = AppConfigManager().get_app_config()
RBAC_FILEPATH = "../config/rbac.json"
with open(RBAC_FILEPATH, 'r') as json_file:
    rbac_data = json.load(json_file)

# APIRouter creates path operations for module
router = APIRouter(prefix="/tfstudioservice/api/v1/user",
                   responses={404: {"description": "Not found"}})


class RoleTypeCde(object):
    admin: int = 101
    agent: int = 102

# get user session details and their corresponding access level
@router.get("/session/{userId}", response_model=ResponseData, tags=["User"],
            summary="Get user session details", include_in_schema=SHOW_PRIVATE_API)
async def get_session_data(userId):
    start_time = time.time()
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    date_time_stamp = datetime.datetime.fromtimestamp(
        utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
    # -------------------- start: session handler ----------------
    proj_mgmt_service = ProjectManagementService()
    user_list = proj_mgmt_service.get_tenant_details(
        app_config['AICLOUD_CONFIG']['tenant_id'])
    found_admin = [x for x in user_list if x.get('userEmail') == userId]
    if found_admin:
        user_rbac_data_list = get_rbac_for(
            RoleTypeCde.admin)  # superadmin
    else:
        user_rbac_data_list = get_rbac_for(RoleTypeCde.agent)  # agent

    # -------------------- end: session handler ----------------
    elapsed_time = round(time.time() - start_time, 3)
    response = ResponseData(response={"featureAuthDataList": user_rbac_data_list},
                            responseCde=API_RESPONSE_CDE_SUCCESS, responseMsg=API_RESPONSE_MSG_SUCCESS,
                            timestamp=date_time_stamp, responseTimeInSecs=(elapsed_time))
    return response

# get the role based access control data for the user
def get_rbac_for(role_type_cde):
    user_rbac_data_list = []

    def _get_role_data(feature_data):
        data = [x.get('accessLevelCde') for x in feature_data.get(
            'permissions') if x.get('roleTypeCde') == role_type_cde]
        return data[0] if data else 0
    for feature_data in rbac_data.get('appRoleBasedAccessControlMapping'):
        user_rbac_data = {
            "featureId": feature_data.get('featureId'),
            "accessLevelCde":  _get_role_data(feature_data)
        }
        user_rbac_data_list.append(user_rbac_data)
    return user_rbac_data_list
