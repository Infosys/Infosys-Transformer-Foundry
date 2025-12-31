/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import {
  Component,
  OnInit,
  HostListener,
  Output,
  EventEmitter,
} from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { BaseComponent } from "src/app/base.component";
import { PayloadData } from "src/app/data/payload-data";
import { PipelineDetailsData } from "src/app/data/pipeline-details-data";
import { PipelineServiceService } from "src/app/services/pipeline-service.service";
import { SessionService } from "src/app/services/session.service";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { UtilityService } from "src/app/services/utility.service";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { PageEvent } from "@angular/material/paginator";
import { tr } from "date-fns/locale";


export interface TemplateItem {
  name: string;
  version: string;
  description: string;
  type: string;
  createdOn: string; // or Date if you're using date objects
}
@Component({
  selector: "app-import-pipeline",
  templateUrl: "./import-pipeline.component.html",
  styleUrls: ["./import-pipeline.component.scss"],
})
export class ImportPipelineComponent extends BaseComponent implements OnInit {
  constructor(
    private pipelineService: PipelineServiceService,
    private route: ActivatedRoute,
    public sessionService: SessionService,
    public configDataHelper: ConfigDataHelper,
    public utilityService: UtilityService,
    private toaster: ToasterServiceService,
    private router: Router
  ) {
    super(sessionService, configDataHelper);
  }
  // event emitters for close and save
  @Output() close = new EventEmitter<string>();
  // @Output() onActionCompleted: EventEmitter<any> = new EventEmitter();

  // height and width offset for resizing
  heightOffset = 270;
  widthOffset = 20;

  pipelineList: any = [];
  activeItem: any = null;
  panelOpenState: boolean = false;
  originalData: TemplateItem[] = []; // Populate this with your initial data
  filteredData: TemplateItem[] = [];
  searchText: string = "";

  inputTemplatePayload: PayloadData;
  inputTemplateDetails: PipelineDetailsData;

  model: any = {
    templateList: [],
    templateTypeList: [],
    breadcrumbOne: "",
    isDataLoaded: false,
    projectId: "",
    pageDefault: 0,
    pageSize: 10,
    totalItems: 0,
    height: 0,
    width: 0,
    projectName: "",
    permissionStatus: false,
    pipelineData: {},
    nodePayload: {},
    confidentialData: {},
  };
  currentPageData: TemplateItem[] = [];

  ngOnInit(): void {
    // this.model.templateList = dummytemplateList;
    // this.model.templateList = pipelines;

    const promise1 = this.pipelineService.getGlobalTemplates();

    promise1
      .then((response: any) => {
        this.originalData = response["pipelines"];
        this.filteredData = this.originalData;
        this.model.isDataLoaded = true;
        this.model.totalItems = this.filteredData.length;
        this.getDataForCurrentPage();
      })
      .catch(() => {
        this.model.isDataLoaded = true;
      });

 

    // this.model.isDataLoaded = true;
    console.log(this.model.templateTypeList, this.originalData);
    this.updateProjectName();
    this.resizeComponent();
    this.updateProjectId();
  }

  filterData() {
    if (!this.searchText) {
      this.filteredData = this.originalData;
      console.log("No search text", this.filteredData);
    } else {
      // this.filteredData = this.originalData.filter((item) => {
      //   console.log("Item", item);
      //   return Object.values(item).some((val) =>
      //     val.toString().toLowerCase().includes(this.searchText.toLowerCase())
      //   );
      // });
      // console.log("Search text", this.searchText, this.filteredData);
      this.filteredData = this.originalData.filter(record => {
          return Object.values(record).some(val => {
            if (typeof val === 'object') {
              return Object.values(val).some(subVal => subVal.toString().toLowerCase().includes(this.searchText.toLowerCase()));
            } else {
              return val.toString().toLowerCase().includes(this.searchText.toLowerCase());
            }
          });
        });
    }
  }

  // groupTemplates() {
  //   const templateMap = new Map();
  //   for (const template of dummytemplateList) {
  //     if (!templateMap.has(template.type)) {
  //       templateMap.set(template.type, {
  //         type: template.type,
  //         pipelines: [],
  //       });
  //     }
  //     templateMap.get(template.type).pipelines.push(template);
  //   }
  //   this.groupedTemplates = Array.from(templateMap.values());

  //   console.log(this.groupedTemplates);
  // }

  setActiveItem(item: any) {
    this.activeItem = item;
    console.log(item);
  }

  isItemActive(item: any): boolean {
    return this.activeItem && this.activeItem.metadata.id === item.metadata.id;
  }
  // on page change, get the data for the current page
  onPageChange(page: PageEvent) {
    console.log("Balloon", page);
    const parent = this;
    parent.model.pageDefault = page.pageIndex;
    parent.getDataForCurrentPage();
  }

  // get the data for the current page
  getDataForCurrentPage() {
    const parent = this;
    const startIndex = parent.model.pageDefault * parent.model.pageSize;
    parent.currentPageData = parent.filteredData.slice(
      startIndex,
      startIndex + parent.model.pageSize
    );
    console.log("Current Page Data", parent.currentPageData);
  }

