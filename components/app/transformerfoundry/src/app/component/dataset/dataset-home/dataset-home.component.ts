
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { Component, HostListener, OnInit } from "@angular/core";
import { PayloadData, PipelineData } from "src/app/data/payload-data";
import { DatasetService } from "src/app/services/dataset.service";
import { PipelineDetailsData } from "../../../data/pipeline-details-data";
import { ActivatedRoute } from "@angular/router";
import { COMMA, ENTER } from "@angular/cdk/keycodes";

@Component({
  selector: "app-dataset-home",
  templateUrl: "./dataset-home.component.html",
  styleUrls: ["./dataset-home.component.scss"],
})
export class DatasetHomeComponent implements OnInit {
  constructor() {}

  model = {
    height: 0,
    width: 0,
    data: {},
    dataStorage: {},
    // isDataLoaded: false,
    // pipelineData: new PipelineDetailsData(),
    // confidentialData: new PipelineData(),
  };
  

  // offset values for height and width
  widthOffset = 32;
  heightOffset = 270.5;

  ngOnInit(): void {
    this.resizeChildComponents();
    // this.model.data = this.data;
  //   this.model.dataStorage = this.dataStorage;
  }
  // function to handle the window resize event
  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.resizeChildComponents();
  }

  // function to resize the child components
  private resizeChildComponents() {
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    this.model.height = windowHeight - this.heightOffset;
    this.model.width = windowWidth - this.widthOffset;
  }

  // onPipelineDetail(pipelinedtData: any) {
  //   if (!pipelinedtData.pipeline?.flow) {
  //     pipelinedtData.pipeline.flow =
  //       this.model.pipelineData?.pipeline?.flow || {};
  //       console.log("pepedatare",pipelinedtData);
  //   }
  //   this.model.pipelineData = pipelinedtData;
  //   console.log("elrf",pipelinedtData);
  // }
}
