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

// Constants file to store all the constants used in the application
export const CONSTANTS = {
  APIS: {
    LEADERBOARD_SERVICE: {
      GET_LEADERBOARD: '/api/v1/utilities/elastic/<<REQUEST>>/search',
      POST_BENCHMARK: '/api/v1/utilities/elastic/<<REQUEST>>/search',
      GET_LEADERBOARD_COUNT: '/api/v1/utilities/elastic/<<REQUEST>>/count',
      POST_BENCHMARK_COUNT: '/api/v1/utilities/elastic/<<REQUEST>>/count',
    },
    BENCHMARK_SERVICE: {
      POST_BENCHMARK_SUBMIT: '/api/v1/benchmarks',
      GET_BENCHMARK_METADATA: '/api/v1/benchmarks/metadata/taskargs?benchmarkType=<<BENCHMARK>>&metadataType=<<METADATA>>',
      GET_BENCHMARK_DATASET: '/api/v1/benchmarks/metadata/data?benchmarkType=<<BENCHMARK>>&task=<<METADATA>>',
      GET_BENCHMARK_LIST: '/api/v1/benchmarks?projectId=<<ID>>',
      GET_BENCHMARK_STATUS: '/api/v1/benchmarks/<<ID>>',
    }
  },
  CONFIG: {
    ENV: 'environment',
    BENCHMARK_SERVICE_BASER_URL: "benchmarkServiceBaserUrl",
    LEADERBOARD_SERVICE_BASER_URL: "leaderboardServiceBaserUrl",
    PROJECT_ID: "projectId",
    USER_ID: "userId",
  },
  PLACEHOLDER: {
    REQUEST: "<<REQUEST>>",
    BENCHMARK: "<<BENCHMARK>>",
    METADATA: "<<METADATA>>",
    ID: "<<ID>>",
  },
  BENCHMARK_MODALITIES:{
    CODE: 'code',
    TEXT: 'text',
    EMBEDDING: 'embedding',
    RAG: 'rag'
  }
};
