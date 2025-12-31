/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, OnInit } from '@angular/core';
import { ProjectDetailsData } from 'src/app/data/project-details-data';
import { ProjectServiceService } from 'src/app/services/project-service.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';
import { ConfigDataHelper } from 'src/app/utils/config-data-helper';
import { CONSTANTS } from 'src/app/common/constants';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { BaseComponent } from 'src/app/base.component';
import { SessionService } from 'src/app/services/session.service';
import { NgModel } from '@angular/forms';
import { DataStorageService } from 'src/app/services/data-storage.service';
import { UtilityService } from 'src/app/services/utility.service';

@Component({
  selector: 'app-create-project',
  templateUrl: './create-project.component.html',
  styleUrls: ['./create-project.component.scss']
})
export class CreateProjectComponent extends BaseComponent implements OnInit {

  // Constructor
  constructor(
    private myService: ProjectServiceService,
    private toaster: ToasterServiceService,
    public configDataHelper: ConfigDataHelper,
    private route: ActivatedRoute,
    private router:Router,
    private modalService: NgbModal,
    public sessionService: SessionService,
    public storageService: DataStorageService,
    public utilityService: UtilityService
  ) {
    super(sessionService, configDataHelper);
  }

  // model object to store the data
  model: any = {
    projectDetails: new ProjectDetailsData(this.configDataHelper.getValue(CONSTANTS.CONFIG.TENANT_ID)),
    isReadOnly: false,
    projectId: undefined,
    buttonName: 'Create',
    isBtnDisabled: false,
    height:0,
    width:0,
  };

  // offset values for height and width
  heightOffset = 285.5;
  widthOffset = 33;

  // onInit method
  ngOnInit(): void {
    const parent = this;
    parent.route.params.subscribe(params => {
      parent.model.projectId = params['pid'];
    });
    const urlSegments = parent.router.url.split('/');
    if (parent.model.projectId !== undefined) {
      parent.model.isReadOnly = urlSegments.includes('edit')? false:true ;
      parent.getProjectDetailsByID();
      parent.model.buttonName = "Update";
    }
    this.resizeComponent();
    this.isUpdateAllowed();
  }

  // Method to filter the input to allow only valid characters
  onInput(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    const regexPattern = /^[a-z0-9-]+$/;
    const currentValue = inputElement.value;

    // Filter the input to allow only valid characters
    const filteredValue = currentValue.split('').filter((char) => regexPattern.test(char)).join('');

    // Update the input value with the filtered value
    inputElement.value = filteredValue;
    this.model.projectDetails.name = filteredValue;
  }

  // Method to add user details
  addUserDetails() {
    const parent = this;
    parent.model.projectDetails.userLists.push({ userEmail: '', permissions: { createPipeline: false, executePipeline: false, deployModel: false, uploadDataset: false, view: true, workspaceAdmin: false } })
  }

  // Method to remove user details
  removeUserDetails(index) {
    this.model.projectDetails.userLists.splice(index, 1);
  }

  // Method to create project
  createProject() {
    const parent = this;
    console.log(JSON.stringify(parent.model.projectDetails))
    parent.model.isReadOnly = true;
    parent.myService.createProjectDetails(parent.model.projectDetails)
      .then(
        responseData => {
          parent.model.projectDetails = responseData;
          parent.model.projectId = responseData['id'];
          parent.model.buttonName = "Update"
          parent.toaster.success(107);
          parent.model.isReadOnly = true;
          parent.router.navigate(['/projects/']);
        }).catch(
          data => {
            parent.model.isReadOnly = false;
            if (data) {
              parent.toaster.failureWithMessage(parent.utilityService.getErrorMessage(data));
            } else {
              parent.toaster.failure(104);
            }
          });
  }

  // Method to check if the user is allowed to update the project
  isUpdateAllowed() {
    const parent = this;
    if(parent.model.isReadOnly == true)
      parent.model.isBtnDisabled = true;
    else{
      this.model.currentUserId = parent.storageService.getData().userId;
      parent.myService.getTenantDetail().then((values) => {
        if (values[0]) {
          const tenantResList = values[0]['userLists'].filter(user =>
            user.userEmail === this.model.currentUserId);
          if (tenantResList.length > 0) {
            parent.model.isBtnDisabled = !tenantResList[0]['permissions']['createProject'];
          }
          if (parent.model.projectId != undefined && parent.model.isBtnDisabled)
            parent.model.isBtnDisabled = !parent.utilityService.isPermissionAllowed('workspaceAdmin', parent.model.projectId)
          }
      }).catch(() => {
        parent.model.isBtnDisabled = true;
        if (parent.model.projectId != undefined){
          parent.model.isBtnDisabled = !parent.utilityService.isPermissionAllowed('workspaceAdmin', parent.model.projectId);
        }
      });
    } 
  }

  // Method to get project details by ID
  getProjectDetailsByID() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.myService.getProjectDetailsByID(parent.model.projectId).then((response: any[]) => {
        parent.model.projectDetails = JSON.parse(JSON.stringify(response));
        fulfilled(true);
      }).catch(() => {
        rejected()
      });
    });
  }

  // Method to handle project modification
  projectModification() {
    const parent = this;
    parent.model.projectId === undefined ? parent.createProject() : parent.updateProject();
  }

  // Method to validate email
  validateEmail(emailRef: NgModel) {
    if (emailRef.value) {
      emailRef.control.setErrors(null);
      if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(emailRef.value)) {
        emailRef.control.setErrors({ pattern: true });
      }
    }
    emailRef.control.setValue(emailRef.value.toLowerCase());
  }

  // Method to update project
  updateProject() {
    const parent = this;
    console.log(JSON.stringify(parent.model.projectDetails))
    parent.model.isReadOnly = true;
    parent.myService.updateProjectDetails(parent.model.projectDetails)
      .then(
        responseData => {
          parent.model.projectDetails = responseData;
          parent.toaster.success(108);
          parent.model.isReadOnly = true;
          parent.router.navigate(['/projects/']);
        }).catch(
          data => {
            parent.model.isReadOnly = false;
            if (data) {
              parent.toaster.failureWithMessage(parent.utilityService.getErrorMessage(data));
            } else {
              parent.toaster.failure(104);
            }
          });
  }

  // Method to open confirm dialog
  openConfirmDialog(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });
  }

  // method to listen the resize window event
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  // Method to resize component
  private resizeComponent() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    console.log(windowWidth)
    parent.model.height = windowHeight - parent.heightOffset;
    parent.model.width = windowWidth - parent.widthOffset;
    console.log(windowHeight);
    console.log(windowWidth);
  }
}



