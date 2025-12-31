/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, Input, OnInit } from '@angular/core';
import { ModelData } from 'src/app/data/model-data';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-list-model',
  templateUrl: './list-model.component.html',
  styleUrls: ['./list-model.component.scss']
})
export class ListModelComponent implements OnInit {
  //modelListData is the input to the component which is used to display the model list
  @Input() 
  set modelListData(modelListData: any){
    this.model.modelsWithMetadata = modelListData.filter(modelItem => modelItem.metadata?.modelDetails != undefined || null);
    this.model.modelsWithoutMetadata = modelListData.filter(modelItem => modelItem.metadata?.modelDetails == undefined || null);
    this.model.isDataLoaded = true;
  }

  //modelErrorMessage is used to display the error message
  @Input() modelErrorMessage: string

  public modelList: ModelData[];
  model = {
    isDataLoaded: false,
    projectId: undefined,
    data: [],
    height: 0,
    width: 0,
    projectName: '',
    isProjectModel: false,
    selectedModel: '',
    modelsWithMetadata: [],
    modelsWithoutMetadata: []
  }
  heightOffset = 185;
  widthOffset = 30;

  modelType = undefined;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
  ) { }

  //ngOnInit method with the logic to resize the component dynamically
  ngOnInit(): void {
    const parent = this;
    console.log("modelListData", parent.modelListData);

    // const localStorage = parent.storageService.getData();
    let modelparam = undefined;
    parent.route.params.subscribe(params => {
      modelparam = params['models'];
      parent.model.projectId = params['pid'];
      console.log("AAAAA", parent.model.projectId);
      // localStorage.projectId = params['pid'];
      parent.modelType = modelparam == 'models' ? 'models' : 'modelZoo';
      parent.model.isProjectModel = modelparam == 'models' ? true : false;
      if(parent.modelType == 'modelZoo')
        parent.filterModels();
      parent.model.selectedModel = parent.modelType;
      // parent.getModelList(modelparam == 'models' ? parent.model.projectId : '');
    });
    parent.resizeComponent();
    parent.updateProjectName();
  }

  // filter models to exclude models whose provider is not aicloud when inside the the project
  filterModels(){
    const parent = this;
    if(parent.model.projectId !== undefined){
      parent.model.modelsWithMetadata = parent.model.modelsWithMetadata.filter(model => model.metadata.modelDetails.customTags[1].tags.toLowerCase() === 'aicloud');
    }
  }

  //navigates to the list models screen and passes the model too.
  navigateToModelDetails(model: ModelData) {
    if (this.isProjectSelected()) {
      this.router.navigate(['/projects', this.model.projectId, this.modelType, model["id"]], { queryParams: { mv: model["version"], pn: this.model.projectName }, state: { modelData: model, } });
    } else {
      this.router.navigate(['/', this.modelType, model["id"]], { queryParams: { mv: model["version"] }, state: { modelData: model } });
    }
  }

  // function to check if project is selected
  isProjectSelected() {
    return this.model.projectId != undefined;
  }

  // function to check if model is selected
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  // resize the component based on the window size
  private resizeComponent() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;

    parent.model.height = windowHeight - parent.heightOffset;
    parent.model.width = windowWidth - parent.widthOffset;
  }

  // function to update the project name
  private updateProjectName() {
    const parent = this;
    this.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else {
        parent.model.projectName = '';
      }
    });
  }

  // function to disable the deploy button based on the status
  deployDisabled(status){
    const parent = this;
    var projectId = ''
    parent.route.params.subscribe(params => {
      projectId = params['pid'];
    });
    if( projectId!=='' && projectId!==undefined && projectId!==null){ 
      if(status === 'Registered' || status === 'Graduated' || status === 'Lab' || status === 'Incubated' || status === 'Created'){
        return false;
      } 
      else if (status === 'Deployed' || status ==='In Progress'){
        return true;
      } 
    }
    else
    {
      return true;
    }
  }
  
  //function returns ngClass for status chip
  getClass(status: string): string {
    switch (status.toLowerCase()) {
      case 'graduated':
        return 'color-Green';
      case 'lab':
        return 'color-Pink';
      case 'incubated':
        return 'color-blue';
      case 'registered':
        return 'color-Red';
      default:
        return 'color-Grey';
    }
  }
}
