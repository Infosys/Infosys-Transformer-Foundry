/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
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
  // today date 
  todayDate = new Date();

  // model object to store the UI values
  model: any = {
    isDataLoaded: false,
    projectId: undefined,
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
  
  id: number;
  list: any;

  // offset values for resizing the component
  heightOffset = 292;
  widthOffset = 50;

  // flag to show/hide the sections
  showSection = {
    modelDetails: true,
    modelParameters: true,
    quantitativeAnalysis: true,
    considerations: true
  }

  // constructor to inject the required services
  constructor(
    private datePipe: DatePipe,
    private route: ActivatedRoute,
    private service: ModelService,
    private location: Location
  ) { }

  // onInit function to load the model data
  ngOnInit() {
    const parent = this;
    parent.resizeComponent();

    parent.route.params.subscribe(params => {
      parent.model.projectId = params['pid'];
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

  // function to filter the leaderboard data based on the model
  filterByModel(leaderBoardData) {
    const parent = this;
    const filteredData = leaderBoardData.filter((item) => {
      if (item["Model"].toLowerCase() === parent.model.modelDetails['metadata'].modelDetails.displayName.toLowerCase()) {
        console.log("XXX", item["Model"].toLowerCase(), parent.model.modelDetails['metadata'].modelDetails.displayName.toLowerCase());
        return true;
      } else {
        return false;
      }
    });

    return filteredData;
  }

  // function to filter the leaderboard data based on the modaity
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

  // function to resize the component based on the window size
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  // function to resize the component based on the window size
  private resizeComponent() {
    const parent = this;

    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    parent.model.metaDataHeight = windowHeight - parent.heightOffset;
    parent.model.metaDataWidth = windowWidth - parent.widthOffset;
  }

  // function to get the model data
  getModelData() {
    const modelState = history.state.modelData;
    const parent = this;
    return new Promise(function (fulfilled, rejected) {


      if (modelState) {
        console.log("Getting modelData from parent.", modelState);
        fulfilled(modelState);
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

  // function to check if the value is an object
  isObject(value: any): boolean {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
  }

  // function to check if the value is an array
  isArray(value: any): boolean {
    return Array.isArray(value);
  }

  // function to sort
  noSortCompareFn() {
    return 0;
  }

  // function to get the length of the object
  getLength(keyval: []): any {
    return keyval.length;
  }

  // function to go back to the previous page
  goBack() {
    this.location.back();
  }

  // function to toggle the section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
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
