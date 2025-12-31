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

@Injectable({
  providedIn: 'root'
})
export class LeaderboardServiceService {

  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper) { }

  //fetch leaderboard data
  fetchLBoardBMarkData(from: any, leaderDataFilterValue: any, tab: any) {
    const parent = this
    console.log("tab", tab)
    var url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.LEADERBOARD_SERVICE_BASER_URL) + CONSTANTS.APIS.LEADERBOARD_SERVICE.POST_BENCHMARK;
    console.log("tab", tab)
    if (tab === 0) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.CODE)
    }
    else if (tab === 1) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.TEXT)
    }
    else if (tab === 2) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.EMBEDDING)
    }
    else if (tab === 3) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.RAG)
    }
    const headerDict = {
      "Accept": "application/json",
      "Content-Type": "application/json",
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };

    var leaderDataFilter = Object.assign({}, leaderDataFilterValue);
    return new Promise((fulfilled, rejected) => {
      var body = JSON.parse(`{
      "query": {
        "bool": {
          "must": [ ]
        }
      },
      "from":${from},
      "size":20
    }`)

      body = parent.prepareQueryForLeaderBoardData(body, leaderDataFilter.modelName, leaderDataFilter.datasetName, leaderDataFilter.metricName, leaderDataFilter.isSortingClicked, leaderDataFilter.benchmarkName, leaderDataFilter.fromDate, leaderDataFilter.toDate);
      this.httpClient.post(url, body, requestOptions)
      .subscribe(
        (data: any) => {
          console.log("BenchMark-POST", data["response"]["hits"]["hits"], "body", body);
          if (data["response"]["hits"]["hits"]) {
            fulfilled(data["response"]["hits"]["hits"]);
          } else {
            rejected(true);
          }
        },
        (error: any) => {
          console.error("API request failed:", error);
          rejected("apiError");
        }
      );
    })
  }

  //fetch leaderboard data count
  fetchLBoardBMarkDataCount(leaderDataFilterValue: any, tab: any) {
    const parent = this
    var url = parent.configDataHelper.getValue(CONSTANTS.CONFIG.LEADERBOARD_SERVICE_BASER_URL) + CONSTANTS.APIS.LEADERBOARD_SERVICE.POST_BENCHMARK_COUNT
    console.log("tab", tab)
    if (tab === 0) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.CODE)
    }
    else if (tab === 1) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.TEXT)
    }
    else if (tab === 2) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.EMBEDDING)
    }
    else if (tab === 3) {
      url = url.replace(CONSTANTS.PLACEHOLDER.REQUEST, CONSTANTS.BENCHMARK_MODALITIES.RAG)
    }
    const headerDict = {
      "Accept": "application/json",
      "Content-Type": "application/json",
    }
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };

    var leaderDataFilter = Object.assign({}, leaderDataFilterValue);
    return new Promise((fulfilled, rejected) => {
      var body = JSON.parse(`{
          "query": {
            "bool": {
              "must": [ ]
            }
          }
        }`)
      body = parent.prepareQueryForLeaderBoardData(body, leaderDataFilter.modelName, leaderDataFilter.datasetName, leaderDataFilter.metricName = '', leaderDataFilter.isSortingClicked, leaderDataFilter.benchmarkName, leaderDataFilter.fromDate, leaderDataFilter.toDate);
      console.log("URL_getcount", URL);
      this.httpClient.post(url, body, requestOptions)
        .subscribe((data: any) => {
          if (data) {
            console.log(data)
            fulfilled(data["response"]["count"]);
          }
          else
            rejected(true)
            console.log("rejected data true");
        })
    })
  }

  //for sorting via metric column
  private previousMetricName: string = '';
  private defaultSortOrder = "desc";

  //prepare query for leaderboard data
  private prepareQueryForLeaderBoardData(body: any, modelName?: string, datasetName?: string, metricName?: string, isSortingClicked?: boolean, benchmarkName?: string, fromDate?: string, toDate?: string) {
    console.log(fromDate, toDate, typeof (fromDate), typeof (toDate))
    if (fromDate !== '' && toDate !== '') {
      const mustObject: any = {
        "range": {
          "@timestamp": {
          }
        }
      };
      mustObject['range']['@timestamp']['gte'] = fromDate;
      mustObject['range']['@timestamp']['lte'] = toDate;
      body['query']['bool']['must'].push(mustObject);
    }
    if (modelName !== undefined && modelName !== '' && modelName !== null) {
      const mustObject = {
        "bool": {
          "should": [
            {
              "regexp": {
                "model": {
                  "value": ".*" + modelName + ".*",
                  "case_insensitive": true
                }
              }
            },
            {
              "match_phrase": {
                "model": {
                  "query": modelName
                }
              }
            }
          ]
        }
      };
      body['query']['bool']['must'].push(mustObject);
    }
    if (benchmarkName !== undefined && benchmarkName !== '' && benchmarkName !== null) {
      const mustObject = {
        "bool": {
          "should": [
            {
              "regexp": {
                "run_name": {
                  "value": ".*" + benchmarkName + ".*",
                  "case_insensitive": true
                }
              }
            },
            {
              "match_phrase": {
                "run_name": {
                  "query": benchmarkName
                }
              }
            }
          ]
        }
      };
      body['query']['bool']['must'].push(mustObject);
    }
    if (datasetName !== undefined && datasetName !== '' && datasetName !== null) {
      const mustObject = {
        "bool": {
          "should": [
            {
              "regexp": {
                "dataset": {
                  "value": ".*" + datasetName + ".*",
                  "case_insensitive": true
                }
              }
            },
            {
              "match_phrase": {
                "dataset": {
                  "query": datasetName
                }
              }
            }
          ]
        }
      };
      body['query']['bool']['must'].push(mustObject);
    }

    if (metricName !== '' && metricName !== undefined && metricName !== null) {
      if (isSortingClicked) {
        if (metricName === this.previousMetricName) {
          this.defaultSortOrder = this.defaultSortOrder === "asc" ? "desc" : "asc";
        } else {
          this.defaultSortOrder = "desc";
          this.previousMetricName = metricName;
        }
      } else if (!this.previousMetricName) {
        this.defaultSortOrder = "desc";
        this.previousMetricName = metricName;
      }
      body['sort'] = [
        {
          [metricName as string]: {
            "order": this.defaultSortOrder,
            "unmapped_type": "long"
          }
        }
      ];
    }

    return body;
  }
}
