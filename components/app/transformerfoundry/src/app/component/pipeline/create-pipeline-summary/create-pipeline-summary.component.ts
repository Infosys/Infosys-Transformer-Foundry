/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, Input, OnInit, Output, EventEmitter } from "@angular/core";
import { ActivatedRoute, Router } from '@angular/router';
import { PipelineServiceService } from "../../../services/pipeline-service.service";
import { PipelineDetailsData } from "../../../data/pipeline-details-data";
import { PayloadData } from "../../../data/payload-data";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { UtilityService } from "src/app/services/utility.service";

@Component({
  selector: "app-create-pipeline-summary",
  templateUrl: "./create-pipeline-summary.component.html",
  styleUrls: ["./create-pipeline-summary.component.scss"],
})

export class CreatePipelineSummaryComponent implements OnInit {
  // close and confirm output events
  @Output() close = new EventEmitter<string>();
  @Output() confirm = new EventEmitter<string>();

  // input properties for the component height and width
  @Input() height: number;
  @Input() width: number;

  // input payload data and pipeline data, confidential data
  @Input() inputNodePayload: PayloadData;
  @Input() inputPipelineData: PipelineDetailsData;
  @Input() inputConfidentialData:any;
  @Input()
  set isReadOnly(isReadOnly: boolean) {
    this.model.isReadOnly = isReadOnly
  }
  @Input()
  set isDataLoaded(isDataLoaded: boolean) {
    this.model.isDataLoaded = isDataLoaded
  }
  @Output() pipelineId = new EventEmitter<string>();

  // model for the component
  model: any = {
    summaryData: {},
    maskedSummaryData:{},
    isReadOnly: false,
    isDataLoaded: false,
    pipelineId: '',
    projectId:'',
    isBtnDisabled: false,
    projectName: ''
  }

  // constructor for the component
  constructor(
    private pipelineService: PipelineServiceService,
    private router: Router,
    private route: ActivatedRoute,
    private toaster: ToasterServiceService,
    private modalService: NgbModal,
    private utilityService: UtilityService
  ) {
  }

  // on init lifecycle hook
  ngOnInit(): void {
    this.getProjectName();
    this.model.maskedSummaryData=this.maskFields(this.inputPipelineData,this.inputConfidentialData);
    this.model.summaryData = this.inputPipelineData;
    this.model.pipelineId = this.model.summaryData.id;
    this.updateProjectId();
    this.model.summaryData.projectId = this.model.projectId;
    console.log(this.model.maskedSummaryData);
    this.isCreatePipelineAllowed();
    console.log(this.model.pipelineId);
  }

  // update project id from url
  updateProjectId(){
    const parent=this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('projects');
    if (index!==-1 && index+1 < urlsegment.length) {
      parent.model.projectId= urlsegment[index+1];
    }
  }

  // create pipeline
  createPipeline() {
    const parent = this;
    parent.model.isReadOnly = true;
    parent.model.isDataLoaded = false;
    try {
      parent.pipelineService.createPipelineDetails(parent.model.summaryData)
        .then(
          (responseData: any) => {
            parent.model.isReadOnly = true;
            parent.isCreatePipelineAllowed();
            parent.model.isDataLoaded = true;
            // console.log("ResponseData:", responseData);
            
            parent.sendPayloadData(responseData?.id);
            //if the url contains rc==true in params, navigate to view, pipeline id
            if (parent.router.url.includes('rc=true')) {
              parent.router.navigate(['/projects/', parent.model.projectId, 'pipelines' , 'view', responseData?.id], { queryParams: { pn:  this.model.projectName} });
            }

            if (parent.router.url.includes('gt=true')) {
              parent.pipelineService.postGlobalTemplatesHistory(
                parent.model.projectId,
                responseData?.id
              );
              parent.router.navigate(['/projects/', parent.model.projectId, 'pipelines' , 'view', responseData?.id], { queryParams: { pn:  this.model.projectName} });
            }
          }).catch(
            data => {
              parent.model.isReadOnly = false;
              parent.model.isDataLoaded = true;
              if (data) {
                parent.toaster.failureWithMessage(data?.["details"]?.[0]?.message|| data?.["detail"]?.message || data?.Error); //backendFix
              } else {
                parent.toaster.failure(104);
              }
            });
    } catch {
      parent.toaster.failure(104);
    }

  }

  // send payload data of the pipeline id
  sendPayloadData(pipelineId) {
    const parent = this;
    parent.inputNodePayload.pipelineId = pipelineId;
    parent.inputNodePayload.projectId = this.model.projectId;
    parent.inputNodePayload.pipelineData = parent.inputConfidentialData;
    parent.pipelineService.postNodeFormData(parent.inputNodePayload).then((response: any) => {
     
      console.log("CreatePipelineSummary:", response);
      
      parent.toaster.success(102);
      this.model.summaryData.id = pipelineId;
      parent.model.pipelineId = pipelineId;
      parent.pipelineId.emit(pipelineId);
    });
  }

  // download the summary data
  downloadSummaryData() {
    const fileName = 'PipelineData.json';
    const fileToSave = new Blob([JSON.stringify(this.model.summaryData)], {
      type: 'application/json',
    });

    const url = window.URL.createObjectURL(fileToSave);

    // Create a dummy anchor element and click it to trigger the download
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName; // Specify the filename
    link.click();

    // Clean up the URL object to avoid memory leaks
    window.URL.revokeObjectURL(url);
  }

  // check if create pipeline is allowed
  isCreatePipelineAllowed() {
    const parent = this;
    if(!this.model.isReadOnly){
        this.utilityService.isPermissionAllowed('createPipeline', parent.model.projectId).then(
            (response: any) => {        
              parent.model.isBtnDisabled = !response;
              console.log(parent.model.isBtnDisabled)
            }
          ).catch((error: any) => {
            console.error("Error in fetching permission status", error);
            parent.model.isBtnDisabled = false;
          });
    }
    else{

        parent.model.isBtnDisabled = true;
    }
  }

  // open modal
  open(content, isBtnDisabled,) {
    const parent = this;
    parent.openConfirmDialog(content);
  }

  // open confirm dialog
  private openConfirmDialog(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });
  }

  // get project name from url
  private getProjectName() {
    const parent = this;
    parent.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else {
        parent.model.projectName = '';
      }
    });
  }

  // mask input confidential fields
  private maskFields(inputPipelineData:any, inputConfidentialData:any){

    //funtion to dispay masked values according to input length 
    // function maskString(str){
    //   return '.'.repeat(str.length);
    // }

    if(!inputPipelineData || !inputConfidentialData){
      return inputPipelineData
    }
    const maskedData = JSON.parse(JSON.stringify(inputPipelineData));
    const maskValue=(obj:any, key:string)=>{
      if(obj[key] && typeof obj[key] === 'string'){
        obj[key]='**********';

        //funtion to dispay masked values according to input length
        // obj[key]=maskString(obj[key]);
      }
    };
    const variables = inputConfidentialData.variables;
    const globalVariables = inputConfidentialData.globalVariables;
    if (variables) {
      for(const key in variables){
        if (variables.hasOwnProperty(key) && variables[key]) {
          maskValue(maskedData.pipeline.variables,key);
        }
      }
    }
    if (globalVariables) {
      for(const key in globalVariables){
        if (globalVariables.hasOwnProperty(key) && globalVariables[key]) {
          maskValue(maskedData.pipeline.globalVariables,key);
        }
      }
    }
    return maskedData;
  }
}
