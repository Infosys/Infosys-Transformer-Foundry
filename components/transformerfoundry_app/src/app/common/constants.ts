/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

// Constants file to store all the constants used in the application

export const CONSTANTS = {
  APIS: {
    MODEL_MGMT_SERVICE: {
      GET_MODEL_LIST: '/api/v1/models?projectId=<<ID>>',
      GET_MODEL_DETAILS: '/api/v1/models/<<MID>>/versions/<<MVER>>',
    },
  },
  CONFIG: {
    ENV: 'environment',
    USER_ID: 'userId',
    PROJECT_ID: 'projectId',
    AI_CLD_MGMT_SERVICE_BASER_URL: "aiCloudManagementServiceBaseUrl",
    TS_GLBL_PROJECT_ID: 'tsGlobalProjectID',
    TS_GLBL_PROJECT_ADMIN_ID: 'tsGlobalProjectAdminID',
    LEADERBOARD_MFE_URL:'leaderboardMfeUrl',
  },
  PLACEHOLDER: {
    ID: "<<ID>>",
    MID: "<<MID>>",
    MVER: "<<MVER>>",
  }
};
