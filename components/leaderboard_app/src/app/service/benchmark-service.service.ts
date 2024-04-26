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
import { BenchmarkData } from '../data/benchmark-data';

@Injectable({
  providedIn: 'root'
})
export class BenchmarkServiceService {

  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper) { }

  //create benchmark
  createBenchmark(benchmarkData: BenchmarkData, userId?:any) {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      "userId": parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID),
    }

    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.BENCHMARK_SERVICE_BASER_URL) + CONSTANTS.APIS.BENCHMARK_SERVICE.POST_BENCHMARK_SUBMIT;

    console.log(url);
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    console.log(requestOptions, headerDict);

    benchmarkData = JSON.parse(JSON.stringify(benchmarkData));
    //concatenate s3:// with model path of each model at the start
    benchmarkData.configuration.model.forEach((model: any) => {
      model.modelPathorId = "s3://" + model.modelPathorId;
    });
    //concatenate s3:// with storage uri 
    benchmarkData.configuration.dataStorage.uri = 's3://' + benchmarkData.configuration.dataStorage.uri;
    benchmarkData.resourceConfig.volume.mountPath = "/" + benchmarkData.resourceConfig.volume.mountPath;
    console.log(JSON.stringify(benchmarkData));

    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, benchmarkData, requestOptions)
        .subscribe({
          next: (data: any) => {
            if (data['code'] != 200) {
              rejected(data)
            } else {
              fulfilled(data);
            }
          },
          error: error => {
            rejected(error);
          }
        });
    });
  }

  //get benchmark metadata
  getBenchmarkMetaDataList(benchmarkType: string, metadataType: string) {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID),
    }  
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.BENCHMARK_SERVICE_BASER_URL) + CONSTANTS.APIS.BENCHMARK_SERVICE.GET_BENCHMARK_METADATA.replace(CONSTANTS.PLACEHOLDER.BENCHMARK, benchmarkType).replace(CONSTANTS.PLACEHOLDER.METADATA, metadataType);

    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe({
          next: (_data: any) => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']);
            }
          },
          error: _error => {
            rejected(_error);
          }
        });
    });


  }

  //get benchmark datasets
  getBenchmarkDatasets(benchmarkType: string, task: string) {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID),
    }  
    let url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.BENCHMARK_SERVICE_BASER_URL) + CONSTANTS.APIS.BENCHMARK_SERVICE.GET_BENCHMARK_DATASET.replace(CONSTANTS.PLACEHOLDER.BENCHMARK, benchmarkType).replace(CONSTANTS.PLACEHOLDER.METADATA, task);

    const requestOptions = {
      headers: new HttpHeaders(headerDict)
    };
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get(url, requestOptions)
        .subscribe({
          next: (_data: any) => {
            if (_data['code'] != 200) {
              rejected(_data)
            } else {
              fulfilled(_data['data']);
            }
          },
          error: _error => {
            rejected(_error);
          }
        });
    });


  }

  //get benchmark list
  getBenchmarkList() {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID),
    }  
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.BENCHMARK_SERVICE_BASER_URL) + CONSTANTS.APIS.BENCHMARK_SERVICE.GET_BENCHMARK_LIST.replace(CONSTANTS.PLACEHOLDER.ID, parent.configDataHelper.getValue(CONSTANTS.CONFIG.PROJECT_ID));
    console.log(url, "url obtained from constants.ts and sent to getBenchmarkList()");
    return new Promise(function (fulfilled, rejected) {
      console.log("header", requestOptions);
      parent.httpClient.get(url, requestOptions)
        .subscribe({
          next: (data: any) => {
            if (data["code"] != 200) {
              rejected(data)
            } else {
              fulfilled(data['data']);
            }
          },
          error: (error: any) => {
            rejected(error);
          }
        });
    });
  }

  //get benchmark status
  getBenchmarkStatus(executionid: string) {
    const parent = this;
    const headerDict = {
      'accept': 'application/json',
      'userId': parent.configDataHelper.getValue(CONSTANTS.CONFIG.USER_ID),
    }

    const url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.BENCHMARK_SERVICE_BASER_URL) + CONSTANTS.APIS.BENCHMARK_SERVICE.GET_BENCHMARK_STATUS.replace(CONSTANTS.PLACEHOLDER.ID, `${executionid}`);
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };
    return new Promise(function (fulfilled, rejected) {
      console.log("requestOptions",requestOptions)
      parent.httpClient.get(url, requestOptions)
        .subscribe({
          next: (_data: any) => {
            fulfilled(_data['data']);
          },
          error: (_error: any) => {
            rejected(_error);
          }
        });
    });
  }
}
