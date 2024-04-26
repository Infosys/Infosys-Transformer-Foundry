/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ModelData } from 'src/app/data/model-data';
import { ModelService } from 'src/app/services/models.service';
import { DatePipe, Location } from '@angular/common';
import { LeaderFilterData } from 'src/app/data/leader-filter-data';

@Component({
  selector: 'app-model-details',
  templateUrl: './model-details.component.html',
  styleUrls: ['./model-details.component.scss']
})
export class ModelDetailsComponent implements OnInit {

  todayDate = new Date();
  model: any = {
    isDataLoaded: false,
    modelId: undefined,
    modelVersion: undefined,
    modelType: undefined,
    modelDetails: ModelData,
    modelName: "",
    metaDataHeight: 0,
    metaDataWidth: 0,
    apiError: "",
    benchMarkData: [],
    benchmarkCount: 0,
    modality:"",
    exeModelName:true,
    leaderDataFilter: new LeaderFilterData(this.datePipe.transform(this.todayDate, 'yyyy-MM-dd'), this.datePipe.transform(this.todayDate.setDate(this.todayDate.getDate() -30), 'yyyy-MM-dd'))
  }
  
  heightOffset = 292;
  widthOffset = 50;

  showSection = {
    modelDetails: true,
    modelParameters: true,
    quantitativeAnalysis: true,
    considerations: true
  }

  constructor(
    private datePipe: DatePipe,
    private route: ActivatedRoute,
    private service: ModelService,
    private location: Location
  ) { }

  //ngOnInit method used to get the modelId and modelType from the url and get the model data
  ngOnInit() {
    const parent = this;
    parent.resizeComponent();

    parent.route.params.subscribe(params => {
      parent.model.modelId = params['modelId'];
      parent.model.modelType = params['modelType'];
      parent.route.queryParamMap.subscribe(queryParams => {
        parent.model.modelVersion = queryParams.get('mv');
        parent.getModelData().then((values) => {
          parent.model.modelDetails = values;
          parent.model.modelName = values["metadata"]["modelDetails"]["displayName"];
          parent.model.leaderDataFilter.modelName = values["metadata"]["modelDetails"]["displayName"];
          parent.model.isDataLoaded = true;// else model doesn't load when leaderboard services are down
          parent.filterModality();
        }).catch((error) => {
          parent.model.apiError = error["statusText"];
          parent.model.isDataLoaded = true;
        });
      });
    });
  }

  //function to get the model data
  getModelData() {
    const modelState = history.state.modelData;
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      if (modelState) {
        console.log("Getting modelData from parent.", modelState);
        fulfilled(modelState);
        //dataloaded flag 
      } else {
        // If the data is not loaded, fetch it from the service and return a promise
        parent.service.getModelData(parent.model.modelId, parent.model.modelVersion)
          .then((response: any) => {
            fulfilled(response);
          })
          .catch((error) => {
            parent.model.apiError = error["statusText"];
            rejected(error);
          });
      }
    });
  }

  //function to filter the modality
  filterModality() {
    const parent = this;
    const url = 'assets/leadberboard-modality-data.json';
    fetch(url)
      .then(response => response.json())
      .then(leaderboardData => {
        let foundMatch = false;
        for (const entry of leaderboardData.leaderboard) {
          if (parent.model.leaderDataFilter.modelName === entry.modelName) {
            parent.model.modality = entry.modality;
            console.log(`Modality for ${parent.model.leaderDataFilter.modelName}: ${parent.model.modality}`);
            foundMatch = true;
            break;
          }
        }
        if (!foundMatch) {
          parent.model.modality = "NA";
          console.log(`No matching modelName found. Modality set to NA.`);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  //function to check the value is object
  isObject(value: any): boolean {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
  }

  //function to check the value is array
  isArray(value: any): boolean {
    return Array.isArray(value);
  }

  //function to check the value is string
  noSortCompareFn() {
    return 0;
  }

  //function to expand or collapse the section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
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
    parent.model.metaDataHeight = windowHeight - parent.heightOffset;
    parent.model.metaDataWidth = windowWidth - parent.widthOffset;
  }

}
