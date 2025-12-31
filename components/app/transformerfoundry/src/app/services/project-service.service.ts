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
import { ProjectDetailsData } from '../data/project-details-data';
import { MessageInfo } from '../utils/message-info';

@Injectable({
  providedIn: 'root'
})
export class ProjectServiceService {

  private projectData = undefined
  
  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper,
    private storageService: DataStorageService, private msgInfo: MessageInfo) { }

  private currentTenatData = undefined;

  // function to get tenant details
  getTenantDetail() {
    const parent = this;
    if (parent.currentTenatData) {
      return new Promise(function (fulfilled, rejected) {
        fulfilled(parent.currentTenatData);
    });
    } else {
      const tenantID = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TENANT_ID)
      const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
        CONSTANTS.APIS.PRJCT_MGMT_SERVICE.GET_TENANT_DETAIL.replace(CONSTANTS.PLACEHOLDER.ID, `${tenantID}`);
      const headerDict = {
        'accept': 'application/json',
        'userId': parent.storageService.getData().userId,
      }
      const requestOptions = {
        headers: new HttpHeaders(headerDict)
      };
      return new Promise(function (fulfilled, rejected) {
        parent.httpClient.get(url, requestOptions)
          .subscribe(
            _data => {
              parent.currentTenatData = (_data['code'] == 200) ? _data['data']['tenant'] : undefined;
              fulfilled(parent.currentTenatData);
            },
            _error => {
              if (_error['status'] == 422) {
                parent.currentTenatData = undefined;
                fulfilled(parent.currentTenatData)
              }
              rejected(_error);
            }
          );
      });
    }
  }

  // function to get project data list
  getProjectDataList() {
    const parent = this;
    const tenantID = parent.configDataHelper.getValue(CONSTANTS.CONFIG.TENANT_ID)
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.PRJCT_MGMT_SERVICE.GET_PRJCT_LIST.replace(CONSTANTS.PLACEHOLDER.ID, `${tenantID}`);
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId,
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
              _data['data']['projects'] = _data['data']['projects'].filter(x=>x['id']!==parent.configDataHelper.getValue(CONSTANTS.CONFIG.TS_GLBL_PROJECT_ID));
              fulfilled(_data['data']['projects']);
            }
          },
          _error => {
            if (_error['status'] == 422) {
              fulfilled({message:parent.msgInfo.getMessage(111)});
            }
            rejected(_error);
          }
        );
    });
  }

  // function to create project details
  createProjectDetails(projectDetails: ProjectDetailsData) {
    const parent = this;
    const body = JSON.stringify(projectDetails);
    const headerDict = {
      'Accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.PRJCT_MGMT_SERVICE.POST_PRJCT_DATA;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, projectDetails, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 201) {
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

  // function to get project details by id
  getProjectDetailsByID(projectId) {
    const parent = this;
    if (parent.projectData && parent.projectData.id == projectId) {
      return new Promise(function (fulfilled, rejected) {
        fulfilled(parent.projectData);
      });
    } else {
      const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
        CONSTANTS.APIS.PRJCT_MGMT_SERVICE.PRJCT_DETAILS.replace(CONSTANTS.PLACEHOLDER.ID, `${projectId}`);
      const headerDict = {
        'accept': 'application/json',
        'userId': parent.storageService.getData().userId,
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
                parent.projectData = (_data['code'] == 200) ? _data['data']['project'] : undefined;
                fulfilled(parent.projectData);
              }
            },
            _error => {
              rejected(_error);
            }
          );
      });
    }
  }

  // function to update project details
  updateProjectDetails(projectDetails: ProjectDetailsData) {
    const parent = this;
    const body = JSON.stringify(projectDetails);
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId,
      'Content-Type': 'application/json',
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.PRJCT_MGMT_SERVICE.POST_PRJCT_DATA;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.put(url, projectDetails, requestOptions)
        .subscribe(
          _data => {
            if (_data['code'] != 201) {
              rejected(_data)
            } else {
              parent.projectData = _data['data']
              fulfilled(_data['data']);
            }
          },
          _error => {
            rejected(_error);
          }
        );
    });
  }

  // function to delete project
  deleteProject(projectId) {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.storageService.getData().userId,
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_MGMT_SERVICE_BASER_URL) +
      CONSTANTS.APIS.PRJCT_MGMT_SERVICE.PRJCT_DETAILS.replace(CONSTANTS.PLACEHOLDER.ID, `${projectId}`);;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.delete(url, requestOptions)
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
}
