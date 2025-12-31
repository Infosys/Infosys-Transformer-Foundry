/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, OnInit, Output, Input, SimpleChanges } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { CONSTANTS } from "src/app/common/constants";
import { ExecutePipelineData } from "../../../data/execute-pipeline-data";
import { PipelineServiceService } from "../../../services/pipeline-service.service";
import { ToasterServiceService } from "../../../services/toaster-service";
import { UtilityService } from "src/app/services/utility.service";
import { PipelineDetailsData } from "src/app/data/pipeline-details-data";
import { BaseComponent } from "src/app/base.component";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { SessionService } from "src/app/services/session.service";
import { PageEvent } from "@angular/material/paginator";

@Component({
  selector: "app-create-pipeline-execution",
  templateUrl: "./create-pipeline-execution.component.html",
  styleUrls: ["./create-pipeline-execution.component.scss"],
})

export class CreatePipelineExecutionComponent extends BaseComponent implements OnInit {
  flag: boolean;
  // model object for storing UI values
  model: any = {
    executionResponseDataList: [],
    isDataLoaded: false,
    executionId: '',
    pipelineName: '',
    isPipelineCreated: false,
    message: '',
    success: CONSTANTS.PIPELINE_EXECUTION_STATUS.SUCCESS,
    executionIDData: undefined,
    refreshRowId: undefined,
    pageDefault:1,
    pageSize:10,
    totalItems:0,
    permissionStatus: false,
    projectId:'',
  };

  // event emitter for closing the modal
  @Output() close = new EventEmitter<string>();
  @Output() saves = new EventEmitter<string>();

  // event emitter for sending the execution data to the parent component
  @Output() executionData = new EventEmitter<{}>();

  // height and width of the modal
  @Input() height: number;
  @Input() width: number;
  @Input() isReadOnly: boolean;

  // input values from the parent component
  @Input() inputPipelineData: PipelineDetailsData;
  @Input() inputPipelineName: string;
  @Input() inputExecutionData: any;
  @Input() pipelineId: string;
  @Input() inputConfidentialData:any;
  @Input()
  set isDataLoaded(isDataLoaded: boolean) {
    this.model.isDataLoaded = isDataLoaded;
  }

  // input project id
  @Input()
  set projectId(projectId: boolean) {
    this.model.projectId = projectId;
  }

  // constructor for the component
  constructor(
    private modalService: NgbModal,
    private pipelineService: PipelineServiceService,
    private toaster: ToasterServiceService,
    public utilityService: UtilityService,
    public sessionService: SessionService,
    public configDataHelper: ConfigDataHelper,
  ) {
    super(sessionService, configDataHelper)
  }

  // on init function
  ngOnInit(): void {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.model.isPipelineCreated = parent.utilityService.isStringHasValue(parent.pipelineId);
    parent.model.pipelineName = this.inputPipelineName;
    parent.model.inputPipelineData = parent.inputPipelineData;
    parent.model.isDataLoaded = true;
    parent.listExecutionDetails();

    parent.model.inputConfidentialData = parent.inputConfidentialData;
    console.log("inputE",this.inputConfidentialData);
    this.isExecutePipelineAllowed()
  }

  // on changes function
  ngOnChanges(changes: SimpleChanges) {
    const parent = this;
    // only run when property "dataLoaded" is changed in the parent component indicating the service call has loaded the values. 
    if (parent.utilityService.isListHasValue(changes['inputExecutionData']?.currentValue)) {
      parent.model.executionResponseDataList = changes['inputExecutionData'].currentValue;
      parent.model.message = parent.model.executionResponseDataList[0]["message"];
    }
    else if(parent.model.executionResponseDataList?.length === 0){
      parent.model.message = "No data found"
    }
  }

