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
import { JobDetailsData } from "src/app/data/job-details-data";

@Component({
  selector: "app-create-job-home",
  templateUrl: "./create-job-home.component.html",
  styleUrls: ["./create-job-home.component.scss"],
})
export class CreateJobHomeComponent implements OnInit {
  constructor(private myService: ModelService, private route: ActivatedRoute, private storageService: DataStorageService) { }

  // public data:JobDetailsData;

  model: any = {
    jobDetails: new JobDetailsData(),
    // plTemplateId: '',
    pipelineId:'',
    jobName: '',
    selectedTabIndex: '',
    isDataLoaded: false,
    isReadOnly: true,
    height: 0,
    width: 0,
    trailData: undefined,
    projectId:'',
    experimentId:0,
    runName: ''
  };
  experimentName='';

  // height and width offset for the tabs in job fine tuning module
  experimentalDetailsHeightOffset = 250;
  summaryHeightOffset = 233;
  trialHeightOffset = 305;
  experimentalDetailsWidthOffset = 30;
  summaryWidthOffset = 65;
  trialWidthOffset = 32;

  // on init fill the tabs with values corresponding to the project id, pipeline id, experiment id.
  ngOnInit(): void {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.checkReadOnlyStatus();

    parent.model.selectedTabIndex = (parent.storageService.getData()).jobTabIndex;
    parent.resizeChildComponents();
    parent.updateProjectId();
    parent.getPipelineIdFromUrl().then((pipelineId) => {
      if(pipelineId !== 'null' && pipelineId !== 'undefined'){       
      const promise1 = parent.getPlById(pipelineId);

      Promise.all([promise1]).then((values) => {
        parent.model.isDataLoaded = true;
        const promise2 = parent.getTrialList();
        Promise.all([promise2]).then((values) => {
          parent.model.isTrialDataLoaded = true;
        }).catch(() => {
          parent.model.isTrialDataLoaded = true;
        })
      }).catch(() => {
        parent.model.isDataLoaded = true;
      });
    }
    else{
      parent.model.isDataLoaded = true;
    }
    }).catch(() => {
      parent.model.isDataLoaded = true;
    });
  }

  // on destroy set the tab index to 0
  ngOnDestroy(): void {
    this.setTabIndex(0);
  }

  // on resize of the window, resize the child components
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeChildComponents();
  }

  // on tab change set the tab index
  onTabChange(event: MatTabChangeEvent) {
    this.setTabIndex(event.index);
    this.resizeChildComponents();
  }

  // set the value for job details
  onJobDetails(jobDetails: any) {
    this.model.jobDetails = jobDetails;
    console.log('onJobDetails',jobDetails);
  }

  // once pipeline created, set the pipeline id
  onCreatePipeline(pipelineId: any) {
    if (pipelineId) {
      this.model.isReadOnly = true;
      this.model.jobDetails.id = pipelineId;
    }
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

  // get the pipeline details by pipeline id
  getPlById(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.myService.getPlById(pipelineId).then((response: JobDetailsData) => {
        parent.model.jobDetails = response;
        parent.model.jobDetails.originalName = response.name;
        parent.model.jobDetails.id = parent.model.isReadOnly ? parent.model.jobDetails.id : '';
        parent.model.jobDetails.jobArguments.forEach(element => {
          if(element['name'] == "mlflow_exp_name")
          {
            parent.model.runName = element['defaultVal'];
          }
        });

        console.log(parent.model.jobDetails);
        fulfilled(true);
      }).catch(error => {
        rejected(true);
      });
    });
  }

  // check if the job is read only
  checkReadOnlyStatus() {
    this.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('rc') && queryParams.get('rc') === 'true') {
        this.model.isReadOnly = false;
      } else {
        this.model.isReadOnly = true;
      }
    });
  }

  // get the trial list
  getTrialList() {
    const parent = this;
    if (parent.model.projectId !== '' && parent.model.jobDetails.id !== '') {
      return new Promise(function (fulfilled, rejected) {
        parent.myService.getTrialList(parent.model.projectId, parent.model.jobDetails.id)
          .then((responseData: any[]) => {
            parent.model.trailData = responseData['trials'];
            fulfilled(true);
          }).catch(() => {
            rejected(true)
          });
      });
    }
  }

  // get the pipeline id from the url
  getPipelineIdFromUrl() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.route.params.subscribe(params => {
        if (params['id']) {
          parent.model.pipelineId = params['id'];
          fulfilled(params['id'])
        } else {
          rejected(true)
        }
      });
    });
  }

  // If we want to fetch experimentId from experimentName we can use below method | Uncomment above code related to this 
  getExperimentId(experimentName) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
        parent.myService.getExperimentId(experimentName).then((responseData:any) => {
            let experimentData = responseData
            parent.model.experimentId=experimentData["experiments"]["experiment_id"];
            console.log("expid",parent.model.experimentId);
            fulfilled(true);
        }).catch(() => {
            rejected(true);
        });
    });
  }

  // set the tab index
  private setTabIndex(index) {
    const parent = this;
    const storedData = parent.storageService.getData();
    storedData.jobTabIndex = index;
    parent.storageService.setData(storedData);
  }

  // resize the child components
  private resizeChildComponents() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    const tabIndex = (parent.storageService.getData()).jobTabIndex;

    if (tabIndex == 0) {
      this.model.height = (windowHeight - this.experimentalDetailsHeightOffset);
      this.model.width = (windowWidth - this.experimentalDetailsWidthOffset);
    }
    if (tabIndex == 1) {
      this.model.height = (windowHeight - this.summaryHeightOffset);
      this.model.width = (windowWidth - this.summaryWidthOffset);
    }
    if (tabIndex == 2) {
      this.model.height = (windowHeight - this.trialHeightOffset);
      this.model.width = (windowWidth - this.trialWidthOffset);
    }
  }
}
