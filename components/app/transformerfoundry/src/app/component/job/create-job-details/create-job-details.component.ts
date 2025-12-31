/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, Input, OnInit, Output,EventEmitter, SimpleChanges } from "@angular/core";
import { JobDetailsData } from "src/app/data/job-details-data";

@Component({
  selector: "app-create-job-details",
  templateUrl: "./create-job-details.component.html",
  styleUrls: ["./create-job-details.component.scss"],
})

export class CreateJobDetailsComponent implements OnInit {
  constructor(
  ) { }

  // event emitters
  @Output() jobDetails = new EventEmitter<{}>();
  @Input() height: number;
  @Input() width: number;
  @Input()
  set inputJobDetails(inputJobDetails: JobDetailsData) {
    this.model.jobDataObject = inputJobDetails
    console.log(this.model.jobDataObject);
  }
  @Input()
  set isDataLoaded(isDataLoaded: boolean) {
    this.model.isDataLoaded = isDataLoaded
  }
  @Input()
  set isReadOnly(isReadOnly: boolean) {
    this.model.isReadOnly = isReadOnly
  }

  model: any = {
    jobDataObject: undefined,
    isDataLoaded: false,
    isReadOnly:false,
  }

  // show or collapse the sections 
  showSection = {
    jobArguments: true,
    container: true,
    storage: true,
    environmentVariables: true,
    commandAndArguments: true,
    pretrainedModel: true,
    output: true,
  }

  // on init
  ngOnInit() {
    this.updateType();
  }

  // values for the storage
  storage: Storage[] = [
    { value: "INFY_AICLD_MINIO", viewValue: "INFY_AICLD_MINIO" },
    { value: "INFY_AICLD_NUTANIX", viewValue: "INFY_AICLD_NUTANIX" },
  ];
  selectedStorage: string = this.storage[0].value;
  preSelectedStorage: string = this.storage[0].value;

  // values for the data type
  dataType: Storage[] = [
    { value: "string", viewValue: "string" },
    { value: "int", viewValue: "int" },
    { value: "bool", viewValue: "bool" },
    { value: "float", viewValue: "float" },
  ];
  selectedDataType: string = this.dataType[0].value;

  // handle the input job details on change
  ngOnChanges(changes: SimpleChanges) {
    if (changes.inputJobDetails && !changes.inputJobDetails.firstChange) {
      this.handleDetailChanges();
    }
  }

  // add job arguments
  addJobArgs() {
    this.model.jobDataObject.jobArguments.push({ name: '', defaultVal: '', dataType: '' });
  }

  // remove job arguments
  removeJobArgs(index: number) {
    this.model.jobDataObject.jobArguments.splice(index, 1);
  }

  // add environment variables
  addEnvVariable() {
    if(!this.model.jobDataObject.steps[0].trainingStep.container.envVariables){
      this.model.jobDataObject.steps[0].trainingStep.container.envVariables=[];
    }
    this.model.jobDataObject.steps[0].trainingStep.container.envVariables.push({name:'',value:''});
  }

  // remove environment variables
  removeEnvVariable(index: number) {
    this.model.jobDataObject.steps[0].trainingStep.container.envVariables.splice(index, 1);
  }

  // update the storage type
  updateType() {
    const parent = this;
    if (parent.model.jobDataObject.steps?.trainingStep?.inputArtifacts?.storageType !== undefined) {
      this.selectedStorage = parent.model.jobDataObject.steps.trainingStep.inputArtifacts.storageType;
    }
    
    if (parent.model.jobDataObject?.steps?.trainingStep?.preTrainedModelDetails?.artifacts?.storageType !== undefined) {
      this.preSelectedStorage = parent.model.jobDataObject.steps.trainingStep.preTrainedModelDetails.artifacts.storageType;
    }
  }

  // input validation for job name
  onInput(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    const regexPattern = /^[a-z0-9-]+$/;
    const currentValue = inputElement.value;

    // Filter the input to allow only valid characters
    const filteredValue = currentValue.split('').filter((char) => regexPattern.test(char)).join('');

    // Update the input value with the filtered value
    inputElement.value = filteredValue;
    this.model.jobDataObject.name = filteredValue;
    this.model.flag=false;
    console.log(this.model.flag);
  }

  // toggle the section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
  }

  // handle the detail changes
  private handleDetailChanges() {
    const parent = this;
    parent.jobDetails.emit(parent.model.jobDataObject);
  }
}
export interface Storage {
  value: string;
  viewValue: string;
}
