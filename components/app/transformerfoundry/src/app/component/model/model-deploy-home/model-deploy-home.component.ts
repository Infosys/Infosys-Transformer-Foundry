/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, OnInit } from "@angular/core";
import { ModelService } from 'src/app/services/models.service';
import { ActivatedRoute } from '@angular/router';
import { DataStorageService } from "src/app/services/data-storage.service";
import { MatTabChangeEvent } from "@angular/material/tabs";
import { UpdateModelData } from "src/app/data/update-model-data";
import { Location } from "@angular/common";
import { EndpointData } from "src/app/data/endpoint-data";
import { DeployedModelData } from "src/app/data/deploy-model-data";

@Component({
  selector: 'app-model-deploy-home',
  templateUrl: './model-deploy-home.component.html',
  styleUrls: ['./model-deploy-home.component.scss']
})
export class ModelDeployHomeComponent implements OnInit {

  constructor(
    private route: ActivatedRoute, 
    private storageService: DataStorageService,
    private modelService: ModelService
  ) { }

  // model object to store the UI values
  model: any = {
    updateModelData: new UpdateModelData(),
    endpointData: new EndpointData(),
    deployData: new DeployedModelData(),
    selectedTabIndex: '',
    modelName:'',
    height: 0,
    width: 0,
    modelId: '',
    projectId: '',
    modelVersion: '',
    artifacts: {},
    endpointId: '',
    endpointName:'',
  };

  // offset values for height and width
  widthOffset=32;
  heightOffset=270.5;
  
  // on init function
  ngOnInit(): void {
    const parent = this;
    parent.model.selectedTabIndex = (parent.storageService.getData()).deployModelTabIndex;
    parent.getModelName();
    parent.getModelDetails();
    parent.resizeChildComponents();
  }

  // get model details for the selected model
  getModelDetails(){
    const parent = this;
    parent.route.params.subscribe(params => {
      parent.model.projectId = params['pid'];
      parent.model.modelId = params['modelId'];
      parent.route.queryParamMap.subscribe(queryParams => {
        parent.model.modelVersion = queryParams.get('mv');
        parent.modelService.getModelData(parent.model.modelId, parent.model.modelVersion)
        .then((response: any) => {
          parent.model.artifacts = response['artifacts'];
          parent.model.modelName = response['name'];
        })
        .catch((error) => {
          parent.model.artifacts = {};
          parent.model.modelName = '';
        });
      });
    });
  }

  // function to update the model details
  onUpdateModelDetail(modeldtData: any) {
    this.model.updateModelData = modeldtData;
    console.log("home receiving the date", this.model.updateModelData, modeldtData);
  }

  // function to update the endpoint details
  onEndpointDetailChanges(endptData: any){
    this.model.endpointData = endptData;
    console.log("home receiving and storing the endpoint data", this.model.endpointData, endptData);
  }

  // function to update the endpoint id
  onEndpointId(endptData: any){
    this.model.endpointId = endptData.id;
    this.model.deployData.endpointId = endptData.id;
    this.model.endpointName = endptData.name;
  }

  // function to update the deploy details
  onDeployDetailChanges(deployData: any){
    this.model.deployData = deployData;
  }

  // on destroy function, to set the tab index to 0
  ngOnDestroy(): void {
    this.setTabIndex(0);
  }

  // function to handle the window resize event
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeChildComponents();
  }

  // function to handle the tab change event
  onTabChange(event: MatTabChangeEvent) {
    this.setTabIndex(event.index);
    this.resizeChildComponents();
  }

  // function to handle the next tab event
  nextTab(event: any) {
    console.log(event);
    this.setTabIndex(event);
    this.resizeChildComponents();
  }

  // function to update the endpoint id and name
  deployDetails(event: any) {
    console.log(event);
    this.model.endpointId = event.id;
    this.model.endpointName = event.name;
  }

  // function to get the model name from the query params
  getModelName(){
    const parent=this;
    this.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('mn')) {
        parent.model.modelName = queryParams.get('mn');
      }
      else{
        parent.model.modelName ='';
      }
    });
  }

  // function to set the tab index
  private setTabIndex(index) {
    const parent = this;
    const storedData = parent.storageService.getData();
    storedData.deployModelTabIndex = index;
    parent.storageService.setData(storedData);
    parent.model.selectedTabIndex = index;
  }

  // function to resize the child components
  private resizeChildComponents() {
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    this.model.height = (windowHeight - this.heightOffset);
    this.model.width = (windowWidth - this.widthOffset);
  }

}
