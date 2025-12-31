/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, Input, OnInit, Output, SimpleChanges } from "@angular/core";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { CONSTANTS } from "src/app/common/constants";
import { JobDetailsData } from "src/app/data/job-details-data";
import { TrialData } from "src/app/data/trial-data";
import { DataStorageService } from "src/app/services/data-storage.service";
import { ModelService } from "src/app/services/models.service";
import { ProjectServiceService } from "src/app/services/project-service.service";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { UtilityService } from "src/app/services/utility.service";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { DomSanitizer, SafeResourceUrl } from "@angular/platform-browser";
import { PageEvent } from "@angular/material/paginator";

@Component({
  selector: "app-create-job-execution",
  templateUrl: "./create-job-execution.component.html",
  styleUrls: ["./create-job-execution.component.scss"],
})

export class CreateJobExecutionComponent implements OnInit {
  // close and save event emitters
  @Output() close = new EventEmitter<string>();
  @Output() saves = new EventEmitter<string>();

  // input job details data
  @Input() inputJobDetails: JobDetailsData;

  // input trial data
  @Input()
  set inputTrialData(inputTrialData: TrialData) {
    this.model.trialDataList = inputTrialData;
  }

  // height and width
  @Input() height: number;
  @Input() width: number;
  @Input()
  set isDataLoaded(isDataLoaded: boolean) {
    this.model.isDataLoaded = isDataLoaded;
  }

  // pipeline id
  @Input() pipelineId: string;

  // project id
  @Input()
  set projectId(projectId: string) {
    this.model.projectId = projectId;
  }

  // experiment id
  @Input() 
  set inputExperimentId(inputExperimentId: number) {
    this.model.experimentId = inputExperimentId;
  }

  // run name
  @Input() 
  set runName(runName: string) {
    this.model.runName = runName;
    console.log(this.model.runName);
  }

  model: any = {
    isDataLoaded: false,
    isPipelineCreated: false,
    trialDataList: undefined,
    refreshRowId: undefined,
    message: '',
    pageDefault:1,
    // pageDefault:0,
    pageSize:10,
    totalItems:0,
    permissionStatus: false,
    projectId: '',
    success: CONSTANTS.TRIAL_EXECUTION_STATUS.SUCCESS,
    iFrameUrl:'',
    experimentId:0,
    runName: '',
    runId:0
  }
  
  // modal configurations
  normalModalConfig = {
    ariaLabelledBy: "modalTitle2",
    windowClass: "web_custom_modal modal-xlg",
  };
  largeModalConfig = {
    ariaLabelledBy: "modalTitle3",
    windowClass: "web_custom_modal modal-xlg",
  };

  showLoadingIcon: boolean = true;

  // once iframe is loaded, hide the loading icon
  onIframeLoad() {
    this.showLoadingIcon = false;
  }
 
  // constructor
  constructor(private modalService: NgbModal,
    private modelService: ModelService,
    public utilityService: UtilityService,
    public configDataHelper: ConfigDataHelper,
    private toaster: ToasterServiceService,
    private sanitizer:DomSanitizer,
  )
  { }

  // on init, get the trial list for the experiment id
  ngOnInit(): void {
    const parent = this;
    parent.model.isPipelineCreated = parent.utilityService.isStringHasValue(this.inputJobDetails.id);
    parent.modelService.getExperimentDetails(parent.model.runName).then(response => {
      console.log(response);
      parent.model.experimentId = response['experiment']['experiment_id'];
      parent.model.runId = response['experiment']['tags']?.[0]?.['value'];
      console.log(parent.model.experimentId, parent.model.runId);
    }).catch(error => {
      console.error("Error in fetching experiment details", error);
    });
    this.refreshExecutionDetails();
    this.isExecutePipelineAllowed();
  }

