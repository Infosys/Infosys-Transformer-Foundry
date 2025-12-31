/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { DatePipe } from "@angular/common";
import { Component, EventEmitter, OnInit, Output, Input, SimpleChanges, HostListener } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { CONSTANTS } from "../../../common/constants";
import { BenchmarkServiceService } from "../../../service/benchmark-service.service";
import { ConfigDataHelper } from "../../../utils/config-data-helper";
import { PageEvent } from "@angular/material/paginator";


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
    pageDefault:0,
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
    private modalService: NgbModal,
    public configDataHelper: ConfigDataHelper,
    private benchmarkServiceService: BenchmarkServiceService,
    private route: ActivatedRoute,
    private router: Router,
  ) {  }

  ngOnInit(): void {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.getBenchmarkList();
    // parent.model.isDataLoaded = false;
    // parent.model.jobList = [
    //   {
    //     executionId: "2f416feb-1d9c-4a55-911f-486d6dbd95f1",
    //     name: "starcodbasemultiint8",
    //     status: "Initiated",
    //     type: "code",
    //     createdOn: "2023-10-30T13:02:15.278Z",
    //   },
    //   {
    //     executionId: "69ffe3e9-a4c1-43f0-925b-8d8a795e7f0a",
    //     name: "starcodeint4infosysdyn",
    //     status: "In Progress",
    //     type: "code",
    //     createdOn: "2023-10-20T13:02:15.278Z",
    //   },
    //   {
    //     executionId: "c7b60806-6a3a-4c22-9579-bfdb836bca0c",
    //     name: "code2bfp32concode",
    //     status: "Success",
    //     type: "text",
    //     createdOn: "2023-10-21T13:02:15.278Z",
    //   },
    //   {
    //     executionId: "3113bc5d-ab37-4f19-8861-7fd015d43f72",
    //     name: "code2bint16concode",
    //     status: "Failed",
    //     type: "text",
    //     createdOn: "2023-10-10T13:02:15.278Z",
    //   },
    // ];
    // parent.model.jobList.sort((a:any, b:any) => new Date(b.createdOn).getTime() - new Date(a.createdOn).getTime());
    parent.model.totalItems = parent.model.jobList.length;
  }

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

  refreshExecutionDetails() {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.getBenchmarkList();
  }

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

  getStatusColor(currentStatusTxt: string) {
    const statusColor: any = {
      succeeded: "#074b07",
      failed: "#a41414"
    };
    const value = statusColor[currentStatusTxt.toLowerCase()]
    return value ? value : 'black'
  }

  // onPageChange(page:number){
  //   const parent = this;
  //   parent.model.pageDefault=page;
  //   parent.getDataForCurrentPage();
  // }

  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }

  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault)*parent.model.pageSize;
    return parent.model.jobList.slice(startIndex,startIndex+parent.model.pageSize);
  }

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
    // parent.model.jobList = parent.model.jobList.sort((a:any,b:any)=>{
    //    ? a.createdOn - b.createdOn : b.createdOn - a.createdOn;
    // });
    console.log(parent.model.jobList);
  }

}
