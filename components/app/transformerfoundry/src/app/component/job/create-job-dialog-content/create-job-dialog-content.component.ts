/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { Compute, ExecuteTrailData, RunArgument } from "src/app/data/execute-trail-data";
import { JobDetailsData } from "src/app/data/job-details-data";
import { ModelService } from "src/app/services/models.service";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { UtilityService } from "src/app/services/utility.service";

@Component({
  selector: "app-create-job-dialog-content",
  templateUrl: "./create-job-dialog-content.component.html",
  styleUrls: ["./create-job-dialog-content.component.scss"],
})
export class CreateJobDialogContentComponent implements OnInit {
  // input job details data
  @Input() inputJobDetailsData: JobDetailsData;
  // trial count
  @Input() trialCount: number;
  // close and save event emitters
  @Output() close = new EventEmitter<string>();
  @Output() save = new EventEmitter<object>();

  // store the trial id
  trialId: string;
  // show the load icon
  showLoadIcon: boolean = false;

  model: any = {
    trialData: undefined,
  }
  constructor(
    private utilityService: UtilityService,
    private modelService: ModelService,
    private toaster: ToasterServiceService
  ) { }

  // on init
  ngOnInit(): void {
    this.filterInputJobData()
  }

  // close the dialog window
  closeWindow() {
    const parent = this;
    parent.close.emit('window closed');
  }

  // execute the trial
  executeTrial() {
    const parent = this;
    parent.showLoadIcon = true;
    parent.model.isDataLoaded = false;
    console.log(parent.model.trialData);
    try {
      parent.modelService.postTrailDetails(parent.model.trialData)
        .then(
          responseData => {
            parent.model.isDataLoaded = true;
            parent.toaster.success(110);
            parent.trialId = responseData['id'];
            console.log(parent.trialId, parent.model.trialData.name);
            if (parent.utilityService.isStringHasValue(parent.trialId))
                parent.closeWindow();
            parent.showLoadIcon = false;
            parent.save.emit();
          }).catch(error => {
            parent.toaster.failureWithMessage(parent.utilityService.getErrorMessage(error));
            parent.model.isDataLoaded = true;
            parent.showLoadIcon = false;
          });
      console.log(this.showLoadIcon);
    }
    catch (error) {
      parent.toaster.failureWithMessage(parent.utilityService.getErrorMessage(error));
      parent.model.isDataLoaded = true;
      this.showLoadIcon = false;
    }
  }

  // add the compute
  addComputes() {
    // console.log(this.model.trailData.resourceConfig.computes.length)
    this.model.trialData.resourceConfig.computes.push(new Compute('CPU', NaN, '', NaN));
  }

  // add the run arguments
  addRunArguments() {
    this.model.trialData.runArguments[''] = '';
  }

  // delete the compute
  deleteCompute(index) {
    this.model.trialData.resourceConfig.computes.splice(index, 1);
  }

  // filter the input job data
  private filterInputJobData() {
    console.log(this.inputJobDetailsData);
    this.model.trialData = new ExecuteTrailData(this.inputJobDetailsData.projectId, this.inputJobDetailsData.id);
    this.model.trialData.name = this.inputJobDetailsData.name;
    this.model.trialData.modelName = this.inputJobDetailsData.name;
    this.model.trialData.modelVersion = "1"
    this.model.trialData.experimentConfig.name = this.inputJobDetailsData.name;
    this.model.trialData.description = this.inputJobDetailsData.description;
    this.inputJobDetailsData.jobArguments.forEach(element => {
      this.model.trialData.runArguments.push({ name: element.name, argValue: element.defaultVal });
    });
    this.model.trialData.resourceConfig.computes = [new Compute()];
    this.generateTrialName()
    console.log(this.model.trialData);
  }

  // generate the trial name
  private generateTrialName() {
    this.model.trialData.name = this.model.trialData.name + '-' + (this.trialCount + 1);
  }
}

