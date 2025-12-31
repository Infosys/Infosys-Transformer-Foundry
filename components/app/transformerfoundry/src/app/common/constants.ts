/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const CONSTANTS = {
  APIS: {
    PL_MGMT_SERVICE: {
      GET_PIPELINES: '/api/v2/pipelines/list/<<ID>>',
      GET_PL_EXEC_LIST: '/api/v2/pipelines/list/<<ID>>/execution',
      GET_PIPELINE_DEF: '/api/v2/pipelines/<<ID>>',
      POST_EXE_PL_DETAILS: '/api/v2/pipelines/execute/<<ID>>',
      POST_PIPELINES: '/api/v2/pipelines/create',
      GET_EXECUTION_DETAILS: '/api/v2/pipelines/execution/<<ID>>'
    },
    TRANSTUDIO_SERVICE: {
      GET_API: '/tfstudioservice/api/v1/pipelines/formdata/<<ID>>',
      POST_API: '/tfstudioservice/api/v1/pipelines/formdata',
      GET_USER_SESSION_DETAILS: '/tfstudioservice/api/v1/user/session/<<ID>>',
      GET_GLOBAL_TEMPLATES: '/tfstudioservice/api/v1/pipelines/global',
      POST_GLOBAL_TEMPLATES_HISTORY: '/tfstudioservice/api/v1/pipelines/global',
      GET_NODE_YML_DETAILS:'/tfstudioservice/api/v1/pipelines/nodeyml',
    },
    PRJCT_MGMT_SERVICE: {
      GET_PRJCT_LIST: '/api/v1/tenants/<<ID>>/projects',
      POST_PRJCT_DATA: '/api/v1/projects',
      PRJCT_DETAILS: '/api/v1/projects/<<ID>>',
      GET_TENANT_DETAIL: '/api/v1/tenants/<<ID>>'
    },
    MODEL_MGMT_SERVICE: {
      GET_MODEL_LIST: '/api/v1/models?projectId=<<ID>>',
      GET_MODEL_DETAILS: '/api/v1/models/<<MID>>/versions/<<MVER>>',
      UPDATE_MODEL_DETAILS: '/api/v1/models/<<MID>>',
      DEPLOY_MODEL_DETAILS: '/api/v1/endpoint/deploy',
      POST_ENDPOINT: '/api/v1/endpoint',
      GET_ENDPOINT: '/api/v1/endpoint/<<ID>>',
      GET_ENDPOINT_LIST: '/api/v1/endpoint?projectId=<<PID>>',
    },
    JOB_MGMT_SERVICE: {
      GET_PL_DETAILS: '/api/v1/pipelines/trainingjobs/<<ID>>',
      POST_PL_DATA: '/api/v1/pipelines/trainingjobs',
      POST_TRAIL_DATA: '/api/v1/pipelines/trainingjobs/trial',
      GET_PL_LIST: '/api/v1/pipelines/trainingjobs?projectId=<<ID>>',
      GET_TRIAL_STATUS: '/api/v1/pipelines/trainingjobs/trial/trialId?trialId=<<ID>>',
      GET_TRIAL_LIST: '/api/v1/pipelines/trainingjobs/trial/<<ID>>?projectId=<<PID>>',
      GET_EXPID: '/api/v1/pipelines/trainingjobs/mlfexp/<<NAME>>',
    },
    ML_FLOW_SERVICE: {
      SEARCH_RUNS: '/#/experiments/<<EXID>>/runs/<<ID>>',
    },
    LEADERBOARD_SERVICE: {
      GET_LEADERBOARD: '/api/v1/query/<<INDEX>>/search',
      POST_BENCHMARK: '/api/v1/query/<<INDEX>>/<<REQUEST>>',
    },
    RAG_PLAYGROUND_SERVICE: {
      UPLOAD_FILE: '/api/v1/rag/uploadfile',
      CREATE_SETUP: '/api/v1/rag/setup',
      GET_INDEX_LIST: '/api/v1/rag/indexes',
      DELETE_INDEX: '/api/v1/rag/deleteIndex/<<INDEXID>>',
      GET_INDEX_STATUS: '/api/v1/rag/setupstatus/<<INDEXID>>',
      SEARCH_RAG: '/api/v1/inference/search',
      MESSAGE_METADATA: '/api/v1/rag/getSearch',
      POST_MESSAGE_METADATA: '/api/v1/rag/search',
    },
    PROMPT_LIBRARY_SERVICE: {
      POST_PROMPT_LIBRARY: '/api/v1/library/prompt',
      GET_PROMPT_LIBRARY: '/api/v1/library/prompt',
      UPDATE_PROMPT_LIBRARY: '/api/v1/library/prompt',
      GET_PROMPT_LIBRARY_BY_ID: '/api/v1/library/prompt',
    }
    
  },
  CONFIG: {
    ENV: 'environment',
    USER_ID: 'userId',
    PROJECT_ID: 'projectId',
    PL_MGMT_SERVICE_BASER_URL_V1: "pipelineManagementService-v1",
    PL_MGMT_SERVICE_BASER_URL_V2: "pipelineManagementService-v2",
    MODEL_MGMT_SERVICE_BASER_URL: "modelManagementService",
    PROJECT_MGMT_SERVICE_BASER_URL: "projectManagementService",
    ML_FlOW_SERVICE_BASER_URL: "mlFlowServiceBaserUrl",  
    // replace the appropriate mlflow url in config-data.json file
    TENANT_ID: 'tenantID',
    TS_GLBL_PROJECT_ID: 'tsGlobalProjectID',
    TS_GLBL_PROJECT_ADMIN_ID: 'tsGlobalProjectAdminID',
    LEADERBOARD_MFE_URL:'leaderboardMfeUrl',
    GUSER_ID: 'gUserId',
    RAG_PROJECT_ID: 'ragProjectId',
    RAG_SEARCH_BASE_URL: 'ragSearchBaseUrl',
    PROMPT_LIBRARY_BASE_URL:'promptlibraryUrl',
  },
  PLACEHOLDER: {
    ID: "<<ID>>",
    PID: "<<PID>>",
    MID: "<<MID>>",
    EXID: "<<EXID>>",
    MVER: "<<MVER>>",
    NAME: "<<NAME>>",
    INDEX: "<<INDEX>>",
    REQUEST: "<<REQUEST>>",
    INDEXID: "<<INDEXID>>",
    GID: "<<GID>>",
  },
  PIPELINE_EXECUTION_STATUS: {
    INITIATED: 'INITIATED',
    INPROGRESS: 'INPROGRESS',
    SUCCESS: 'SUCCESS',
    FAILURE: 'FAILURE'
  },
  TRIAL_EXECUTION_STATUS: {
    INITIATED: 'Initiated',
    INPROGRESS: 'InProgress',
    SUCCESS: 'Succeeded',
    FAILURE: 'Failed'
  },
  FEATURE_ID_CONFIG: {
    PROJECT_CREATE: 'project-create',
    PROJECT_DELETE: 'project-delete',
    PROJECT_LIST: 'project-list',
    PROJECT_VIEW: 'project-view',
    PIPELINE_CREATE: 'pipeline-create',
    PIPELINE_EXECUTE: 'pipeline-execute',
    PIPELINE_LIST: 'pipeline-list',
    PIPELINE_VIEW: 'pipeline-view',
    MODEL_DEPLOY: 'model-deploy',
    MODEL_LIST: 'model-list',
    MODEL_VIEW: 'model-view',
    MODEL_CREATE: 'model-create',
    USER_LIST: 'user-list',
    USER_VIEW: 'user-view',
    USER_EDIT: 'user-edit',
    USER_DELETE: 'user-delete',
  },
  FEATURE_ERROR_MSG: {
    NOT_ALLOWED: "You are not authorized to this content."
  },

};
