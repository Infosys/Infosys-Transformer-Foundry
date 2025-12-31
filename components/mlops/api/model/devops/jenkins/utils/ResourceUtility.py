# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from kubernetes import client, config
from pprint import pprint
from kubernetes.client.rest import ApiException
import os
import sys

class ResourceUtility(object):
     
    def __init__(self,cfgFilePath:str):
        self.config_file=os.getenv("KUBE_CONFIG_FILE")
        if  self.config_file is None:
              self.config_file=cfgFilePath
        
    def _k8s_client(self):
            try:
                if not self.config_file:
                    return 

                kubeconf = self.config_file
                config.load_kube_config(config_file=kubeconf)
                api_client = client.CoreV1Api()
                if api_client is None:
                     return

                return api_client
            except ApiException as ex:
                print(str(ex))

    def _getQuota_details(self,namespace,gpuMemory):
            try:
                 api_client=self._k8s_client()
                 if gpuMemory.lower() == '20gb':
                       gpudet='requests.nvidia.com/mig-3g.20gb'
                 if gpuMemory.lower() == '40gb':
                       gpudet='requests.nvidia.com/mig-7g.40gb'
                 if gpuMemory.lower() == '80gb':
                       gpudet='requests.nvidia.com/gpu'
                 api_response=api_client.read_namespaced_resource_quota_with_http_info("compute-resources",namespace)
                 resquota=api_response[0].__dict__
                 spec=resquota['_status'].__dict__
                 hard=spec['_hard'][gpudet]
                 used=spec['_used'][gpudet]
                 quota_det = {'hard':hard, 'used':used}
                 return quota_det
            except ApiException as e:
                 print(str(e))

if __name__=="__main__":
    cfgFilePath=sys.argv[1]
    namespace=sys.argv[2]
    req_gpuQty=sys.argv[3]
    req_gpuMemory=sys.argv[4]
    resutil=ResourceUtility(cfgFilePath)
  
    quotadet=resutil._getQuota_details(namespace,req_gpuMemory)
    hard=int(quotadet['hard'])
    used=int(quotadet['used'])
    avail_qty=hard-used
    allocate_gpu=int(avail_qty)-int(req_gpuQty)
    if allocate_gpu >=0:
         is_allocate_gpu=True
    else:
         is_allocate_gpu=False
    print(is_allocate_gpu)