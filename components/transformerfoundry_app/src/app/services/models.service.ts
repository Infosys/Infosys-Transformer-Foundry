/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ConfigDataHelper } from '../utils/config-data-helper';
import { CONSTANTS } from '../common/constants';
import { DataStorageService } from './data-storage.service';

@Injectable({
  providedIn: 'root'
})
export class ModelService {

  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper, private storageService: DataStorageService) { }

  //this fn gets the list of models for a particular project by passing projectId if any.
  getModelList(projectId?) {
    const parent = this;
    const tsGlobalProjectID = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TS_GLBL_PROJECT_ID);
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.AI_CLD_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${tsGlobalProjectID}`);
    let userId = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TS_GLBL_PROJECT_ADMIN_ID)
    if (projectId) {
      url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.AI_CLD_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${projectId}`);
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

  //this fn gets a particular model details by passing userId, modelId and version.
  getModelData(modelId, version) {
    const parent = this;
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.AI_CLD_MGMT_SERVICE_BASER_URL) + CONSTANTS.APIS.MODEL_MGMT_SERVICE.GET_MODEL_DETAILS.replace(CONSTANTS.PLACEHOLDER.MID, `${modelId}`).replace(CONSTANTS.PLACEHOLDER.MVER, `${version}`);
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

}
