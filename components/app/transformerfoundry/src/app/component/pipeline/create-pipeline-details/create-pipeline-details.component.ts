/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, OnInit, Output, Input, OnDestroy, SimpleChanges } from "@angular/core";
import { PipelineDetailsData, Volume } from "../../../data/pipeline-details-data";
import { MatSelectChange } from "@angular/material/select";
import { PipelineData } from "src/app/data/payload-data";

@Component({
  selector: "app-create-pipeline-details",
  templateUrl: "./create-pipeline-details.component.html",
  styleUrls: ["./create-pipeline-details.component.scss"],
})

export class CreatePipelineDetailsComponent {
  constructor(
  ) { }

  // event emitters for height, width, pipeline data and confidential data
  @Input() height: number;
  @Input() width: number;
  @Output() pipelinedtData = new EventEmitter<{}>();
  @Output() confidentialData = new EventEmitter<any>();
  @Input() isReadOnly: boolean;
  @Input() 
  set inputConfidentialData(inputConfidentialData: PipelineData) {
      this.model.pipelineData = inputConfidentialData
  }
  @Input()
  set isDataLoaded(isDataLoaded: boolean) {
    this.model.isDataLoaded = isDataLoaded
  }
  @Input()
  set inputPipelineData(inputPipelineData: PipelineDetailsData) {
    this.model.pipelineObject = inputPipelineData
  }

  // masked character for password
  maskedCharacter = '*';
  type='';

  // model for pipeline details
  model: any = {
    pipelineObject: undefined,
    isDataLoaded: false,
    pipelineData:{
      variables:{},
      globalVariables:{}
    },
    maskedPassword: this.maskedCharacter.repeat(10)
  }

  // show section flag
  showSection = {
    volume: true,
    storage: true,
    environmentVariables: true,
    pipelineVariables: true
  }

  // on init function
  ngOnInit(){
    const parent = this;
    // TODO: Make volume field as null in form.
    if (parent.model.pipelineObject.pipeline.volume)
      parent.model.pipelineObject.pipeline.volume.scope = parent.Scope[0].value;
  }

  Runtime: Runtime[] = [
    { value: "kubernetes", viewValue: "kubernetes" },
    { value: "Vm", viewValue: "Vm" },
  ];
  ops: Orchestrator[] = [
    { value: "kubeflow", viewValue: "kubeflow" },
    { value: "airflow", viewValue: "airflow" },
  ];
  Scope:  Scope[] = [
    { value: "pipeline", viewValue: "Pipeline" },
    { value: "platform", viewValue: "platform" },
  ];
  variables: Variables[] = [
    { value: "Input Variable  ", viewValue: "Input Variable" },
    { value: "Global Variable", viewValue: "Global Variable" },
  ];
  storage: Storage[] = [
    { value: "INFY_AICLD_MINIO", viewValue: "INFY_AICLD_MINIO" },
    { value: "INFY_AICLD_NUTANIX", viewValue: "INFY_AICLD_NUTANIX" }
  ];
  selectedScope: string = this.Scope[0].value;
  selectedRuntime: string = this.Runtime[0].value;
  selectedOperator: string = this.ops[0].value;
  selectedVariable: string = "variables"
  // variableType: string = this.variables[0].value;
  selectedStorage: string = this.storage[0].value;
  
  // on changes function
  ngOnChanges(changes: SimpleChanges) {
    if (changes.inputPipelineData && !changes.inputPipelineData.firstChange) {
      this.handleDetailChanges();
    }
    if (changes.inputConfidentialData && !changes.inputConfidentialData.firstChange) {
      this.handleConfidentialFlagChanges();
    }
  }

  //function to return the list of keys - html we will iterate the keys - remove the declaration.
  getKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  // function to add and remove fields from the UI
  addNewVariable(variableType) {
    const parent = this;
    parent.selectedVariable = variableType == this.variables[0].value ? 'variables' : 'globalVariables';
    parent.model.pipelineObject.pipeline[parent.selectedVariable][''] = "";
  }

