/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { JobDetailsData } from "src/app/data/job-details-data";
import { ModelService } from "src/app/services/models.service";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { UtilityService } from "src/app/services/utility.service";

@Component({
    selector: "app-create-job-summary",
    templateUrl: "./create-job-summary.component.html",
    styleUrls: ["./create-job-summary.component.scss"],
})
export class CreateJobSummaryComponent implements OnInit {
    // close event emitter
    @Output() close = new EventEmitter<string>();
    // confirm event emitter
    @Output() confirm = new EventEmitter<string>();
    // pipeline id event emitter
    @Output() pipelineId = new EventEmitter<string>();
    // input job details data
    @Input()
    set inputJobDetails(inputJobDetails: JobDetailsData) {
        console.log('inputJobDetails', inputJobDetails);
        if (inputJobDetails) {
            inputJobDetails.steps[0].trainingStep.stepArguments.jobArgNames = inputJobDetails.jobArguments.map((jobArg) => jobArg.name);
            this.model.summaryData = JSON.parse(JSON.stringify(inputJobDetails));
            this.updateSummaryData();
        }
    }
    // height and width
    @Input() height: number;
    @Input() width: number;
    // data loaded flag
    @Input()
    set isDataLoaded(isDataLoaded: boolean) {
        console.log("this.model.isDataLoaded",isDataLoaded)
        this.model.isDataLoaded = isDataLoaded
    }
    // read only flag
    @Input()
    set isReadOnly(isReadOnly: boolean) {
        this.model.isReadOnly = isReadOnly
    }

    // constructor
    constructor(
        private modalService: NgbModal,
        private router: Router,
        private route: ActivatedRoute,
        private myService: ModelService,
        private toaster: ToasterServiceService,
        private utilityService: UtilityService) { }

    // model object that contains the variables binding to the UI
    model: any = {
        summaryData: {},
        experimentDataObject: {},
        pipelineId: '',
        isDataLoaded: false,
        isReadOnly: false,
        projectId:'',
        isBtnDisabled:false
    }

    // on init
    ngOnInit(): void {
        this.getProjectName();
        this.isCreatePipelineAllowed();
    }

    // update the summary data
    updateSummaryData(){
        const parent = this;
        this.model.pipelineId = this.model.summaryData.id;
        // this.model.pipelineId = this.model.isReadOnly ? this.model.summaryData.id : '';
        console.log(this.model.pipelineId);
        console.log(this.model.isReadOnly);
        const modelOriginalName = this.model.summaryData.originalName;
        parent.filterExperimentData();
        console.log(this.model.summaryData);

        //while initial loading summary data will contain globalId 
        const tsGlobalProjectId = this.model.summaryData.projectId;
        this.updateProjectId();
        this.model.summaryData.projectId = parent.model.projectId;
        this.replaceArtifactUri(modelOriginalName, tsGlobalProjectId);
    }

    // update the project id
    updateProjectId(){
        const parent=this;
        let urlsegment = (window.location.href).split('/')
        let index = urlsegment.indexOf('projects');
        if (index!==-1 && index+1 < urlsegment.length) {
            parent.model.projectId= urlsegment[index+1];
        }
    }

    // replace the artifact uri
    replaceArtifactUri(modelOriginalName: string, globalProjectId: string) {
        let artifactUri = this.model.summaryData?.steps[0]?.trainingStep?.inputArtifacts?.uri;
        if (this.model.summaryData?.steps[0]?.trainingStep?.inputArtifacts?.uri != null) {
            artifactUri = artifactUri.replace(modelOriginalName, this.model.summaryData.name);
            artifactUri = artifactUri.replace(globalProjectId, this.model.summaryData.projectId);
            this.model.summaryData.steps[0].trainingStep.inputArtifacts.uri = artifactUri;
        }
    }

    // create experiment
    createExperimentDetails() {
        const parent = this;
        parent.model.isReadOnly = true;
        parent.model.isDataLoaded = false;
        try {
            parent.myService.createExperimentDetails(parent.model.summaryData)
                .then(
                    responseData => {
                        parent.model.isReadOnly = true;
                        parent.model.isDataLoaded = true;
                        parent.toaster.success(102);
                        const data = responseData;
                        console.log('post', data);
                        parent.model.pipelineId = responseData['data'].id;
                        parent.pipelineId.emit(this.model.pipelineId);
                        if (parent.router.url.includes('rc=true')) {
                            this.router.navigate(['/projects', responseData['data']["projectId"], 'experiments', 'view', parent.model.pipelineId], { queryParams: { pn: parent.model.projectName } });
                        }
                    }).catch(
                        data => {
                            parent.model.isReadOnly = false;
                            parent.model.isDataLoaded = true;
                            if(data){
                                parent.toaster.failureWithMessage(data.error?.detail?.message || data.error?.details?.[0]?.message); //backendFix
                            }else {
                                parent.toaster.failure(106);
                            }
                        });
        } catch {
            parent.toaster.failure(106);
        }
    }

    // download summary data
    downloadSummaryData() {
        const fileName = 'JobData.json';
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
    isCreatePipelineAllowed(){
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

    // call the open modal
    open(content, isBtnDisabled,) {
        const parent = this;
        parent.openConfirmDialog(content);
    }

    // open modal window
    private openConfirmDialog(content) {
        const parent = this;
        parent.modalService
        .open(content, {
          centered: true,
          windowClass: 'square-modal',
        });    }

    // get the project name from query params
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

    // filter experiment data for unnecessary fields
    private filterExperimentData() {
        delete this.model.summaryData.createdBy;
        delete this.model.summaryData.createdOn;
        delete this.model.summaryData.isDeleted;
        delete this.model.summaryData.updatedBy;
        delete this.model.summaryData.modifiedOn;
        delete this.model.summaryData.scope;
        delete this.model.summaryData.status;
        delete this.model.summaryData.originalName;
        delete this.model.summaryData.id;
    }

}
