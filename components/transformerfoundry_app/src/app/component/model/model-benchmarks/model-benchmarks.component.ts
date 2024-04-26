/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CONSTANTS } from "src/app/common/constants";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { ModelService } from 'src/app/services/models.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
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
    private modalService: NgbModal,
    private storageService: DataStorageService
  ) { }

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
  }

  //Used for browser cache busting for leaderboard mfe and to set the dynamic offset
  ngOnInit(): void {
    const parent = this;
    parent.setDynamicOffset();
    let cacheBuster = new Date().toISOString().replace(/[-:.T]/g, '');
    parent.model.leaderboardMfeUrl = parent.model.leaderboardMfeUrl + cacheBuster;
  }

  //set the dynamic offset for the leaderboard mfe
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

  //onSelectedBenchmarkData method used to set the query params for the benchmark
  onSelectedBenchmarkData(data: any) {
    const parent = this;
    parent.setQueryParams(data);
  }

  //open pop up for the benchmark when integrated 
  open(content) {
    console.log("content:", content)
    const parent = this;
    parent.modalService
      .open(content, {
        ariaLabelledBy: "modalTitle",
        windowClass: "web_custom_modal tf_modal-sm",
      })
      .result.then(
        () => {
          document
            .getElementsByTagName("html")[0]
            .classList.remove("tf_modaloverflow");
        },
        () => {
          document
            .getElementsByTagName("html")[0]
            .classList.remove("tf_modaloverflow");
        }
      );
    document.getElementsByTagName("html")[0].classList.add("tf_modaloverflow");
  }

  //set the query params for the benchmark
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
