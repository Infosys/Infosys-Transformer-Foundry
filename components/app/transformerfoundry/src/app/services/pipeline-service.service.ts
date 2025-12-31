/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ConfigDataHelper } from '../utils/config-data-helper';
import { CONSTANTS } from '../common/constants';
import { PipelineData } from '../data/pipeline-data';
import { ExecutePipelineData } from '../data/execute-pipeline-data';
import { PipelineDetailsData } from '../data/pipeline-details-data';
import { DataStorageService } from './data-storage.service';
import * as yaml from 'js-yaml';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PipelineServiceService {
  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper,private storageService:DataStorageService) { }
  private nodeConfigData = undefined;

  model: any = {
    key:''
  };

  // get the list of pipelines for the project id
  getPipelineListData(projectId: string, isRag?: boolean) {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': isRag?parent.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID):parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.GET_PIPELINES.replace(CONSTANTS.PLACEHOLDER.ID, projectId);
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            fulfilled(_data['data']['pipelines'] as PipelineData);
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // get the execution data of pipelines
  getExecutionData(pipelineId: string) {
    const parent = this;
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.GET_PL_EXEC_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${pipelineId}`);

    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };

    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] == 200) {
              fulfilled(_data['data']['executions'])
            } else {
              rejected(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // get the pipeline details by id
  getDataById(id: number) {
    const parent = this;
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.GET_PIPELINE_DEF.replace(CONSTANTS.PLACEHOLDER.ID, `${id}`);
    return new Promise(function (fulfilled, rejected) {
        parent.httpClient.get(url)
            .subscribe(
                _data => {
                    fulfilled(_data['response']);
                },
                _error => {
                    rejected(_error);
                }
            );
    });
  }

  // get the payload details by id
  getPayloadData(pipelineId) {
    const parent = this;
    const apiUrl: string = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) + CONSTANTS.APIS.TRANSTUDIO_SERVICE.GET_API.replace(CONSTANTS.PLACEHOLDER.ID, `${pipelineId}`);
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(apiUrl)
        .subscribe(
          _data => {
            if(_data['response'][0]['message'])
                rejected(_data['response'][0]);
            fulfilled(_data['response']);
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // get the execution details by execution id
  getExecutionDetails(executionid: string) {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.GET_EXECUTION_DETAILS.replace(CONSTANTS.PLACEHOLDER.ID, `${executionid}`);
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data["code"] === 200) {
              fulfilled(_data['data']['response']['data']);
            } else {
              rejected(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // create node form data
  postNodeFormData(payload: any) {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const apiUrl: string = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) + CONSTANTS.APIS.TRANSTUDIO_SERVICE.POST_API;
    console.log("api url:", apiUrl);
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(apiUrl, payload, requestOptions)
        .subscribe(
          _data => {
            fulfilled(_data['response']);
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // create pipeline details
  createPipelineDetails(pipeline: PipelineDetailsData) {
    const parent = this;
    const body = JSON.stringify(pipeline);
    // const userId = parent.storageService.getData().userId;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.POST_PIPELINES;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, pipeline, requestOptions).subscribe(
        (_data) => {
          // console.log("createPipelineDetails",_data);
          if (_data["code"] === 200) {
            console.log("SUccess", _data);

            fulfilled(_data["data"]);
          } else {
            rejected(_data["response"]);
          }
        },
        (_error) => {
          rejected(_error['error']);
        }
      );
    });
  }

  // execute pipeline details
  postExecutePipelineDetails(pipelineId: string, pipeline: ExecutePipelineData) {
    const parent = this;
    const body = JSON.stringify(pipeline);
    // const userId = parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID); //get from session
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.POST_EXE_PL_DETAILS.replace(CONSTANTS.PLACEHOLDER.ID, `${pipelineId}`);
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, body, requestOptions)
        .subscribe(
          _data => {
            if (_data['responseCde'] > 0) {
              rejected(_data['response'])
            } else {
              fulfilled(_data['response']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // get the pipeline details by id
  getPipelineDefinition(pipelineId: string, globalCall?: boolean) {
    const parent = this;
    const userId = globalCall? parent.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID): parent.storageService.getData().userId
    console.log("userId in service",userId,globalCall);
    
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.PL_MGMT_SERVICE.GET_PIPELINE_DEF.replace(CONSTANTS.PLACEHOLDER.ID, `${pipelineId}`);
      const headerDict = {
        'Accept': 'application/json',
        'userId':userId,
        'Content-Type': 'application/json',
      }
      const requestOptions = {
        headers: new HttpHeaders(headerDict),
      };
      return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] === 200) {
              console.log(_data);
              fulfilled(_data['data']);
            } else {
              rejected(_data)
              // TODO: handle error
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }


  // latest getconfigdata integrated with jodeyml api
  getNodeConfigData(): Promise<any> {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      // 'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    };
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.TRANSTUDIO_SERVICE.GET_NODE_YML_DETAILS;
    // const url = "http://127.0.0.1:8009/tfstudioservice/api/v1/pipelines/get-node-data";
  
    return new Promise(function (fulfilled, rejected) {

      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] === 200) {
              console.log(_data);
              fulfilled(_data['data']['node_data']);
            } else {
              rejected(_data)
             
            }
          },
          _error => {
            rejected(_error);
          }
        );
    }
    );
  }

 

  // get the list of global templates
  getGlobalTemplates() {
    const parent = this;
    const url =
      // "http://localhost:8009" +
      parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.TRANSTUDIO_SERVICE.GET_GLOBAL_TEMPLATES;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url).subscribe(
        (_data) => {
          if (_data["code"] === 200) {
            fulfilled(_data["data"]);
          } else rejected(_data);
        },
        (_error) => {
          rejected(_error);
        }
      );
    });
  }

  // post the global templates history
  postGlobalTemplatesHistory(projectId: string, templateId: string) {
    const parent = this;
    const url =
      // "http://localhost:8009" +
      parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V2) +
      CONSTANTS.APIS.TRANSTUDIO_SERVICE.GET_GLOBAL_TEMPLATES;
    const headerDict = {
      userId: parent.storageService.getData().userId,
    };
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const request = {
      projectId: projectId,
      templateId: templateId,
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, request, requestOptions).subscribe(
        (_data) => {
          if (_data["code"] === 200) {
            fulfilled(_data["data"]);
          } else rejected(_data);
        },
        (_error) => {
          rejected(_error);
        }
      );
    });
  }
}
