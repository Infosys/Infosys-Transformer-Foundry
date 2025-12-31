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
import { DataStorageService } from './data-storage.service';
import { JobDetailsData } from '../data/job-details-data';
import { ExecuteTrailData } from '../data/execute-trail-data';
import { UpdateModelData } from '../data/update-model-data';
import { DeployedModelData } from '../data/deploy-model-data';
import { EndpointData } from '../data/endpoint-data';

@Injectable({
  providedIn: 'root'
})
export class ModelService {

  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper, private storageService: DataStorageService) { }

  //this fn gets the list of models based on the project id.
  getModelList(projectId?) {
    const parent = this;
    const tsGlobalProjectID = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TS_GLBL_PROJECT_ID);
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${tsGlobalProjectID}`);
    let userId = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TS_GLBL_PROJECT_ADMIN_ID)
    if (projectId) {
      url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${projectId}`);
      userId = parent.storageService.getData().userId;
    }
    const headerDict = {
      'accept': 'application/json',
      'userId': userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['models']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  //this fn gets a particular model by passing userId, modelId and version.
  getModelData(modelId, version) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_DETAILS.replace(CONSTANTS.PLACEHOLDER.MID, `${modelId}`).replace(CONSTANTS.PLACEHOLDER.MVER, `${version}`);

    console.log("URL:", url);
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['model']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function gets the pipeline template based on the template id.
  getPlById(plTemplateId: string) {
    const parent = this;
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) +
      CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_PL_DETAILS.replace(CONSTANTS.PLACEHOLDER.ID, `${plTemplateId}`);
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['pipeline']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function creates the experiment details based on the experiment data.
  createExperimentDetails(experimentData: JobDetailsData) {
    const parent = this;
    const body = JSON.stringify(experimentData);
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) +
      CONSTANTS.APIS.JOB_MGMT_SERVICE.POST_PL_DATA;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, experimentData, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function executes the created experiment
  postTrailDetails(trailData: ExecuteTrailData) {
    const parent = this;
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) +
      CONSTANTS.APIS.JOB_MGMT_SERVICE.POST_TRAIL_DATA;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, trailData, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function gets the list of experiments based on the project id.
  getExperimentList(projectId: string) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) + CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_PL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${projectId}`);
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['pipelines']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function gets the list of trials based on the project id and pipeline id.
  getTrialList(projectId, pipelineId) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) + CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_TRIAL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${pipelineId}`).replace(CONSTANTS.PLACEHOLDER.PID, `${projectId}`)
    const headerDict = {
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function gets the trial status based on the trial id.
  getTrialStatus(trialID) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1) + CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_TRIAL_STATUS.replace(CONSTANTS.PLACEHOLDER.ID, `${trialID}`)
    const headerDict = {
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['trial']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function updates the model data based on the model id and update data.
  updateModelData(modelId: string, updateModelData: UpdateModelData){
      const parent = this;
      const headerDict = {
        'accept': 'application/json',
        'userId': parent.storageService.getData().userId,
        'Content-Type': 'application/json',
      }
      const requestOptions = {
        headers: new HttpHeaders(headerDict),
      };
      const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) +
        CONSTANTS.APIS.MODEL_MGMT_SERVICE.UPDATE_MODEL_DETAILS.replace(CONSTANTS.PLACEHOLDER.MID, `${modelId}`);
      console.log(url)
      console.log(updateModelData);
      return new Promise(function (fulfilled, rejected) {
        parent.httpClient.patch(url, updateModelData, requestOptions)
          .subscribe(
            _data => {
              if (_data['code'] != 200) {
                rejected(_data)
              } else {
                fulfilled(_data['data']);
              }
            },
            _error => {
              rejected(_error);
            }
          );
      });
    }

  // function deploys the model 
  createModelDeployment(deployData: DeployedModelData){
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.MODEL_MGMT_SERVICE.DEPLOY_MODEL_DETAILS;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, deployData, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // create endpoint for the model
  createEndpoint(endpointData: EndpointData){
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.MODEL_MGMT_SERVICE.POST_ENDPOINT;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, endpointData, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function to get the list of endpoints based on the project id.
  getEndPointList(projectId) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) 
              + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_ENDPOINT_LIST.replace(CONSTANTS.PLACEHOLDER.PID, `${projectId}`)
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']['endpoints']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function to get the endpoint details based on the endpoint id.
  getEndPoint(endpointId) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.MODEL_MGMT_SERVICE_BASER_URL) 
              + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_ENDPOINT.replace(CONSTANTS.PLACEHOLDER.ID, `${endpointId}`)
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function to get the mlflow experiment id based on the experiment name
  getExperimentId(experimentName) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.ML_FlOW_SERVICE_BASER_URL) + CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_EXPID.replace(CONSTANTS.PLACEHOLDER.NAME, `${experimentName}`);
    console.log('url', url);
    const headerDict = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'access-control-allow-origin': '*',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            if (_data != 200) {
              rejected(_data)
            } else {
              fulfilled(_data);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function to get the mlflow experiment id based on the experiment name
  getExperimentDetails(expName) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1)+ CONSTANTS.APIS.JOB_MGMT_SERVICE.GET_EXPID.replace(CONSTANTS.PLACEHOLDER.NAME, `${expName}`);
    console.log('url', url);
    const headerDict = {
      'userId': parent.storageService.getData().userId,
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe(
          _data => {
            console.log(_data["code"]);
            if (_data["code"]==200) {
              fulfilled(_data["data"]["experimentDetails"]);
            } else {
              rejected(_data)
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }
}
