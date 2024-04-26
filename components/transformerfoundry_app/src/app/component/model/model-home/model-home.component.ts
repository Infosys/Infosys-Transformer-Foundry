/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit } from '@angular/core';
import { DatePipe, Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ModelService } from 'src/app/services/models.service';
import { LeaderFilterData } from 'src/app/data/leader-filter-data';
import { DataStorageService } from "src/app/services/data-storage.service";
import { MatTabChangeEvent } from "@angular/material/tabs";

@Component({
  selector: 'app-model-home',
  templateUrl: './model-home.component.html',
  styleUrls: ['./model-home.component.scss']
})
export class ModelHomeComponent implements OnInit {

  todayDate = new Date();
  constructor(
    private datePipe: DatePipe,
    private location: Location,
    private route: ActivatedRoute,
    private router: Router,
    private modelService: ModelService,
    private storageService: DataStorageService) { }

  model: any = {
    isDataLoaded: false,
    modelListData: [],
    leaderDataCount: 0,
    leaderData: [],
    modelCount: 0,
    errormsg: '',
    leaderDataFilter: new LeaderFilterData(this.datePipe.transform(this.todayDate, 'yyyy-MM-dd'), this.datePipe.transform(this.todayDate.setDate(this.todayDate.getDate() - 30), 'yyyy-MM-dd')),
    selectedTabIndex: 0,
    selectedBenchmarkData:{},
  }

  // showLeaderBoard: boolean;
  checkIfModelZoo() {
    const currentUrl = this.location.path()
    if (currentUrl.includes("modelZoo")) {
      return true
    }
    return false
  }

  ngOnInit(): void {
    //to handle url change.
    this.route.paramMap.subscribe(params => {
      const parent = this;
      const pId = !parent.checkIfModelZoo() ? params.get('pid') : '';
      parent.model.selectedTabIndex = (parent.storageService.getData()).modelZooTabIndex;
      const promiseModelList = parent.modelService.getModelList(pId);
      const promiseLeaderboard = parent.getQueryParams();

      Promise.all([promiseModelList,promiseLeaderboard]).then(values => {
        console.log("Promises", values);
        parent.model.modelListData = values[0];
        parent.model.modelCount = parent.model.modelListData.length;
        parent.model.isDataLoaded = true;
      }).catch(error => {
        console.log(error);
        parent.model.errormsg = error?.error?.detail?.message;
        parent.model.modelListData = [];
        parent.model.isDataLoaded = true;
      });
    });
    
  }

  //get the query params from the url for fetching the benchmark of particular model
  getQueryParams() {
    const parent = this;
    parent.route.queryParamMap.subscribe(queryParams => {
      console.log("queryParams:", queryParams['params']);
      if(Object.keys(queryParams['params']).length > 1){
        if (queryParams['params']['bm'] !== '' || queryParams['params']['bm'] !== undefined && queryParams['params']['mdl'] !== ''||queryParams['params']['mdl'] !== undefined && queryParams['params']['td'] !== ''||queryParams['params']['td'] !== undefined&& queryParams['params']['fd'] !== ''||queryParams['params']['fd'] !== undefined) {
          parent.model.selectedTabIndex = 1;
          this.setTabIndex(1);
          localStorage.setItem('modelZooTabIndex','1');
          parent.model.selectedBenchmarkData ={"benchmarkName":queryParams['params']['bm'],"modality":queryParams['params']['mdl'],"toDate":queryParams['params']['td'],"fromDate":queryParams['params']['fd']};
        }
      }
    });
  }

  //function to reset the filter
  onResetFilters(data:any){
    const parent = this;
    console.log('receivedparentResetFlag',data);
    if(data){
      parent.setQueryParams();
    }
  }

  //function to handle the tab change
  onTabChange(event: MatTabChangeEvent) {
    this.setTabIndex(event.index);
  }
  
  //function to set the query params
  private setQueryParams(){
    const parent = this;
    function getUrl(url: string): string {
      let urlSplit = url.split('#');
      urlSplit = urlSplit[1]?.split('?');
      return urlSplit[0];
    }
    let url:any = (new URL(window.location.href)).href;
    url = getUrl(url);
    console.log("url:",url);
    this.location.replaceState(url);
    parent.model.selectedBenchmarkData = {};
  }

  //function to set the tab index
  private setTabIndex(index) {
    const parent = this;
    const storedData = parent.storageService.getData();
    storedData.modelZooTabIndex = index;
    parent.storageService.setData(storedData);
  }
}
