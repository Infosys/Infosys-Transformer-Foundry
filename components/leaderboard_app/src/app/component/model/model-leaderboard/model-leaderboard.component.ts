/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, ElementRef, EventEmitter, HostListener, Injector, Input, OnInit, Output} from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-model-leaderboard',
  templateUrl: './model-leaderboard.component.html',
  styleUrls: ['./model-leaderboard.component.scss']
})
export class ModelLeaderboardComponent implements OnInit {
  @Input() 
  set standaloneFlag(standaloneFlag: boolean){
    this.model.standaloneFlag = standaloneFlag;
    console.log("homestandaloneFlag",this.model.standaloneFlag);
    this.resizeComponent();
    this.setL1TabIndex();
  }
  @Input() 
  set modelName(modelName: string){
    this.model.modelName = modelName;
    console.log("modelName",this.model.modelName);
  }
  @Input()
  set l1RowEnabled(l1RowEnabled:boolean){
    console.log("l1l1l1",l1RowEnabled);
    this.model.l1RowEnabled = l1RowEnabled;
    console.log("l1RowEnabled",this.model.l1RowEnabled);
    this.hideL1Labels();
  }
  @Input()
  set l2RowEnabled(l2RowEnabled: boolean){
    console.log("l2l2l2",l2RowEnabled);
    this.model.l2RowEnabled = l2RowEnabled;
    console.log("l2RowEnabled",this.model.l2RowEnabled);
  }
  @Input()
  set l1RowLeaderboardEnabled(l1RowLeaderboardEnabled:boolean){
    this.model.l1RowLeaderboardEnabled = l1RowLeaderboardEnabled;
    console.log("l1RowLeaderboardEnabled",this.model.l1RowLeaderboardEnabled);
    this.setL1TabIndex();
  }
  @Input()
  set l1RowBenchmarkEnabled(l1RowBenchmarkEnabled:boolean){
    this.model.l1RowBenchmarkEnabled = l1RowBenchmarkEnabled;
    console.log("l1RowBenchmarkEnabled",this.model.l1RowBenchmarkEnabled);
    this.setL1TabIndex();
  }
  @Input() 
  set toDate(toDate: string){
    if(toDate !== '' && toDate !== undefined){
      this.model.toDate = toDate;
    }
  }
  @Input() 
  set fromDate(fromDate: string){
    if(fromDate !== '' && fromDate !== undefined){
      this.model.fromDate = fromDate;
    }
  }
  @Input()
  set benchmarkName(benchmarkName:any){
    if(benchmarkName!==''||benchmarkName!==undefined){
      this.model.benchmarkName = benchmarkName; 
    }
  }
  @Input()
  set modality(modality:any){
    console.log("modallqwe",modality);
    if(modality!==''||modality!==undefined){
      this.model.modality = modality; 
      console.log("modalityset",this.model.modality);
    }
    if(!this.model.standaloneFlag && this.model.selectedL2TabIndex===0 ){
      console.log("modallll",this.model.modality);
      this.switchTabsOnModality(this.model.modality);
    }
  }
  @Input()
  set exeModelName(exeModelName:any){
    this.model.exeModelName = exeModelName; 
    console.log("exeModelHome",this.model.exeModelName);
  }
  @Input()
  set dynamicOffset(dynamicOffset:any){
    this.model.dynamicOffset = dynamicOffset; 
    console.log("dynamicOffset",this.model.dynamicOffset);
    this.onResize();
  }
  @Output() selectedBenchmarkData = new EventEmitter<{}>();
  @Output() resetFiltersFlag = new EventEmitter<{}>();

  model: any = {
    standaloneFlag:true,
    modelName:'',
    l1RowEnabled:true,
    l2RowEnabled:true,
    l1RowLeaderboardEnabled:true,
    l1RowBenchmarkEnabled:true,
    modality:'',
    benchmarkName:'',
    toDate:'',
    fromDate:'',
    exeModelName:false,
    dynamicOffset:{},
    selectedL1TabIndex: 0,
    selectedL2TabIndex: 0,
    noDataMsg:false,
  }

  //standalone-app
  leaderboardOffset = 310; //leaderboard
  jobOffset = 213;//265 //job-tab
  jobSubmitOffset = 178; // job-submit-tab
  jobListOffset = 147; //job-list-tab

  leaderboardWOffset = 33; //leaderboard
  jobWOffset = 213;//265 //job-tab
  jobSubmitWOffset = 30; // job-submit-tab
  jobListWOffset = 33; //job-list-tab

  constructor(
    private location: Location,
    private route: ActivatedRoute,
  ) { }
  
  //resize components, and retrieve parameters from the url
  ngOnInit(): void {
    const parent = this;
    //to handle url change.
    this.route.paramMap.subscribe(params => {
      const parent = this;
      const pId = !parent.checkIfModelZoo() ? params.get('pid') : '';
      console.log("BBBB-", pId);
    });
    parent.resizeComponent();
  }

  //show the tabs based on the flag
  ngAfterViewInit(){
    if(!this.model.l2RowEnabled){
    this.hideL2Labels();
    console.log("afterview");
    }
  }

  //check if the app is running in standalone or foundry-integration mode
  checkIfStandalone() {
    const parent = this;
    const urlCheck = window.location.hash;
    if(!urlCheck){
      parent.model.standaloneFlag = true;
      console.log(parent.model.standaloneFlag);
    }
    parent.setL1TabIndex();
  }

