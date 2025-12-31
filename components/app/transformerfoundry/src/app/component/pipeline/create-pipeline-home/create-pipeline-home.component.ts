/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, HostListener } from "@angular/core";
import { PipelineServiceService } from "../../../services/pipeline-service.service";
import { ActivatedRoute, Router } from "@angular/router";
import { DataStorageService } from "../../../services/data-storage.service";
import { PipelineDetailsData } from "../../../data/pipeline-details-data";
import { MatTabChangeEvent } from "@angular/material/tabs";
import { PayloadData, PipelineData } from "src/app/data/payload-data";

@Component({
  selector: "app-create-pipeline-home",
  templateUrl: "./create-pipeline-home.component.html",
  styleUrls: ["./create-pipeline-home.component.scss"],
})
export class CreatePipelineHomeComponent implements OnInit {
  constructor(
    private pipelineService: PipelineServiceService,
    private route: ActivatedRoute,
    private storageService: DataStorageService,
    private router: Router
  ) {}

  // model object to store the UI data
  model: any = {
    nodePayload: new PayloadData(),
    pipelineData: new PipelineDetailsData(),
    isDataLoaded: false,
    pipelineId: "",
    executionData: {},
    isReadOnly: false,
    key: "",
    pipelineName: "",
    selectedTabIndex: "",
    projectId: "",
    confidentialData: new PipelineData(),
    height: 0,
    width: 0,
  };

  // height and width offset for each tab
  detailsHeightOffset = 250;
  flowHeightOffset = 165;
  summaryHeightOffset = 233;
  executionHeightOffset = 295.5;
  detailsWidthOffset = 30;
  summaryWidthOffset = 65;
  executionWidthOffset = 32;

  // onInit method to load the data on load of the page
  ngOnInit(): void {
    const parent = this;
    parent.model.isDataLoaded = false;

    parent.model.selectedTabIndex =
      parent.storageService.getData().pipelineTabIndex;
    // parent.model.projectId = parent.storageService.getData().projectId;
    parent.updateProjectId();

    parent
      .getPipelineIdFromUrl()
      .then((pipelineId) => {
        const promise2 = parent.getPayloadData(pipelineId);
        const promise1 = parent.getPipelineDefinition(pipelineId);
        const promise3 = parent.getExecutionData(pipelineId);
        const promise4 = parent.getRecreateMode();
        const promise5 = parent.getGlobalTemplateMode();

        Promise.all([promise1, promise2, promise3, promise4, promise5])
          .then((values) => {
            console.log("Promise values", values);

            if (this.model.isReadOnly === false) {
              delete parent.model.pipelineData["pipelineId"];
              parent.model.pipelineId = "";
            }
            parent.model.isDataLoaded = true;
          })
          .catch(() => {
            if (this.model.isReadOnly === false) {
              delete parent.model.pipelineData["id"];
              parent.model.pipelineId = "";
            }
              parent.manageRecreateData();
            parent.model.isDataLoaded = true;
          });
      })
      .catch(() => {
        if (this.model.isReadOnly === false) {
          delete parent.model.pipelineData["pipelineId"];
          parent.model.pipelineId = "";
        }
        parent.model.isDataLoaded = true;
      });
    parent.resizeChildComponents();
  }

  // method to manage the data for the recreate mode
  manageRecreateData() {
    const parent = this;
    delete parent.model.pipelineData?.status;
    delete parent.model.pipelineData?.createdBy;
    delete parent.model.pipelineData?.createdOn;
    delete parent.model.pipelineData?.isDeleted;
    delete parent.model.pipelineData?.updatedBy;
    delete parent.model.pipelineData?.modifiedOn;
    delete parent.model.pipelineData?.tenantName;

    if (parent.model.pipelineData.pipeline.volume === null) {
      delete parent.model.pipelineData.pipeline.volume;
    }

    for (let key in parent.model.pipelineData.pipeline.flow) {
      delete parent.model.pipelineData.pipeline.flow[key].inputArtifacts;
    }
  }

  // method to destroy the component and set the tab index to 0
  ngOnDestroy(): void {
    this.setTabIndex(0);
  }

  // method to update the project id from the url
  updateProjectId() {
    const parent = this;
    let urlsegment = window.location.href.split("/");
    let index = urlsegment.indexOf("projects");
    if (index !== -1 && index + 1 < urlsegment.length) {
      parent.model.projectId = urlsegment[index + 1];
    }
    this.model.pipelineData.projectId = parent.model.projectId;
  }

