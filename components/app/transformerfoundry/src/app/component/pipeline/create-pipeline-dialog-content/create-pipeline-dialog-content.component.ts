/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, Input, OnInit, Output, SimpleChanges } from "@angular/core";
import { MatSelectChange } from "@angular/material/select";
import { ExecutePipelineData } from "src/app/data/execute-pipeline-data";
import { PipelineDetailsData } from "src/app/data/pipeline-details-data";
import { PipelineServiceService } from "src/app/services/pipeline-service.service";
import { ToasterServiceService } from "src/app/services/toaster-service";

@Component({
  selector: "app-create-pipeline-dialog-content",
  templateUrl: "./create-pipeline-dialog-content.component.html",
  styleUrls: ["./create-pipeline-dialog-content.component.scss"],
})
export class CreatePipelineDialogContentComponent implements OnInit {
  // constructor
  constructor(
    private pipelineService: PipelineServiceService, 
    private toaster: ToasterServiceService) {
  }
  // event emitters for close and save
  @Output() close = new EventEmitter<string>();
  @Output() save = new EventEmitter<object>();
  // input pipeline data
  @Input() inputPipelineData: PipelineDetailsData;
  @Input() isReadOnly: boolean;
  @Input() isLinkClicked:Boolean;
  // input execution details
  @Input() executionDetails:ExecutePipelineData;
  @Input() isViewMode:boolean;
  @Input() pipelineId: string;
  
  storage: Storage[] = [
    { value: "INFY_AICLD_MINIO", viewValue: "INFY_AICLD_MINIO" },
    { value: "INFY_AICLD_NUTANIX", viewValue: "INFY_AICLD_NUTANIX" }
  ];
  variables: Variables[] = [
    { value: "Input Variable  ", viewValue: "Input Variable" },
    { value: "Global Variable", viewValue: "Global Variable" },
  ];
  selectedStorage: string = this.storage[0].value;
  // variableType: string = this.variables[0].value;
  selectedVariable: string = "variables"
  model: any = {
    isDataLoaded: false,
    pipelineObject: undefined,
    pipelineData: undefined
  }

  // on init
  ngOnInit(): void {
    if(!this.isViewMode){
      this.filterInputPipelineData();
    }
    this.getPayloadData(this.pipelineId);
  }

  // on changes of input data
  ngOnChanges(changes: SimpleChanges){
      if(changes.executionDetails && !changes.executionDetails.firstChange){
      this.model.pipelineObject=changes['executionDetails'].currentValue;
      console.log('onchange:',this.model.pipelineObject);
    }
  }

  // get payload data for a pipeline id
  getPayloadData(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.pipelineService.getPayloadData(pipelineId).then((response: any[]) => {
        parent.model.pipelineData = response[0].pipelineData;
        fulfilled(true);
      }).catch((error) => {
        parent.toaster.failureWithMessage(error.message);
        parent.closeWindow();
        rejected(true);
      });
    });
  }

  // get keys of an object
  getKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  // add new variables
  addNewVariables() {
    const parent = this;
    parent.model.pipelineObject.pipeline.variables[''] = "";
  }

  // update variable name based on the variable type
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

  // update the value of a variable based on the key
  updateVariableValue(key, obj, event){
    console.log("setValue");
    obj[key] = event.target.value;
  }

  // update the variable item based on the type
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

    parent.model.pipelineData[parent.selectedVariable][newKey] = parent.model.pipelineData[previousType][name];
    delete parent.model.pipelineData[previousType][name];
  }

  // toggle confidential data and add the variable value to the confidential variable
  toggleConfidentialData(key:string,obj:object, variableType: string, event?:any){
    const parent =this;
    const pipelineDataInstance = JSON.parse(JSON.stringify(parent.model.pipelineData));
    pipelineDataInstance[variableType][key]=!pipelineDataInstance[variableType][key];
    parent.model.pipelineData=pipelineDataInstance;
  }

  // close the modal window
  closeWindow() {
    const parent = this;
    parent.close.emit('window closed');
  }

  // save the pipeline data
  onSave() {
    // passing object will propagate to parent component. and handle that in parent component
    const parent = this;
    delete parent.model.pipelineObject["pipelineId"];
    console.log(JSON.stringify(parent.model.pipelineObject));
    parent.save.emit(parent.model.pipelineObject);
    parent.closeWindow();
  }

  // filter input pipeline data to remove unwanted fields
  private filterInputPipelineData() {
    this.model.pipelineObject = JSON.parse(JSON.stringify(this.inputPipelineData));
    delete this.model.pipelineObject.pipeline.name;
    delete this.model.pipelineObject.pipeline.operator;
    delete this.model.pipelineObject.pipeline.runtime;
    delete this.model.pipelineObject.pipeline.flow;
    delete this.model.pipelineObject.pipeline.version;
    delete this.model.pipelineObject.pipeline.description;
    delete this.model.pipelineObject.pipeline.projectId;
  }


}
export interface Storage {
  value: string;
  viewValue: string;
}
export interface Variables {
  value: string;
  viewValue: string;
}

