/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { DatePipe } from "@angular/common";
import { Component, EventEmitter, OnInit, Output, Input } from "@angular/core";
import { BenchmarkServiceService } from "../../../service/benchmark-service.service";
import { ConfigDataHelper } from "../../../utils/config-data-helper";


@Component({
  selector: 'app-job-list',
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.scss']
})
export class JobListComponent implements OnInit {
  @Input()
  set jobHeight(jobHeight: number){
    this.model.jobHeight = jobHeight-59;
  }
  @Input() listWidth: number = 0;
  @Input()
  set standaloneFlag(standaloneFlag:string){
    this.model.standaloneFlag = standaloneFlag;
  }
  @Output() selectedBenchmarkData = new EventEmitter<{}>();

  model: any = {
    jobList: [],
    isDataLoaded: true,
    pageDefault:1,
    pageSize:10,
    totalItems:0,
    projectId:'',
    height:0,
    width:0,
    message:'',
    standaloneFlag:true,
    redirectedViewPath:'',
    isAscendingOrder: true,
  };

  constructor(
    public configDataHelper: ConfigDataHelper,
    private benchmarkServiceService: BenchmarkServiceService,
  ) {  }

  //initialize the component with the benchmark list
  ngOnInit(): void {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.getBenchmarkList();
    parent.model.totalItems = parent.model.jobList.length;
  }

  //refresh the status of the execution of a submitted benchmark 
  refreshExecutionIDStatus(executionObject: any, idx: number) {
    const parent = this;
    parent.model.refreshRowId = idx;
    parent.benchmarkServiceService.getBenchmarkStatus(executionObject.id).then((response: any) => {
      executionObject.status = response['status'];
      if(response['errorMsg']){
        executionObject.reason = response['errorMsg'];
      }      
      parent.model.refreshRowId = undefined;
    });
  }

  //refresh the benchmark table
  refreshExecutionDetails() {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.getBenchmarkList();
  }

  //get the benchmark list from the service
  getBenchmarkList(){
    const parent = this;
    parent.benchmarkServiceService.getBenchmarkList()
      .then((response: any) => {
        console.log(response)
        parent.model.jobList = response;
        parent.model.jobList.sort((a:any, b:any) => new Date(b.createdOn).getTime() - new Date(a.createdOn).getTime());
        parent.model.totalItems = response.length;
        parent.model.isDataLoaded = true;
      }).catch(()=>{
        parent.model.jobList = [];
        parent.model.message = 'No data found';
        parent.model.isDataLoaded = true;
      });
  }

  //set the color of the text based on the status of execution
  getStatusColor(currentStatusTxt: string) {
    const statusColor: any = {
      succeeded: "#074b07",
      failed: "#a41414"
    };
    const value = statusColor[currentStatusTxt.toLowerCase()]
    return value ? value : 'black'
  }

  //change the page based on the page number
  onPageChange(page:number){
    const parent = this;
    parent.model.pageDefault=page;
    parent.getDataForCurrentPage();
  }

  //get the data for the current page
  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault-1)*parent.model.pageSize;
    return parent.model.jobList.slice(startIndex,startIndex+parent.model.pageSize);
  }

  //emit the benchmark data on clicking the view button
  onViewClick(name:string,type:string,toDate:string,fromDate:string){
    const parent = this;
    let formattedToDate = new DatePipe('en-US').transform(toDate, 'yyyy-MM-dd');
    let formattedFromDate = new DatePipe('en-US').transform(fromDate, 'yyyy-MM-dd');
    parent.selectedBenchmarkData.emit({modality:type,benchmarkName:name,toDate:formattedToDate,fromDate:formattedFromDate});
  }

  //sort as asc or desc order based on the clik
  sortJobs(sortOrder:string){
    const parent = this;
    parent.model.isAscendingOrder = !parent.model.isAscendingOrder;
    if(sortOrder === 'asc')
      parent.model.jobList.sort((a:any, b:any) => new Date(b.createdOn).getTime() - new Date(a.createdOn).getTime());
    else
      parent.model.jobList.sort((a:any, b:any) => new Date(a.createdOn).getTime() - new Date(b.createdOn).getTime());
    console.log(parent.model.jobList);
  }

}