  // Method to import a pipeline (create new in same project workspace)
  importPipeline(templateID: any) {
    const parent = this;
    console.log("importing pipeline", templateID);
    // const promise1 = parent.getPipelineDefinition(templateID);
    // const promise2 = parent.getPayloadData(templateID);
    parent.router.navigate(['/projects/', parent.model.projectId, 'pipelines' , 'view', templateID], { queryParams: { gt: true, pn: this.model.projectName } });

    // Promise.all([promise1, promise2])
    //   .then((values) => {
    //     console.log("Promise.all", values);
    //     // process the pipeline data and node payload
    //     parent.managePipelineData();
    //     console.log(
    //       "Pipeline Data",
    //       parent.model.pipelineData,
    //       parent.model.nodePayload
    //     );
    //     // Route to [routerLink]="['view', item.id]" [queryParams]="{ rc: true , pn: model.projectName }"
    //     parent.router.navigate(['/projects/', parent.model.projectId, 'pipelines' , 'view', templateID], { queryParams: { gt: true, pn: this.model.projectName } });
    //     // this.router.navigate(['/view', templateID], { queryParams: { rc: true, pn: this.model.projectName } });
    //     // parent.createPipelineFromTemplate();
    //     // parent.pipelineService.postGlobalTemplatesHistory(
    //     //   parent.model.projectId,
    //     //   templateID
    //     // );
    //   })
    //   .catch((error) => {
    //     console.error("Error in importing pipeline", error);
    //   });
    parent.closeWindow();
  }

  // method to get the pipeline definition of the id from the api
  getPipelineDefinition(pipelineId) {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.pipelineService
        .getPipelineDefinition(pipelineId, true)
        .then((response: any[]) => {
          parent.model.pipelineData = response;
          console.log("Imported this pipeline");
          fulfilled(true);
        })
        .catch(() => {
          rejected();
        });
    });
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

  // remove fields from the pipeline data
  managePipelineData() {
    const parent = this;
    delete parent.model.pipelineData?.status;
    delete parent.model.pipelineData?.createdBy;
    delete parent.model.pipelineData?.createdOn;
    delete parent.model.pipelineData?.isDeleted;
    delete parent.model.pipelineData?.updatedBy;
    delete parent.model.pipelineData?.modifiedOn;
    delete parent.model.pipelineData?.tenantName;
    delete parent.model.pipelineData?.projectId;
    delete parent.model.pipelineData?.id;

    if (parent.model.pipelineData.pipeline.volume === null) {
      delete parent.model.pipelineData.pipeline.volume;
    }

    for (let key in parent.model.pipelineData.pipeline.flow) {
      delete parent.model.pipelineData.pipeline.flow[key].inputArtifacts;
    }

    delete parent.model.nodePayload.pipelineId;
    delete parent.model.nodePayload.projectId;

    // add new project id
    parent.model.pipelineData.projectId = parent.model.projectId;
    parent.model.nodePayload.projectId = parent.model.projectId;
  }

  // create pipeline from the template
  createPipelineFromTemplate() {
    const parent = this;
    try {
      parent.pipelineService
        .createPipelineDetails(parent.model.pipelineData)
        .then((responseData: any) => {
          parent.model.isReadOnly = true;
          // parent.isCreatePipelineAllowed();
          parent.model.isDataLoaded = true;
          // console.log("ResponseData:", responseData);

          parent.sendPayloadData(responseData?.id);
          // navigate to list pipeline
          parent.router.navigate(
            ["/projects/", parent.model.projectId, "pipelines"],
            { queryParams: { pn: this.model.projectName } }
          );
        })

        .catch((data) => {
          parent.model.isReadOnly = false;
          parent.model.isDataLoaded = true;
          if (data) {
            parent.toaster.failureWithMessage(
              data?.["details"]?.[0]?.message ||
                data?.["detail"]?.message ||
                data?.Error
            ); //backendFix
          } else {
            parent.toaster.failure(104);
          }
        });
    } catch {
      parent.toaster.failure(104);
    }
  }

  // send payload data of the pipeline id
  sendPayloadData(pipelineId) {
    const parent = this;
    parent.model.nodePayload.pipelineId = pipelineId;
    parent.model.nodePayload.projectId = this.model.projectId;
    // parent.model.nodePayload.pipelineData = parent.inputConfidentialData;
    parent.pipelineService
      .postNodeFormData(parent.model.nodePayload)
      .then((response: any) => {
        console.log("CreatePipelineSummary:", response);
        parent.toaster.success(102);
        // this.model.summaryData.id = pipelineId;
        parent.model.pipelineId = pipelineId;
        // parent.model.pipelineId.emit(pipelineId);
      });
  }

  printx() {
    console.log("printx");
  }
  // close the modal window
  closeWindow() {
    const parent = this;
    parent.close.emit("window closed");
  }

  // update project id from url
  updateProjectId() {
    const parent = this;
    let urlsegment = window.location.href.split("/");
    let index = urlsegment.indexOf("projects");
    if (index !== -1 && index + 1 < urlsegment.length) {
      parent.model.projectId = urlsegment[index + 1];
    }
  }

  // method to check if create pipeline is allowed
  isCreatePipelineAllowed() {
    const parent = this;

    parent.utilityService
      .isPermissionAllowed("createPipeline", parent.model.projectId)
      .then((response: any) => {
        parent.model.permissionStatus = response;
      })
      .catch((error: any) => {
        console.error("Error in fetching permission status", error);
        parent.model.permissionStatus = false;
      });
  }

  // event listener to resize window
  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.resizeComponent();
  }

  // method to resize component
  private resizeComponent() {
    const parent = this;
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    parent.model.height = windowHeight - parent.heightOffset;
    parent.model.width = windowWidth - parent.widthOffset;
  }

  // method to update project name
  private updateProjectName() {
    const parent = this;
    this.route.queryParamMap.subscribe((queryParams) => {
      if (queryParams.has("pn")) {
        parent.model.projectName = queryParams.get("pn");
      } else {
        parent.model.projectName = "";
      }
    });
  }
}