  // method to handle the window resize event
  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.resizeChildComponents();
  }

  // method to handle the tab change event
  onTabChange(event: MatTabChangeEvent) {
    this.setTabIndex(event.index);
    this.resizeChildComponents();
  }

  // method to handle the pipeline name change event
  onPipelineDetail(pipelinedtData: any) {
    if (!pipelinedtData.pipeline?.flow) {
      pipelinedtData.pipeline.flow =
        this.model.pipelineData?.pipeline?.flow || {};
    }
    this.model.pipelineData = pipelinedtData;
    console.log(pipelinedtData);
  }

  // store the constructed payload data and share it to the child components
  onNodePayload(payload: any) {
    this.model.nodePayload.flowData = payload.flowData;
    console.log(this.model.nodePayload);
  }

  // store the flow section data and share it to the child components
  onFlowData(flowSectionData: any) {
    this.model.pipelineData.pipeline["flow"] = flowSectionData;
  }

  // store the confidential info and share it to the child components
  onConfidentialData(confidentialFlag: any) {
    this.model.confidentialData = confidentialFlag;
  }

  // store the pipeline id and share it to the child components
  onCreatePipeline(pipelineId: any) {
    this.model.isReadOnly = true;
    this.model.pipelineId = pipelineId;
  }

  // store the execution data and share it to the child components
  onExecutionData(data: any) {
    this.model.executionData = data;
  }

  // method to get the payload data from the api
  getPayloadData(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.pipelineService
        .getPayloadData(pipelineId)
        .then((response: any[]) => {
          parent.model.nodePayload = response[0];
          parent.model.confidentialData = response[0].pipelineData;
          fulfilled(true);
        })
        .catch(() => {
          rejected();
        });
    });
  }

  // method to get the pipeline definition of the id from the api
  getPipelineDefinition(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.pipelineService
        .getPipelineDefinition(pipelineId)
        .then((response: any[]) => {
          parent.model.pipelineData = response;
          console.log(this.model.pipelineName);
          fulfilled(true);
        })
        .catch(() => {
          rejected();
        });
    });
  }

  // method to get the pipeline id from the url
  getPipelineIdFromUrl() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.route.params.subscribe((params) => {
        if (params["id"]) {
          parent.model.isReadOnly = true;
          parent.model.pipelineId = params["id"];
          fulfilled(params["id"]);
        } else {
          rejected(true);
        }
      });
    });
  }

  // method to check if the page is in recreate mode from the url
  getRecreateMode() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      try {
        parent.route.queryParamMap.subscribe((queryParams) => {
          if (queryParams.has("rc") && queryParams.get("rc") === "true") {
            parent.model.isReadOnly = false;
            fulfilled(true);
          }
        });
      } catch (error) {
        rejected(true);
      }
    });
  }

  getGlobalTemplateMode() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      try {
        parent.route.queryParamMap.subscribe((queryParams) => {
          if (queryParams.has("gt") && queryParams.get("gt") === "true") {
            parent.model.isReadOnly = false;
            fulfilled(true);
          }
        });
      } catch (error) {
        rejected(true);
      }
    });
  }

  // method to get the execution data from the api
  getExecutionData(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      // if the url has the query params "rc=true", then assign executionData = [], else call the api
      if (parent.router.url.includes("rc=true") ||
          parent.router.url.includes("gt=true") ){
        parent.model.executionData = [];
        fulfilled(true);
      } else {
        parent.pipelineService
          .getExecutionData(pipelineId)
          .then((response: any[]) => {
            parent.model.executionData = response;
            fulfilled(true);
          })
          .catch(() => {
            rejected();
          });
        console.log("ELSE BLOCK Called");
      }
    });
  }

  // method to set the tab index in the local storage
  private setTabIndex(index) {
    const parent = this;
    const storedData = parent.storageService.getData();
    storedData.pipelineTabIndex = index;
    parent.storageService.setData(storedData);
  }

  // method to resize the child components based on the window size
  private resizeChildComponents() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    const tabIndex = parent.storageService.getData().pipelineTabIndex;
    if (tabIndex == 0) {
      this.model.height = windowHeight - this.detailsHeightOffset;
      this.model.width = windowWidth - this.detailsWidthOffset;
    }
    if (tabIndex == 1) {
      this.model.height = windowHeight - this.flowHeightOffset;
    }
    if (tabIndex == 2) {
      this.model.height = windowHeight - this.summaryHeightOffset;
      this.model.width = windowWidth - this.summaryWidthOffset;
    }
    if (tabIndex == 3) {
      this.model.height = windowHeight - this.executionHeightOffset;
      this.model.width = windowWidth - this.executionWidthOffset;
    }
  }
}
