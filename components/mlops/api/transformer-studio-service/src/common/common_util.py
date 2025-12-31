# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

class Singleton(type):
    """Singleton class to be use as base class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CommonUtil:
    @classmethod
    def update_app_info(self, req_res_dict: dict, about_app: dict):
        req_res_dict.update(about_app)
        new_record_list = []
        for record in req_res_dict['records']:
            new_record = {**{'workflow': []}, **record}
            workflow_list = new_record.get("workflow")
            is_exist = any(x['service_name'] == about_app['service_name'] and x['service_version'] == about_app['service_version']
                           for x in workflow_list if x.get('service_name'))
            if not is_exist:
                workflow_list.append(about_app)
            new_record_list.append(new_record)
        req_res_dict['records'] = new_record_list
