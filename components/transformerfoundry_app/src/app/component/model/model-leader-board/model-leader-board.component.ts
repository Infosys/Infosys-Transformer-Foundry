/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ModelService } from 'src/app/services/models.service';
import { LeaderFilterData } from 'src/app/data/leader-filter-data';
import { Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { CONSTANTS } from "src/app/common/constants";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";


@Component({
  selector: 'app-model-leader-board',
  templateUrl: './model-leader-board.component.html',
  styleUrls: ['./model-leader-board.component.scss']
})
export class ModelLeaderBoardComponent implements OnInit {
  @Input() ParentHeight: number;
  @Input() ParentWidth: number;
  //true if leaderboard is called from modelZoo page
  @Input() modelFlag: boolean = false;

  @Input() 
  set modelName(modelName: string){
    this.model.leaderDataFilter.modelName = modelName;
  }

  //to get the selected benchmark data
  @Input() 
  set selectedBenchmarkData(selectedBenchmarkData: any){
    this.model.benchmarkName = selectedBenchmarkData.benchmarkName;
    this.model.modality = selectedBenchmarkData.modality;
    console.log("modalitybench",this.model.modality);
    this.model.toDate = selectedBenchmarkData.toDate;
    this.model.fromDate = selectedBenchmarkData.fromDate;
  }
  //to get the modality of the selected model
  @Input() 
  set modality(modality: string){
    if(modality!==''&& modality!==undefined)
    this.model.modality = modality;
    console.log("modemdeom",this.model.modality);
  }
  //to get the selected model name
  @Input()
  set exeModelName(exeModelName: boolean){
    this.model.exeModelName = exeModelName;
    console.log("exeModelName",this.model.exeModelName);
  }
  //to output the filter reset flag
  @Output() resetFiltersFlag = new EventEmitter<{}>();

  constructor(
    private datePipe: DatePipe, 
    public configDataHelper: ConfigDataHelper,
  ) { }

  todayDate = new Date();
  model: any = {
    height: 0,
    width: 0,
    startIndex: 0,
    standaloneFlag:false,
    l1RowEnabled: false,
    l2RowEnabled: false,
    l1RowBenchmarkEnabled: false,
    l1RowLeaderboardEnabled: true,
    benchmarkName:'',
    modality:'',
    exeModelName:false,
    dynamicOffset:{},
    leaderDataFilter: new LeaderFilterData(this.datePipe.transform(this.todayDate, 'yyyy-MM-dd'), this.datePipe.transform(this.todayDate.setDate(this.todayDate.getDate() -30), 'yyyy-MM-dd')),
    leaderboardMfeUrl: this.configDataHelper.getValue(CONSTANTS.CONFIG.LEADERBOARD_MFE_URL),
  };
  
  //offset decided by where the leaderboard is called.
  heightOffset = this.modelFlag ? 250 : 300;
  widthOffset = !this.modelFlag ? 33 : 10;

  //Used for browser cache busting for leaderboard mfe and to set the dynamic offset
  ngOnInit(): void {
    const parent = this;
    parent.setDynamicOffset();
    parent.resizeComponent();
    console.log("modelflagparent",this.modelFlag);
    parent.model.l2RowEnabled = parent.modelFlag ? false:true;

    //Used for browser cache busting for leaderboard mfe 
    let cacheBuster = new Date().toISOString().replace(/[-:.T]/g, '');
    parent.model.leaderboardMfeUrl = parent.model.leaderboardMfeUrl + cacheBuster;
    console.log("leaderboardMfeUrl", parent.model.leaderboardMfeUrl);
  }

  //set the dynamic offset for the leaderboard mfe
  setDynamicOffset(){
    this.model.dynamicOffset={
    leaderboardOffset: !this.modelFlag?352:437,
    leaderboardWOffset:!this.modelFlag?33:58,
    };
  }

  //function to reset the filters
  onResetFilters(data:any){
    const parent = this;
    console.log('receivedparentResetFlag',data);
    this.resetFiltersFlag.emit(data);
  }

  //function to handle window resize
  @HostListener('window:resize', ['$event'])
  onResize() {
    this.resizeComponent();
  }

  //function to resize the component
  private resizeComponent() {
    const parent = this;
    const windowHeight = this.ParentHeight || window.innerHeight;
    const windowWidth = this.ParentWidth || window.innerWidth;
    parent.model.height = windowHeight - parent.heightOffset;
    parent.model.width = windowWidth - parent.widthOffset;
  }

}