  // get the execution data for the pipeline id 
  getExecutionData(pipelineId) {
    const parent = this;
    parent.pipelineService.getExecutionData(pipelineId)
      .then((response: any[]) => {
        parent.model.executionResponseDataList = response;
        parent.model.totalItems = response.length;
        parent.executionData.emit(response);
        parent.model.isDataLoaded = true;
      }).catch(()=>{
        parent.model.executionResponseDataList = [];
        parent.model.isDataLoaded = true;
      });
  }

  // list all the execution details
  listExecutionDetails(){
    const parent = this;
    if(this.isReadOnly){
      parent.refreshExecutionDetails();
    }
  }

  // execute the pipeline configured
  executePipeline(obj: ExecutePipelineData) {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.pipelineService.postExecutePipelineDetails(parent.pipelineId, obj)
      .then(
        responseData => {
          parent.toaster.success(103);
          parent.getExecutionData(parent.pipelineId);
        }).catch(
          data => {
            parent.toaster.failure(104);
            parent.model.isDataLoaded = true;
          });;
  }

  // get the execution details for the execution id
  getExecutionDetails(executionid: string) {
    const parent = this;
    parent.pipelineService.getExecutionDetails(executionid).then(response => {
      parent.model.executionIDData = JSON.parse(JSON.stringify(response))
      delete parent.model.executionIDData.status;
    })
      .catch(error => {
        console.error(error);
      })
  }

  // refresh the execution status for the execution id
  refreshExecutionIDStatus(executionObject, idx) {
    const parent = this;
    parent.model.refreshRowId = idx;
    parent.pipelineService.getExecutionDetails(executionObject.id).then(response => {
      executionObject.status = response['status'];
      if(response['errorMsg']){
        executionObject.reason = response['errorMsg'];
      }
      parent.model.refreshRowId = undefined;
    }).catch(error => {
      executionObject.status = error['status'];
      executionObject.reason = error['data']['Message'];
      parent.model.refreshRowId = undefined;
    });
  }

  // refresh the execution details
  refreshExecutionDetails() {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.pipelineId != ''? parent.getExecutionData(parent.pipelineId): parent.model.isDataLoaded = true;
  }

  // open the modal window
  open(content, isViewMode, executionId?) {
    const parent = this;
    if (isViewMode) {
      parent.getExecutionDetails(executionId);
    } else {
      parent.model.inputPipelineData = parent.inputPipelineData;
      // parent.model.inputConfidentialData = parent.inputConfidentialData;
    }
    parent.openContent(content);
    parent.model.isViewMode = isViewMode;

  }

  // get the status color for the execution status
  getStatusColor(currentStatusTxt) {
    const statusColor = {
      succe: '#074b07',
      fail: "#a41414"
    };

    for (const key in statusColor) {
      const pattern = new RegExp(`.*${key}.*`, 'i');
      if (pattern.test(currentStatusTxt)) {
        return statusColor[key];
      }
    }
    return 'black'
  }

  // show the refresh icon if the status is not success
  showRefreshIcon(currentStatusTxt) {
    const pattern = new RegExp(`.*succe.*`, 'i');
    if (pattern.test(currentStatusTxt)) {
        return false;
    }
    return true;
  }
  
  // on page change event
  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }
  
  // get the data for the current page
  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault-1)*parent.model.pageSize;
    return parent.model.executionResponseDataList.slice(startIndex,startIndex+parent.model.pageSize);
  }

  // check if the user has permission to execute the pipeline
  isExecutePipelineAllowed(){
    const parent = this;
    parent.utilityService.isPermissionAllowed('executePipeline', parent.model.projectId).then(
      (response: any) => {
        console.log(response)
        parent.model.permissionStatus = response;
      }
    ).catch((error: any) => {
      console.error("Error in fetching permission status", error);
      parent.model.permissionStatus = false;
    });
  }

  // open the modal window
  private openContent(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        ariaLabelledBy: "modalTitle2",
        windowClass: "web_custom_modal modal-xlg",
      })
  }
}