  // on changes, get the trial list
  ngOnChanges(changes: SimpleChanges) {
    const parent = this;
    // only run when property "dataLoaded" is changed in the parent component indicating the service call has loaded the values. 
    if (parent.utilityService.isListHasValue(changes['inputTrialData']?.currentValue) && parent.utilityService.isListHasValue(changes['model.trialDataList']?.currentValue)) {
      parent.model.trialDataList = changes['inputTrialData'].currentValue;
      parent.model.message = parent.model.trialDataList[0]["message"];
    }
    else {
      parent.model.message = "No data found"
    }
  }

  // get the trial list
  getTrialList() {
    const parent = this;
    try {
      if (parent.model.projectId !== '' && parent.pipelineId !== '') {
        parent.modelService.getTrialList(parent.model.projectId, parent.pipelineId)
          .then(responseData => {
            parent.model.trialDataList = responseData['trials'];
            console.log(parent.model.trialDataList)
            parent.model.isDataLoaded = true;
            parent.model.totalItems = responseData['trials'].length;
            // parent.getExecutionData(parent.pipelineId);
          }).catch(error => {
            parent.model.isDataLoaded = true;
            parent.model.trialDataList = [];
            console.log(error.message);
            error.message ? parent.toaster.failureWithMessage(error.message) :
              parent.toaster.failure(104);
          });
      }
      else{
        parent.model.isDataLoaded = true;
        parent.model.trialDataList = [];
      }
    }
    catch (error) {
      error.message ? parent.toaster.failureWithMessage(error.message) :
        parent.toaster.failure(104);
      parent.model.trialDataList = [];
      console.log(error.message, parent.model.trialDataList)
      parent.model.isDataLoaded = true;
    }
  }

  // refresh the trial id status
  refreshTrialIDStatus(executionObject, idx) {
    const parent = this;
    parent.model.refreshRowId = idx;
    parent.modelService.getTrialStatus(executionObject.id).then(response => {
      executionObject.status = response['status'];
      parent.model.refreshRowId = undefined;
    }).catch(error => {
      parent.model.refreshRowId = undefined;
      executionObject.status = "Unknown";
      console.log(error.message, parent.model.refreshRowId, executionObject.status, executionObject.id);
    });
  }

  // refresh the execution details
  refreshExecutionDetails() {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.getTrialList();
  }

  // get the status color based on the trial status
  getStatusColor(currentStatusTxt) {
    const statusColor = {
      Succeeded: "#074b07",
      Failed: "#a41414"
    };
    const value = statusColor[currentStatusTxt]
    return value ? value : 'black'
  }

  // on page change event
  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    // parent.model.isDataLoaded = false;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }

  // get the data for the current page
  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault-1)*parent.model.pageSize;
    return parent.model.trialDataList.slice(startIndex,startIndex+parent.model.pageSize);
  }

  // check if the pipeline is allowed to execute
  isExecutePipelineAllowed(){
    const parent = this;
    console.log("Inside isExecutePipelineAllowed")
    this.utilityService.isPermissionAllowed('executePipeline', parent.model.projectId).then(
      (response: any) => {
        console.log(response)
        parent.model.permissionStatus = response;
      }
    ).catch((error: any) => {
      console.error("Error in fetching permission status", error);
      parent.model.permissionStatus = false;
    });
  }

  // get the iframe url
  getIFrameUrl(){
    const parent = this;
    console.log(parent.model.experimentId, parent.model.runId);
    parent.model.iFrameUrl= parent.sanitizer.bypassSecurityTrustResourceUrl(
      this.configDataHelper.getValue(CONSTANTS.CONFIG.ML_FlOW_SERVICE_BASER_URL)+
      CONSTANTS.APIS.ML_FLOW_SERVICE.SEARCH_RUNS.replace(CONSTANTS.PLACEHOLDER.EXID,parent.model.experimentId).replace(CONSTANTS.PLACEHOLDER.ID,parent.model.runId));
    console.log('iframeUrl:',parent.model.iFrameUrl);
  }

  // open the modal
  open(content, modalConfig, isViewMode, executionId?) {
    const parent = this;
    parent.getIFrameUrl();
    parent.openContent(content, modalConfig);
  }

  // open the content
  private openContent(content, modalConfig) {
    this.modalService
      .open(content, modalConfig)
  }  
}
