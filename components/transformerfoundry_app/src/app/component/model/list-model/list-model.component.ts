/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, Input, OnInit } from '@angular/core';
import { ModelData } from 'src/app/data/model-data';
import { Router } from '@angular/router';

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
  }

  //modelErrorMessage is used to display the error message
  @Input() modelErrorMessage: string

  public modelList: ModelData[];
  model = {
    isDataLoaded: true,
    height: 0,
    width: 0,
    modelsWithMetadata: [],
    modelsWithoutMetadata: []
  }
  heightOffset = 185;
  widthOffset = 30;

  private modelType = 'modelZoo';
  constructor(
    private router: Router) { }

  //ngOnInit method with the logic to resize the component dynamically
  ngOnInit(): void {
    const parent = this;
    console.log("modelListData", parent.modelListData);
    parent.resizeComponent();
  }

  //navigates to the list models screen and passes the model too.
  navigateToModelDetails(model: ModelData) {
    this.router.navigate(['/', this.modelType, model["id"]], { queryParams: { mv: model["version"] }, state: { modelData: model } });
  }

  //function to handle window resize
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  //function to resize the component
  private resizeComponent() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;

    parent.model.height = windowHeight - parent.heightOffset;
    parent.model.width = windowWidth - parent.widthOffset;
  }

  //function returns ngClass for status chip
  getClass(status: string): string {
    switch (status.toLowerCase()) {
      case 'graduated':
        return 'web-SecondaryGreen';
      case 'lab':
        return 'web-SecondaryOrange';
      case 'incubated':
        return 'web-SecondaryBlue';
      case 'registered':
        return 'web-SecondaryPink';
      default:
        return 'web-GreyLightBg';
    }
  }
}