  //set the tab index based on the flag
  setL1TabIndex(){
    if(this.model.standaloneFlag){
      this.model.selectedL1TabIndex = 0;
    }
    else{
      if(this.model.l1RowLeaderboardEnabled){
        this.model.selectedL1TabIndex = 0;
      }
      else{
        this.model.selectedL1TabIndex = 1;
      }
    }
  }

  //switch the tabs based on the modality
  switchTabsOnModality(modality:string) {
    switch (modality) {
      case 'code':
        this.model.selectedL1TabIndex = 0;
        this.model.selectedL2TabIndex = 0;
        this.model.tabIndex = 4;
        console.log("codeeee");
        break;
      case 'text':
        this.model.selectedL1TabIndex = 0;
        this.model.selectedL2TabIndex = 1;
        this.model.tabIndex = 3;
        console.log("textttt");
        break;
      case 'embedding':
        this.model.selectedL1TabIndex = 0;
        this.model.selectedL2TabIndex = 2;
        this.model.tabIndex = 4;
        console.log("embedddd");
        break;
      case '' || 'NA':
        this.model.selectedL1TabIndex = 0;
        this.model.selectedL2TabIndex = 0;
        this.model.noDataMsg = true;
        console.log("NoDataaaa");
        break;
      default:
        break;
    }
    console.log("switch");
  }

  //hide the labels based on the flag
  hideL1Labels() {
    console.log("l1lab",this.model.l1RowEnabled);
    const tabLabels = document.querySelectorAll('.mat-tab-labels');
    console.log("labels1",tabLabels);
    if (tabLabels.length > 0 && !this.model.l1RowEnabled) {
      const tabLabel = tabLabels[1] as HTMLElement;
      tabLabel.style.position = this.model.standaloneFlag? 'static':'absolute';
    }
  }

  //hide the labels based on the flag
  hideL2Labels() {
    console.log("l2lab",this.model.l2RowEnabled);
    const tabLabels = document.querySelectorAll('.mat-tab-labels');
    console.log("labels2",tabLabels);
    if (tabLabels.length > 0 && !this.model.l2RowEnabled) {
      const tabLabel = tabLabels[2] as HTMLElement;
      tabLabel.style.position = this.model.standaloneFlag? 'static':'absolute';
      console.log("postpost",tabLabel.style.position);
    }
  }

  //check if the app is called from the modelZoo/ model details
  checkIfModelZoo() {
    const currentUrl = this.location.path()
    console.log("currentUrl", currentUrl);
    if (currentUrl.includes("modelZoo")) {
      return true
    }
    return false
  }

  //emit the selected benchmark data
  onSelectedBenchmarkData(data:any) {
    const parent = this;
    console.log("flagflag",parent.model.standaloneFlag);
      parent.model.modality = parent.model.standaloneFlag? data.modality:'';
      parent.model.benchmarkName = parent.model.standaloneFlag? data.benchmarkName:'';
      parent.model.toDate = parent.model.standaloneFlag? data.toDate:'';
      parent.model.fromDate = parent.model.standaloneFlag? data.fromDate:'';
      console.log('mfehomeModality',parent.model.modality,'mfehomeBenchmarkName',parent.model.benchmarkName);
      parent.switchTabsOnModality(parent.model.standaloneFlag? data.modality:'');
      parent.selectedBenchmarkData.emit(data);
  }

  //emit the reset filters flag
  onResetFilters(data:any){
    console.log('receivedResetFlag',data)
    this.resetFiltersFlag.emit(data);
    if(data && !this.model.exeModelName){
      this.model.benchmarkName = '';
      this.model.modelName = '';
      console.log("modelnull");
    }
    else if(data && this.model.exeModelName){
      this.model.benchmarkName = '';
      console.log("modelnull2");
    }
  }

  //resize the component based on the window size
  @HostListener('window:resize', ['$event'])
  onResize() {
    this.resizeComponent();
    console.log("resizeHotListner");
  }

  //resize the component based on the window size
  private resizeComponent() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth; //1272
    console.log(windowHeight,windowWidth);

    //standalone-app
    if(parent.model.standaloneFlag){
    parent.model.leaderboardHeight = windowHeight - parent.leaderboardOffset; //leaderboard
    parent.model.jobHeight = windowHeight - parent.jobOffset; //benchmark-tab
    parent.model.submitHeight = windowHeight - parent.jobSubmitOffset; //submit-tab 
    parent.model.listHeight = windowHeight - parent.jobListOffset; //list-tab

    parent.model.leaderboardWidth = windowWidth - parent.leaderboardWOffset; //leaderboard
    parent.model.jobWidth = windowWidth - parent.jobWOffset; //benchmark-tab
    parent.model.submitWidth = windowWidth - parent.jobSubmitWOffset; //submit-tab 
    parent.model.listWidth = windowWidth - parent.jobListWOffset; //list-tab
    }
    //foundry-integration
      else{
      parent.model.leaderboardHeight = windowHeight - parent.model.dynamicOffset.leaderboardOffset; 
      parent.model.jobHeight = windowHeight - parent.model.dynamicOffset.jobOffset; 
      parent.model.submitHeight = windowHeight - parent.model.dynamicOffset.jobSubmitOffset; 
      parent.model.listHeight = windowHeight - parent.model.dynamicOffset.jobListOffset;

      parent.model.leaderboardWidth = windowWidth - parent.model.dynamicOffset.leaderboardWOffset; 
      parent.model.jobWidth = windowWidth - parent.model.dynamicOffset.jobWOffset; 
      parent.model.submitWidth = windowWidth - parent.model.dynamicOffset.jobSubmitWOffset; 
      parent.model.listWidth = windowWidth - parent.model.dynamicOffset.jobListWOffset; 

      }
    // }
  }
}