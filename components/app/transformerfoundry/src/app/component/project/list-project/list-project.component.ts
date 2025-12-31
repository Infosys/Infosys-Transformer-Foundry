/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, HostListener, OnInit, Output } from '@angular/core';
import { ProjectData } from 'src/app/data/project-data';
import { ProjectServiceService } from 'src/app/services/project-service.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';
import { BaseComponent } from 'src/app/base.component';
import { SessionService } from 'src/app/services/session.service';
import { ConfigDataHelper } from 'src/app/utils/config-data-helper';
import { DataStorageService } from 'src/app/services/data-storage.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { UtilityService } from 'src/app/services/utility.service';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-list-project',
  templateUrl: './list-project.component.html',
  styleUrls: ['./list-project.component.scss']
})
export class ListProjectComponent extends BaseComponent implements OnInit {
  // close and confirm output events for dialog box
  @Output() close = new EventEmitter<string>();
  @Output() confirm = new EventEmitter<string>();

  // project list
  public projectList: ProjectData[];

  // constructor to inject services
  constructor(
    private myService: ProjectServiceService,
    private toaster: ToasterServiceService,
    public sessionService: SessionService,
    public configDataHelper: ConfigDataHelper,
    private storageService: DataStorageService,
    private modalService: NgbModal,
    private utilityService: UtilityService,
  ) {
    super(sessionService, configDataHelper);
  }

  // model for list project component
  private tenantPermission = {
    createProject: false,
    deleteProject: false
  }

  deleteId: string =''
  model: any = {
    pageDefault: 0,
    pageSize: 10,
    totalItems: 0,
    tenantID: '',
    isDataLoaded: false,
    currentPageData: [],
    tenantPermission: this.tenantPermission,
    currentUserId: '',
    height: 0,
    width: 0,
    message: 'No data found'
  };
  heightOffset = 290;
  widthOffset = 48;

  ngOnInit(): void {
    this.getProjectData();
    this.resizeComponent();
  }

  // page change event
  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }

  // get project data from service for a tenant and current user
  getProjectData() {
    const parent = this;
    parent.model.isDataLoaded = false;
    const promise1 = parent.myService.getTenantDetail();
    const promise2 = parent.myService.getProjectDataList();
    this.model.currentUserId = parent.storageService.getData().userId;
    Promise.all([promise1, promise2]).then((values) => {
      // Current Tenant Details
      if (values[0] && values[0]!== undefined) {
        const tenantResList = values[0]['userLists'].filter(user =>
          user.userEmail === this.model.currentUserId);
        if (tenantResList.length > 0) {
          parent.model.tenantPermission.createProject = tenantResList[0]['permissions']['createProject'];
          parent.model.tenantPermission.deleteProject = tenantResList[0]['permissions']['deleteProject'];
        }
        if(parent.model.currentUserId == values[0]['createdBy']){
          parent.model.tenantPermission.createProject = true;
          parent.model.tenantPermission.deleteProject = true;
        }
      }
    // Project List
    // if projectlist has a property "message", then assign model.message = projectlist.message
    // else assign model.message = "No data found"
      if (values[1] && values[1]!== undefined) {
        if (values[1].hasOwnProperty('message')) {
          parent.model.message = values[1]['message'];
          parent.projectList = [];
        } else {
          parent.projectList = values[1] as ProjectData[];
        }
      }
      
      parent.model.totalItems = parent.projectList.length;
      parent.getDataForCurrentPage();
      parent.model.isDataLoaded = true;
    }).catch(() => {
      parent.model.isDataLoaded = true;
    });

  }

  // check if create project is allowed
  isCreateAllowed() {
    return this.model.tenantPermission.createProject && this.getFeature(this.bmodel.FID.PROJECT_CREATE).isEnabled;
  }

  // check if delete project is allowed
  isUpdateAllowed(i) {
    const parent = this;
    if (parent.utilityService.isListHasValue(parent.projectList[i]['userLists'].filter(user => user.userEmail === this.model.currentUserId))) {
      const projectPermList = parent.projectList[i]['userLists'].filter(user => user.userEmail === this.model.currentUserId)
      var isAdmin = projectPermList[0]['permissions']['workspaceAdmin'];
    }
    return this.model.tenantPermission.createProject && this.getFeature(this.bmodel.FID.PROJECT_CREATE).isEnabled || isAdmin;
  }

  // check if delete project is allowed
  isDeleteAllowed(i) {
    const parent = this;
    return parent.model.tenantPermission.deleteProject && this.getFeature(this.bmodel.FID.PROJECT_DELETE).isEnabled;
  }

  // get data for current page
getDataForCurrentPage() {
  const parent = this;
  const startIndex = (parent.model.pageDefault) * parent.model.pageSize;
  console.log(startIndex)
  parent.model.currentPageData = parent.projectList.slice(
    startIndex, startIndex + parent.model.pageSize
  );
}

// delete project
deleteProject(projectId) {
  const parent = this;
  console.log(projectId);
  parent.myService.deleteProject(projectId).then((response: any) => {
    parent.toaster.success(109);
    parent.getProjectData();
  }).catch(
    data => {
      parent.model.isReadOnly = false;
      if (data) {
        parent.toaster.failureWithMessage(data["message"]);
      } else {
        parent.toaster.failure(104);
      }
    });
}

// window resize event
@HostListener('window:resize', ['$event'])
onResize(event) {
  this.resizeComponent();
}

// call open dialog box
open(content, isBtnDisabled, id) {
  const parent = this;
  parent.deleteId = id;
  parent.openConfirmDialog(content);
}

// open dialog box
  private openConfirmDialog(content) {
  const parent = this;
  parent.modalService
    .open(content,  {
      centered: true,
      windowClass: 'square-modal',
    })
}

  private resizeComponent() {
  const parent = this;
  const windowHeight = window.innerHeight;
  const windowWidth = window.innerWidth;
  parent.model.height = windowHeight - parent.heightOffset;
  parent.model.width = windowWidth - parent.widthOffset;
}
}
