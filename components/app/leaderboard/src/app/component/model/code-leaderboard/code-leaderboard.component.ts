/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, HostListener, Injector, Input, OnInit, Output } from '@angular/core';
import { DatePipe, Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { LeaderboardServiceService } from '../../../service/leaderboard-service.service';
import { LeaderFilterData } from '../../../data/leader-filter-data';
import { MessageInfo } from '../../../utils/message-info';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-code-leaderboard',
  templateUrl: './code-leaderboard.component.html',
  styleUrls: ['./code-leaderboard.component.scss']
})
export class CodeLeaderboardComponent implements OnInit {
  //true if leaderboard is called from modelZoo page
  @Input() leaderboardHeight: number = 0;
  // set leaderboardHeight(leaderboardHeight: number){
  //   this.model.leaderboardHeight = leaderboardHeight;
  // };
  @Input() leaderboardWidth: number = 0;

  @Input() modelFlag: boolean = false;
  @Input() exeModelName: boolean = false;
  @Input() 
  set standaloneFlag(standaloneFlag: boolean){
    this.model.standaloneFlag = standaloneFlag;
    console.log("codStandaloneFlag",this.model.standaloneFlag);
  }
  @Input() 
  set modelName(modelName: string){
    this.model.leaderDataFilter.modelName = modelName;
  }
  @Input() 
  set modality(modality: string){
    this.model.leaderDataFilter.modality = modality;
  }
  @Input() 
  set toDate(toDate: string){
    if(toDate !== '' && toDate !== undefined){
      this.model.leaderDataFilter.toDate = toDate;
    }
  }
  @Input() 
  set fromDate(fromDate: string){
    if(fromDate !== '' && fromDate !== undefined){
      this.model.leaderDataFilter.fromDate = fromDate;
    }
  }
  @Input() 
  set benchmarkName(benchmarkName: string){
    this.model.leaderDataFilter.benchmarkName = benchmarkName;
    console.log("code",this.model.leaderDataFilter.benchmarkName);
    this.onSearchClick();
  }
  todayDate = new Date();
  @Output() resetFiltersFlag = new EventEmitter<{}>();
  
  model: any = {
    standaloneFlag: true,
    pageDefault: 0,
    pageSize: 20,
    totalItems: 0,
    currentPageData: [],
    codeLeaderData:[],
    tabFlag: 0,
    leaderDataFilter: new LeaderFilterData('', '', 'codebleu' ||'',false),
    // leaderDataFilter: new LeaderFilterData(this.datePipe.transform(this.todayDate, 'yyyy-MM-dd') || '', this.datePipe.transform(this.todayDate.setDate(this.todayDate.getDate() - 60), 'yyyy-MM-dd') || ''),
    isDataLoaded: true,
    startIndex: 0,
    sortOrder:'Descending Order',
    isAscendingOrder: false,
    sortedColumn:'codebleu',
    tableWidthOffset: 700,
    isSortingClicked:false,
    resetFiltersFlag:false,
    apiError:'',
    // leaderboardHeight: 0
    }

  constructor(
    private datePipe: DatePipe,
    private location: Location,
    private route: ActivatedRoute,
    private router: Router,
    private modelService: LeaderboardServiceService,
    private injector: Injector,
    private msgInfo: MessageInfo
  ) { 
    console.log("codeLeaderboard constructed");
  }
  
  ngOnInit(): void {
    //to handle url change.
    console.log("codeLeaderboard initialized");
    const parent = this;
    parent.model.isDataLoaded = false;
    console.log("leaderfilter:",this.model.leaderDataFilter)
    const promiseLeaderBoardCount = parent.modelService.fetchLBoardBMarkDataCount(parent.model.leaderDataFilter,this.model.tabFlag);
      //0 is passed for the purpose of pagination. (fetches 20 records starting from th 0th index).
    const promiseLeaderBoardData = parent.modelService.fetchLBoardBMarkData(0, parent.model.leaderDataFilter, this.model.tabFlag);

    Promise.all([promiseLeaderBoardCount, promiseLeaderBoardData]).then(values => {
      console.log("Promises", values);
      parent.model.totalItems = values[0];
      parent.model.codeLeaderData = values[1];
      parent.getDataForCurrentPage();
    }).catch(error => {
        console.log("ErorrOninit",error);
        parent.model.errormsg = error?.error?.detail?.message;
        parent.model.totalItems = 0;
      });
  }

  getQueryParams() {
    const parent = this;
    if(!parent.model.standaloneFlag){
      this.route.queryParams.subscribe(params => {
        parent.model.leaderDataFilter.benchmarkName = params['bmname'];
        params['bmname'] = '';
      });
    }
  }

