# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from common.ainauto_logger_factory import AinautoLoggerFactory
from common.app_config_manager import AppConfigManager
import requests
logger = AinautoLoggerFactory().get_logger()
app_config = AppConfigManager().get_app_config()

TENANT_ID_PLACEHOLDER = "{tenant_id}"


class ProjectManagementService():

    def __init__(self):
        pass

    # get the details of a tenant id
    def get_tenant_details(self, tenant_id):
        url = app_config['AICLOUD_CONFIG']['get_tenant_url'].replace(
            TENANT_ID_PLACEHOLDER, tenant_id)
        headers = {
            "userId": app_config['AICLOUD_CONFIG']['user_id'],
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        # Check the response status code
        response_data = None
        if response.status_code == 200:
            response_data = response.json()
            response_data = response_data.get(
                'data').get('tenant').get('userLists')
        return response_data
    
    #get tenant details of a project
    def get_tenant_details_project(self, tenant_id):
        url = app_config['AICLOUD_CONFIG']['get_tenant_projects_url'].replace(
            TENANT_ID_PLACEHOLDER, tenant_id)
        headers = {
            "userId": app_config['AICLOUD_CONFIG']['user_id'],
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        # Check the response status code
        response_data = None
        if response.status_code == 200:
            response_data = response.json()
            response_data = response_data.get(
                'data').get('projects')
        return response_data
