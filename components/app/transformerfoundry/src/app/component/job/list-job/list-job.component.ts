/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, OnInit } from "@angular/core";
import { ModelService } from 'src/app/services/models.service';
import { ActivatedRoute } from "@angular/router";
import { PageEvent } from "@angular/material/paginator";

@Component({
  selector: "app-list-job",
  templateUrl: "./list-job.component.html",
  styleUrls: ["./list-job.component.scss"],
})
export class ListJobComponent implements OnInit {
  // list of experiments
  public experimentList: any[];

  constructor(
    private myService: ModelService,
    private route:ActivatedRoute,
    ) {}

    // model objects of the component
  model: any = {
    isDataLoaded:false,
    pageDefault:0,
    pageSize:10,
    totalItems:0,
    currentPageData:[],
    height:0,
    width:0,
    projectName:'',
  };
 
  // height and width offset for the tabs in job fine tuning module
  heightOffset = 275;
  widthOffset = 33;

  // on init fill the tabs with values corresponding to the project id, pipeline id, experiment id.
  ngOnInit(): void {
    const parent = this;
    parent.updateProjectId();
    parent.getExperimentList(parent.model.projectId);
    parent.resizeComponent();
    parent.updateProjectName();
    
  }

  // get the project id from the url
  updateProjectId(){
    const parent=this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('projects');
    if (index!==-1 && index+1 < urlsegment.length) {
      parent.model.projectId= urlsegment[index+1];
    }
  }

  // get the experiment list for the project id
  getExperimentList(projectId:string) {
    const parent = this;
    parent.model.isDataLoaded = false;
    parent.myService.getExperimentList(projectId).then((response: any) => {
      parent.experimentList = response;
      console.log('list:',parent.experimentList);
      parent.model.isDataLoaded = true;

      parent.model.totalItems = parent.experimentList.length;
      parent.getDataForCurrentPage();
    })
    .catch(error => {
      console.log(error);
      parent.experimentList= [];
      parent.model.isDataLoaded = true;
    });
  }

  // on page change, get the data for the current page
  onPageChange(page: PageEvent) {
    console.log(page);
    const parent = this;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }
  
  // get the data for the current page
  getDataForCurrentPage(){
    const parent = this;
    const startIndex = (parent.model.pageDefault)*parent.model.pageSize;
    parent.model.currentPageData=parent.experimentList.slice(
      startIndex,startIndex+parent.model.pageSize
    );
  }

  // on window resize, resize the component
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.resizeComponent();
  }

  // resize the component
  private resizeComponent() {
    const parent =this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    parent.model.height=windowHeight-parent.heightOffset;
    parent.model.width=windowWidth-parent.widthOffset;
  }

  // update the project name
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
