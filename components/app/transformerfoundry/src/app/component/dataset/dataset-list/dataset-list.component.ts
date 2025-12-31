
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { Component, HostListener, OnInit,Input } from "@angular/core";
import { PageEvent } from "@angular/material/paginator";
import { data } from "jquery";
import { DatasetService } from "src/app/services/dataset.service";
import { MatTableDataSource } from '@angular/material/table';
import { Navigation, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Location } from "@angular/common";
import { ActivatedRoute,NavigationExtras } from '@angular/router';

import { da, de } from "date-fns/locale";
import { query } from "@angular/animations";

@Component({
  selector: "app-rag-dataset-list",
  templateUrl: "./dataset-list.component.html",
  styleUrls: ["./dataset-list.component.scss"],
})
export class DatasetListComponent implements OnInit {
  userId: string = 'default-user-id';
  projectId = "";
  rowData:any;
  isViewMode: boolean = false;
  currentPage: number = 0;
  // projectData: Dataset[] = []; // or Dataset if it is a single object
  data: any[] = [];
  // datasets: any[] = [];
  dataSource = new MatTableDataSource<any>();
  displayedColumns: string[] = ['name', 'version','description','createdOn','createdBy','isDeleted','updatedBy','modifiedOn','projectId','scope','userlist','size','task','modality','language','license','purpose','usecase','format','limitation','tags','dataStorage','id','status']; // Specify the fields you want to display
  loading: boolean = true;
    deleteId: string =''; // ID of the item to be deleted
   
  // @Input() data: {};
  @Input() dataSet: string;
  projectData: any;
  nameC: boolean;
  registerNumr: any;
  
  constructor(private datasetservice:DatasetService,private router: Router, private modalService: NgbModal,private location:Location,  private route: ActivatedRoute) {}
  recreatedatasets(): void {
    this.router.navigate(['recreate']);
  }



  model = {
    projectName: "",
    datasetList: [],
    isDataLoaded: false,
    projectId: "",
    pageDefault: 0,
    pageSize: 10,
    totalItems: 0,
    height: 0,
    width: 0,
   
    currentPageData: [],
   
  };

  // height and width offset for resizing
  heightOffset = 291.5;
  widthOffset = 46;

  ngOnInit(): void {
    this.resizeComponent();
    this.updateProjectId();
    this.updateProjectName();
    this.loadData();
    if(this.projectId){
    this.datasetservice.getData(this.projectId).subscribe((response: any) => {
      // this.projectData = response;
      // console.log('ifprojectData:', this.projectData);
      console.log('API Response:', response); // Check response structure
      // console.log('dat')
      this.model.datasetList = response.data.datasets;
      this.model.totalItems = this.model.datasetList.length;
      console.log('totalitems:', this.model.totalItems);
      // this.getDataForCurrentPage();
      this.loadData();
      console.log('modeldatasetlist:', response.data?.datasets); // Inspect datasets
      console.log('getDatasets:', response.data?.datasets); // Inspect datasets
      // console.log('itemm',item.id)
      if(response &&response.data && Array.isArray(response.data.datasets)){
        console.log('afterifdatasets:', response.data.datasets);
      this.data = response.data.datasets.map(item => ({
      //  model.datasetList = response.data.datasets;
        // parent.model.totalItems = parent.pipelineList.length;
      id: item.id,
      name: item.dataset['name'], // Adjust according to your data structure
    
       description: item.dataset['description'],
       version: item.dataset['version'],
       createdOn: item['createdOn'],
        createdBy: item['createdBy'],
        isDeleted: item['isDeleted'],
        updatedBy: item['updatedBy'],
        modifiedOn: item['modifiedOn'],
        projectId: item['projectId'],
        scope: item.dataset['scope'],
        userlist: item.dataset['userlist'],
        size: item.dataset['size'],
        task: item.dataset['task'],
        modality: item.dataset['modality'],
        language: item.dataset['language'],
        tags: item.dataset['tags'],
        license: item.dataset['license'],
        purpose: item.dataset['purpose'],
        usecase: item.dataset['usecase'],
        format: item.dataset['format'],
        limitation: item.dataset['limitation'],
        dataStorage: item.dataset['dataStorage'],
        status: item['status'],


        // return item;
      } ));
      // console.log('item:', item),
      this.dataSource.data = this.data; // If using MatTableDataSource
    console.log('MappedData:', this.data);}
      else {
        console.error('Unexpected response structure:', response);
        this.data = [];
        
      }
      this.loading = false;
    });



      error=> {
        console.error('Error:', error);
        this.data = [];
        this.loading = false;
      }
    // );//previous get data
  }else{
    console.error("Project ID not found in the URL.");
    this.loading = false;
  }
 
    
  }

  loadData(): void {
    this.datasetservice.getData(this.projectId).subscribe((response: any) => {
      console.log('API Response:', response); // Check response structure
      this.model.datasetList = response.data.datasets;
      console.log('modeldatasetlist:', this.model.datasetList); // Check response structure
      this.model.totalItems = this.model.datasetList.length;
      console.log('totalitems:', this.model.totalItems);
      this.getDataForCurrentPage();
    });
  }

  // on page change event
  onPageChange(page: PageEvent) {
    this.currentPage = page.pageIndex;
    this.getDataForCurrentPage();
  }
  
// method for refreshing page
refreshPage(){
  window.location.reload();
}

 
  getDataForCurrentPage() {
    const startIndex = this.currentPage  * this.model.pageSize;
    const endIndex = startIndex + this.model.pageSize;
    this.data = this.model.datasetList.slice(startIndex, endIndex);
    console.log('currentpagedata:', this.data);
  }


 
  onRowClick(rowData: string) {
    console.log('Row data id:', rowData);
    this.router.navigate(['/datasets/view/',rowData], {state:{data:rowData}});
     
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
  updateProjectId(){
    const parent=this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('projects');
    if (index!==-1 && index+1 < urlsegment.length) {
      this.projectId= urlsegment[index+1] || '';
    }
    else {
      console.error("Project ID not found in the U.");
    }
    
  }

 
// console.log("datasetId",datasetId);

deleteDataset(datasetId: string, userId: string) {

  console.log('Dataset ID to delete:', datasetId);
  console.log('User ID:', userId);
 
  this.datasetservice.deleteDataset(datasetId, userId).subscribe(
    response => {
     
      this.refreshPage();
      console.log('Dataset deleted successfully', response);
    },
    error => {
      console.error('Error deleting dataset', error);
    }
  );
}

// method to open services data when we click name
nameRow(rowData: any) {
  console.log('Row data:', rowData);
  
}

logItemId(item: any): void {
  console.log('Item ID:', item.name);
}


navigateToUpdateDetails(modelId: string) {
  const queryParams:NavigationExtras = {queryParams:{pn: this.model.projectName}};
  this.router.navigate(['/projects', this.projectId, 'datasets', 'update', modelId],queryParams);
}
navigateToViewDetails(modelId: string) {
  const queryParams:NavigationExtras = {queryParams:{pn: this.model.projectName}};
  this.router.navigate(['/projects', this.projectId, 'datasets', 'view', modelId],queryParams);
}
  //  function to update the project name
   private updateProjectName() {
    const parent = this;
    parent.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else {
        parent.model.projectName = '';
      }
    });
  }

}
