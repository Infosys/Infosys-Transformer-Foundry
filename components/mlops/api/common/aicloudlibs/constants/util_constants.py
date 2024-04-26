# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

CREATE_PIPELINE="createPipeline"
EXECUTE_PIPELINE="executePipeline"
DEPLOY_MODEL="deployModel"
UPLOAD_DATASET="uploadDataset"
VIEW="view"
WORKSPACEADMIN="workspaceAdmin"

MLOPS_SERVICES=["createPipeline","executePipeline","deployModel","uploadDataset","view","workspaceAdmin"]
GPMS_OPERATOR_OPTIONS=["kubeflow", "airflow"]
GPMS_RUNTIME_OPTIONS=["kubernetes", "vm"]
GPMS_STORAGE_OPTIONS=["INFY_AICLD_MINIO","INFY_AICLD_NUTANIX"]
GPMS_VOLUME_OPTIONS=["platform", "pipeline"]