  addNewStorage() {
    this.model.pipelineObject.pipeline.dataStorage.push({ storageType: '', name: '', uri: '' });
  }

  removeStorage(index: number) {
    this.model.pipelineObject.pipeline.dataStorage.splice(index, 1);
  }

  addNewVolume(){
    this.model.pipelineObject.pipeline.volume = new Volume();
  }

  removeVolume(){
    delete this.model.pipelineObject.pipeline.volume;
  }
  
  deleteAddedVariables(obj: object, key: string) {
    delete obj[key];
    delete this.model.pipelineData[this.selectedVariable][key];
  }

  // function to handle the input event of the pipeline name
  onInput(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    const regexPattern = /^[a-z0-9-]+$/;
    const currentValue = inputElement.value;

    // Filter the input to allow only valid characters
    const filteredValue = currentValue.split('').filter((char) => regexPattern.test(char)).join('');

    // Update the input value with the filtered value
    inputElement.value = filteredValue;
    this.model.pipelineObject.pipeline.name = filteredValue;
  }

  // toggle confidential icon to show and hide password
  toggleConfidentialData(key:string,obj:object,event?:any){
    const parent =this;
    obj[key]=!obj[key];
    parent.handleConfidentialFlagChanges();
  }

  // function to update the variable name
  updateVariableName(obj: Object, oldKey: string, enterdKey: string, variableType: string) {
    if (oldKey === enterdKey) {
      return;
    }
    const parent = this;
    parent.selectedVariable = variableType == this.variables[0].value ? 'variables' : 'globalVariables';
    var newKey = enterdKey, i = 1;
    while (obj.hasOwnProperty(enterdKey)) {
      newKey = enterdKey + "-" + i;
      if (!obj.hasOwnProperty(newKey))
        break;
      else
        newKey = enterdKey;
      i++;
    }
    obj[newKey] = obj[oldKey];
    delete obj[oldKey];

    parent.model.pipelineData[parent.selectedVariable][newKey] = parent.model.pipelineData[parent.selectedVariable]?.[oldKey];
    delete parent.model.pipelineData[parent.selectedVariable][oldKey];
  }

  // function to update the variable value
  updateVariableValue(key, obj, event){
    console.log('updateVariableValue', event, event.target.value);
    obj[key] = event.target.value;
  }

  // function to update the variable item
  updateVariableItem(obj: Object, name: string, type: MatSelectChange) {
    const parent = this;
    parent.selectedVariable = type.value == this.variables[0].value ? 'variables' : 'globalVariables';
    var previousType = type.value == this.variables[0].value ?  'globalVariables' : 'variables';
    var newKey = name, i = 1;
    while (parent.model.pipelineObject.pipeline[parent.selectedVariable].hasOwnProperty(name)) {
      newKey = name + "-" + i;
      if (!obj.hasOwnProperty(newKey))
        break;
      else
        newKey = name;
      i++;
    }
    parent.model.pipelineObject.pipeline[parent.selectedVariable][newKey] = obj[name];
    delete obj[name];

    parent.model.pipelineData[parent.selectedVariable][newKey] = parent.model.pipelineData[previousType]?.[name];
    delete parent.model.pipelineData[previousType][name];
  }

  // toggle show section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
  }

  // function to handle the changes in the pipeline details
  private handleDetailChanges() {
    const parent = this;
    parent.pipelinedtData.emit(parent.model.pipelineObject);
  }

  // function to handle the changes in the confidential flag
  private handleConfidentialFlagChanges(){
    const parent = this;
    parent.confidentialData.emit(parent.model.pipelineData);
    console.log(parent.model.pipelineData);
  }
}
export interface Runtime {
  value: string;
  viewValue: string;
}
export interface Orchestrator {
  value: string;
  viewValue: string;
}
export interface Variables {
  value: string;
  viewValue: string;
}
export interface Storage {
  value: string;
  viewValue: string;
}
export interface Scope {
  value: string;
  viewValue: string;
}
