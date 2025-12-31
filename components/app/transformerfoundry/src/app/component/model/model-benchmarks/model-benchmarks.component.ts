/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CONSTANTS } from "src/app/common/constants";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { ModelService } from 'src/app/services/models.service';
import { DataStorageService } from 'src/app/services/data-storage.service';

@Component({
  selector: 'app-model-benchmarks',
  templateUrl: './model-benchmarks.component.html',
  styleUrls: ['./model-benchmarks.component.scss']
})
export class ModelBenchmarksComponent implements OnInit {

  constructor(
    private route:ActivatedRoute,
    private router:Router,
    public configDataHelper: ConfigDataHelper,
    private modelService: ModelService,
    private storageService: DataStorageService
  ) { }

  // model object to bind with UI
  model: any = {
    standaloneFlag:false,
    l1RowLeaderboardEnabled: false,
    l1RowBenchmarkEnabled: true,
    redirectedViewPath:'',
    benchmarkName:'',
    modality:'',
    dynamicOffset:{},
    pId: '',
    modelListData: [],
    userId: '',
    leaderboardMfeUrl: this.configDataHelper.getValue(CONSTANTS.CONFIG.LEADERBOARD_MFE_URL),
    // leaderboardMfeUrl: 'http://localhost:4102/mfe-tf-leaderboard.js?v=', // give congfig path/enable when run from local
  }

  // on init fetch the benchmark js file.
  ngOnInit(): void {
    const parent = this;
    parent.setDynamicOffset();
    //Used for browser cache busting for leaderboard mfe 
    let cacheBuster = new Date().toISOString().replace(/[-:.T]/g, '');
    parent.model.leaderboardMfeUrl = parent.model.leaderboardMfeUrl + cacheBuster;
    console.log("leaderboardMfeUrl", parent.model.leaderboardMfeUrl);
    parent.getModelDetails();
    //retrieving the user id from storage service
    parent.model.userId = parent.storageService.getData().userId;
    console.log("userId:", parent.model.userId);
  }

  //retrieving the list of models for that project id and global project
  getModelDetails(){
    const parent = this;
    parent.route.paramMap.subscribe(params => {
      parent.model.pId = params.get('pid');
      console.log("pid:", params);
    });
    const promise1 = parent.modelService.getModelList(parent.model.pId);
    const promise2 = parent.modelService.getModelList();
    Promise.all([promise1, promise2]).then(values => {
      parent.model.modelListData = values[0];
      parent.model.modelListData =parent.model.modelListData.concat(values[1]);
      console.log("modelListData",parent.model.modelListData);
    }).catch(error => {
      parent.model.modelListData = [];
    });
  }

  // setting the dynamic offset values
  setDynamicOffset(){
    this.model.dynamicOffset={
      jobOffset: 252, 
      jobSubmitOffset: 207,
      jobListOffset: 205,
      jobWOffset: 213,
      jobSubmitWOffset: 30,
      jobListWOffset: 33,
    };
  }

  // setting the benchmark data
  onSelectedBenchmarkData(data: any) {
    const parent = this;
    parent.setQueryParams(data);
  }

  // setting the query params for the selected benchmark
  private setQueryParams(data:any){
    console.log("datadata",data);
    const parent = this;
    let newParams = {};
    function removeQueryParams(url: string): string {
      let urlSplit = url.split('#');
      urlSplit = urlSplit[1]?.split('?');
      return urlSplit[0];
    }

    let url:any = (new URL(window.location.href)).href;
    url = url.replace('benchmarks', 'modelZoo');
    url = removeQueryParams(url);
    console.log("url:",url);

    parent.route.queryParamMap.subscribe(queryParams => {
      newParams = {...queryParams['params'], bm: data.detail.benchmarkName, mdl: data.detail.modality, td:data.detail.toDate, fd:data.detail.fromDate};
      console.log("params:", newParams);
      parent.router.navigate([url], { queryParams: newParams });
    });
  }
}
