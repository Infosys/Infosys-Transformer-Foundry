/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Compute, DeployedModelData, ModelSpec } from 'src/app/data/deploy-model-data';
import { ModelService } from 'src/app/services/models.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';

@Component({
  selector: 'app-model-deploy-details',
  templateUrl: './model-deploy-details.component.html',
  styleUrls: ['./model-deploy-details.component.scss']
})
export class ModelDeployDetailsComponent implements OnInit {
  // event emitter for the deploy data
  @Output() deployDt = new EventEmitter<{}>();

  // input values for the height and width of the tab
  @Input() height: number;
  @Input() width: number;

  // input deploy model data values
  @Input()
  set inputDeployModelData(inputDeployModelData: DeployedModelData) {
    this.model.deployModelData = inputDeployModelData;
    console.log(this.model.deployModelData);
  }

  // input model name, endpoint name, model id and endpoint id
  @Input() 
  set inputModelName(inputModelName: string) {
    this.model.modelName = inputModelName;
  }
  @Input() 
  set inputEndpointName(inputEndpointName: string) {
    this.model.endpointName = inputEndpointName;
  }
  @Input() 
  set inputModelId(inputModelId: string) {
    this.model.deployModelData.modelId = inputModelId;
  }
  @Input()
  set inputEndpointId(endpointId: string) {
    this.model.deployModelData.endpointId = endpointId;
    console.log("receiving endpoint id", this.model.deployModelData.endpointId)
  }
  
  // model object to store the UI values
  model: any = {
    deployModelData: new DeployedModelData(),
    endpointName: '',
    modelName: '',
    isBtnDisabled: false,
    isReadOnly:false,
    isDataLoaded: true,
  }

  // show section object to show and hide the sections
  showSection = {
    inferenceSpec:true,
    containerResourceConfig:true,
    modelUris:true,
    modelName:'',
    storage: true
  }

  // serving framework, type and storage values
  ServingFramework: ServingFramework[] = [
    { value: "Custom", viewValue: "Custom" },
    { value: "Triton", viewValue: "Triton" },
    { value: "DJL", viewValue: "DJL" },
    // { value: "Huggingface TGI", viewValue: "Huggingface TGI" }
  ];
  Type: Type[] = [
    { value: "CPU", viewValue: "CPU" },
    { value: "GPU", viewValue: "GPU" },
  ];
  storage: Storage[] = [
    { value: "INFY_AICLD_MINIO", viewValue: "INFY_AICLD_MINIO" },
    { value: "INFY_AICLD_NUTANIX", viewValue: "INFY_AICLD_NUTANIX" }
  ];
  // selectedServingFramework: string = this.ServingFramework[0].value;
  selectedType: string = this.Type[0].value;

  // constructor  
  constructor(
    private modelService: ModelService,
    private toaster: ToasterServiceService,
    private modalService: NgbModal
  ) { }


  ngOnInit(): void {
  }

  // ngOnChanges to check the changes in the input values
  ngOnChanges(changes: SimpleChanges) {
    console.log("checking changes in update details", this.model.deployModelData);
    if (changes.inputDeployModelData && !changes.inputDeployModelData.firstChange) {
      console.log("calling to emit update details", this.model.deployModelData);
      this.handleDetailChanges();
    }
    if(changes.isBtnDisabled && !changes.isBtnDisabled.firstChange){
      this.model.isBtnDisabled = changes.isBtnDisabled.currentValue;
    }
  }

  // function to add GB to the memory value
  addGB(){
    let memoryValue = this.model.deployModelData.inferenceConfig.inferenceSpec.containerResourceConfig.computes[0].memory;
    let isNumeric = /^[0-9]+$/.test(memoryValue);
    if(isNumeric && memoryValue !== ''){
      this.model.deployModelData.inferenceConfig.inferenceSpec.containerResourceConfig.computes[0].memory = memoryValue + 'GB';
    }
  }

  // toggle section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
  }

  // add model specfication
  addModel(){
    this.model.deployModelData.inferenceConfig.inferenceSpec.modelSpec.push(new ModelSpec());
  }

  // remove model specification
  removeModel(index: number){
    this.model.deployModelData.inferenceConfig.inferenceSpec.modelSpec.splice(index,1);
  }

  // deploy model
  deployModel() {
    const parent = this;
    parent.model.isReadOnly = true;
    parent.model.isBtnDisabled = true;
    try {
      parent.modelService.createModelDeployment(parent.model.deployModelData)
        .then(
          (responseData: any) => {
            parent.model.isReadOnly = true;
            parent.model.isBtnDisabled = false;
            parent.toaster.success(114);
            console.log("ResponseData:", responseData);
          }).catch(
            data => {
              parent.model.isReadOnly = true;
              parent.model.isBtnDisabled = false;
              if (data) {
                parent.toaster.failureWithMessage(data?.["details"]?.[0]?.message || data?.["detail"]?.message || data?.Error);
              } else {
                parent.toaster.failure(104);
              }
            });
    } catch {
      parent.toaster.failure(104);
    }
  }

  // open confirm dialog
  openConfirmDialog(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });

  }

  // handle detail changes
  private handleDetailChanges() {
    const parent = this;
    parent.deployDt.emit(parent.model.deployModelData);
    console.log("emiting values", parent.model.deployModelData);
  }

}
export interface ServingFramework {
  value: string;
  viewValue: string;
}
export interface Type {
  value: string;
  viewValue: string;
}
export interface Storage {
  value: string;
  viewValue: string;
}