  loadLeaderData() {
    const parent = this;
    parent.model.startIndex = (parent.model.pageDefault) * parent.model.pageSize;
    parent.modelService.fetchLBoardBMarkData(parent.model.startIndex, parent.model.leaderDataFilter, this.model.tabFlag).then(value => {
      console.log("loadLeaderData", parent.model.leaderDataFilter, parent.model.startIndex, "leader data", value)
      parent.model.codeLeaderData = value;
      parent.getDataForCurrentPage();
    }).catch((error: any) => {
      console.log("errorloadData", error);
      parent.model.codeLeaderData = [];
      if(error==="apiError"){
        parent.model.apiError = error;
        parent.model.isDataLoaded = true;
      }
    });
  }

  loadLeaderCount(){
    const parent = this;
    parent.model.leaderDataFilter.isSortingClicked = true;
    parent.model.totalItems = 0;
    parent.modelService.fetchLBoardBMarkDataCount(parent.model.leaderDataFilter, this.model.tabFlag).then(value => {
      parent.model.totalItems = value;
      console.log("loadLeaderCount", parent.model.totalItems, value)
    }).catch((error: any) => {
      console.log("errorloadcount", error);
      parent.model.totalItems = 0;
    })
    parent.model.leaderDataFilter.isSortingClicked = false;
  }

  onSearchClick() {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.model.totalItems = 0;
    parent.loadLeaderCount();
    parent.loadLeaderData();
  }

  getDataForCurrentPage() {
    const parent = this;
    parent.model.currentPageData = parent.model.codeLeaderData;
    parent.model.isDataLoaded = true;
    console.log("getDataForCurrentPage", parent.model.currentPageData);
  }

  onPageChange1(page: any) {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.model.pageDefault = page;
    parent.loadLeaderData();
  }

  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.model.pageDefault = page.pageIndex;
    parent.loadLeaderData();
  }
 

  toggleSortIcon(){
    const parent = this;
    parent.model.isAscendingOrder = !parent.model.isAscendingOrder;
  }

  resetFilter(){
    console.log(this.model.leaderDataFilter);
    let today = new Date();
    let defaultfilter = new LeaderFilterData( '', '', 'codebleu',false,'','','');
    if(this.model.standaloneFlag && this.model.leaderDataFilter!==defaultfilter){
      this.model.resetFiltersFlag = true;
      this.model.leaderDataFilter = defaultfilter;
      this.onSearchClick();
      this.resetFiltersFlag.emit(this.model.resetFiltersFlag);
      console.log("resetcode",this.model.leaderDataFilter);
    }
    else if(!this.model.standaloneFlag && !this.exeModelName){
      this.model.resetFiltersFlag = true;
      this.model.leaderDataFilter = defaultfilter;
      console.log("codesend",this.model.resetFiltersFlag);
      this.onSearchClick();
      this.resetFiltersFlag.emit(this.model.resetFiltersFlag);
    }
    else if(this.exeModelName){
      this.model.resetFiltersFlag = true;
      let tempFilterData = this.model.leaderDataFilter.modelName;
      this.model.leaderDataFilter = defaultfilter;
      this.model.leaderDataFilter.modelName = tempFilterData;
      this.onSearchClick();
      this.resetFiltersFlag.emit(this.model.resetFiltersFlag);
    }
  }

  //sorting according to metrics
  updateMetricName(metricName: string, isSortingClicked: boolean){
    const parent = this;
      if(parent.model.leaderDataFilter.metricName !== metricName){
        parent.model.sortOrder = '';
        parent.model.sortedColumn = '';
        parent.model.isAscendingOrder = false;
      }
      parent.toggleSortIcon();
      parent.model.leaderDataFilter.metricName = metricName;
      parent.model.leaderDataFilter.isSortingClicked = true;

      if (parent.model.sortOrder === 'Descending Order') {
        parent.model.sortOrder = 'Ascending Order';
        parent.model.sortedColumn = parent.model.leaderDataFilter.metricName;
        parent.loadLeaderData();
      } else if(parent.model.sortOrder === '' || parent.model.sortOrder === 'Ascending Order'){
        parent.model.sortOrder = 'Descending Order';
        parent.model.sortedColumn = parent.model.leaderDataFilter.metricName;
        parent.loadLeaderData();
      }
      parent.model.leaderDataFilter.isSortingClicked = false;
  }

  getMessage(msgCode: any): string{
    const parent = this;
    return parent.msgInfo.getMessage(msgCode)
  }
}