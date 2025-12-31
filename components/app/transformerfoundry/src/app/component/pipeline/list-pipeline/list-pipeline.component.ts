/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, HostListener } from "@angular/core";
import { PipelineServiceService } from "../../../services/pipeline-service.service";
import { PipelineData } from "../../../data/pipeline-data";
import { ActivatedRoute } from "@angular/router";
import { BaseComponent } from "src/app/base.component";
import { SessionService } from "src/app/services/session.service";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { UtilityService } from "src/app/services/utility.service";
import { PageEvent } from "@angular/material/paginator";
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: "app-list-pipeline",
  templateUrl: "./list-pipeline.component.html",
  styleUrls: ["./list-pipeline.component.scss"],
})
export class ListPipelineComponent extends BaseComponent implements OnInit {
  public pipelineList: PipelineData[];

  // constructor
  constructor(
    private modalService: NgbModal,
    private myService: PipelineServiceService,
    private route:ActivatedRoute,
    public sessionService: SessionService,
    public configDataHelper: ConfigDataHelper,
    public utilityService: UtilityService) {
    super(sessionService, configDataHelper)
  }

  // model object to store UI data 
  model: any = {
    breadcrumbOne:'',
    isDataLoaded:false,
    projectId:'',
    pageDefault:0,
    pageSize:10,
    totalItems:0,
    height:0,
    width:0,
    // currentPageData:[],
    projectName:'',
    permissionStatus: false
    // currentPageData:[]
  };

  // height and width offset for resizing
  heightOffset = 291.5;
  widthOffset = 46;

  // onInit method
  ngOnInit(): void {
    const parent = this;
    // parent.model.projectId = parent.storageService.getData().projectId;
    parent.updateProjectId();
    parent.getPipelineListData(parent.model.projectId);
    parent.resizeComponent();
    parent.isCreatePipelineAllowed();
    parent.updateProjectName();
  }

  // method to update project id
  updateProjectId(){
    const parent=this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('projects');
    if (index!==-1 && index+1 < urlsegment.length) {
      parent.model.projectId= urlsegment[index+1];
    }
  }

  // method to get pipeline list data
  getPipelineListData(projectId:string) {
    const parent = this;
    parent.model.isDataLoaded=false;
    parent.myService.getPipelineListData(projectId).then((response: any) => {
      parent.pipelineList=response;
      parent.model.isDataLoaded=true;

      parent.model.totalItems = parent.pipelineList.length;
      parent.getDataForCurrentPage();

    })
      .catch((error:any)=>{
        console.error("Error",error);
        parent.model.isDataLoaded=true;
      });
  }

  // on page change event
  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    // parent.model.isDataLoaded = false;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }

  // method to get data for current page
  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault)*parent.model.pageSize;
    parent.model.currentPageData=parent.pipelineList.slice(
      startIndex,startIndex+parent.model.pageSize
    );
  }

  // method to check if create pipeline is allowed
  isCreatePipelineAllowed(){
    const parent = this;

    parent.utilityService.isPermissionAllowed('createPipeline', parent.model.projectId).then(
      (response: any) => {
        parent.model.permissionStatus = response;
      }
    ).catch((error: any) => {
      console.error("Error in fetching permission status", error);
      parent.model.permissionStatus = false;
    });
  }

  // event listener to resize window
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  // method to resize component
  private resizeComponent() {
    const parent =this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    parent.model.height=windowHeight-parent.heightOffset;
    parent.model.width=windowWidth-parent.widthOffset;
  }

  // method to update project name
  private updateProjectName(){
    const parent=this;
    this.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else{
        parent.model.projectName ='';
      }
    });
  }
}
