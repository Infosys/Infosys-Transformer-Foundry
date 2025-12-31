
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { Component, OnInit, Input ,HostListener, EventEmitter,Output,ElementRef, Renderer2 } from "@angular/core";
import { COMMA, ENTER } from "@angular/cdk/keycodes";
import { MatChipInputEvent } from "@angular/material/chips";
import { Limitation } from "src/app/data/update-model-data";
import { Dataset } from "src/app/data/rag-eval-data";
import { DatasetService } from "src/app/services/dataset.service";
import { DataStorageService } from 'src/app/services/data-storage.service';
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { MatDialog,MAT_DIALOG_DATA,MatDialogRef } from '@angular/material/dialog';
// import { DialogConfirmComponent } from "../../dialog-confirm/dialog-confirm.component";

import { ModelService } from "src/app/services/models.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { FormBuilder, FormGroup, NgModel, Validators } from '@angular/forms';
import { ToasterServiceService } from "src/app/services/toaster-service";
import { ActivatedRoute } from '@angular/router';
import { id, th } from "date-fns/locale";


 @Component({
  selector: "app-rag-data-register",
  templateUrl: "./rag-data-register.component.html",
  styleUrls: ["./rag-data-register.component.scss"],
})



export class RagDataRegisterComponent implements OnInit {
 

  data: any;
  @Input() height: number;
  @Input() width: number; 
  @Input() dataStorage: {};
  
  userId: string = 'default-user-id';
  dataSet: any;
  opendialog: boolean;
  widthOffset = 32;
  heightOffset = 270.5;
rowData:any;
  nameC: boolean;
  item:any;

  newModel:any={
    isDataLoaded: false,
    projectId: "",
    dataset: {
      name: "",
      version: 0,
      description: "",
      // enum public or restricted
      scope:"",
      size: 0,
      task: "",
      modality: "",
      language: "",
      tags: [],
      userlist:[],
      license: "",
      purpose: "",
      usecase: "",
      format: "",
      limitation: "",
   
    
  
    dataStorage : { storageType: "", uri: "" }
    }
    
  };
   isViewMode: boolean=false;
   isUpdateMode: boolean=false;
   isCreateMode: boolean=false;
   errorMessage: string;
  

// registrationForm: FormGroup;
 
  constructor(private datasetservice:DatasetService,
     private storageService: DataStorageService,
     private modalService: NgbModal,
    private myService: ModelService,
     public dialog: MatDialog,
     private snackBar: MatSnackBar,
     private elRef: ElementRef, private renderer: Renderer2,
     private fb: FormBuilder,
     private toaster: ToasterServiceService,
     private route: ActivatedRoute,
  
  ) {}
  isAlphanumeric(input: string): boolean {
    const alphanumericPattern = /^[a-zA-Z0-9]*$/;
    return alphanumericPattern.test(input);
  }
  
  isReadOnly = false;
  visible = true;
  selectable = true;
  removable = true;
  addOnBlur = true;
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];
  loading: boolean = true;
 
  isDataLoaded: boolean = true;
 
model={
  mode: '',
  isDataLoaded: false,
  projectId: "",
  id:'',
  dataset: {
    name: "",
    version: 0,
    description: "",
    // enum public or restricted
    scope:"",
    size: 0,
    task: "",
    modality: "",
    language: "",
    tags: [],
    userlist:[],
    license: "",
    purpose: "",
    usecase: "",
    format: "",
    limitation: "",
    
 
  

  dataStorage : { storageType: "", uri: "" },
 
  },
 
  
};

  

  ngOnInit(): void {
    this.updateProjectId();
    this.updateDatasetId();
    this.updateMode();
 
    // this.updateDatasetService();
      if(this.model.mode==='view'){
      
        this.isViewMode=true;
        console.log('isViewMode',this.isViewMode);
       
        console.log('beforemodel:',this.model.id);
        this.getDatasetDetails(this.model.id);
        console.log('model:',this.model.id);
      }else if( this.model.mode==='update'){
        
        this.isUpdateMode=true;
        
        this.getDatasetDetails(this.model.id);
      }else{
        this.isCreateMode=true;
      }

    

     

  }
  
  


 


  storage: Storage[] = [
    { value: "INFY_AICLD_MINIO", viewValue: "INFY_AICLD_MINIO" },
    { value: "INFY_AICLD_NUTANIX", viewValue: "INFY_AICLD_NUTANIX" },
  ];

  // Mat chip functions
  add(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    
     if ((value || "").trim()) {
      this.model.dataset.tags.push(value.trim());//directly push to tags array
    }

    if (input) {
      input.value = "";
    }
  }

  remove(value:string): void {
    const index = this.model.dataset.tags.indexOf(value);

    if (index >= 0) {
      this.model.dataset.tags.splice(index, 1);//directly splice from tags array
    }
  }
 

  addNewStorage() {
    this.model.dataset["storage"].push({
      storageType: "",
      uri: "",
    });
  }

  removeStorage(index: number) {
    this.model.dataset["storage"].splice(index, 1);
    console.log("Project ID before request:", this.model.projectId);
  }

    // update the project id
    
    updateProjectId(){
      const parent=this;
      let urlsegment = (window.location.href).split('/')
      let index = urlsegment.indexOf('projects');
      if (index!==-1 && index+1 < urlsegment.length) {
        parent.model.projectId= urlsegment[index+1] || '';
      }
      else {
        console.error("Project ID not found in the URL.");
      }
      
    }

    //Update DatsetId
    // updateDatasetId(){
    //   const parent=this;
    //   let urlsegment = (window.location.href).split('/')
    //   let index = urlsegment.indexOf('datasets');
    //   if (index!==-1 && index+1 < urlsegment.length) {
    //     parent.model.id= urlsegment[index+2] || '';
    //     console.log('updatedatasetId:',parent.model.id);
    //   }
    //   else {
    //     console.error("Dataset ID not found in the URL.");
    //   }
      
    // }
    updateDatasetId() {
      const parent = this;
      let urlsegment = (window.location.href).split('/');
      let index = urlsegment.indexOf('datasets');
      if (index !== -1 && index + 2 < urlsegment.length) {
        // Split the segment by '?' to remove query parameters
        let datasetIdSegment = urlsegment[index + 2].split('?')[0];
        parent.model.id = datasetIdSegment || '';
        console.log('updatedatasetId:', parent.model.id);
      } else {
        console.error("Dataset ID not found in the URL.");
      }
    }

    // adding valiation for the form
    validateModel(): boolean {
      const errors: string[] = [];
      
      // Validate projectId
      if (!this.model.projectId) {
        errors.push("Project ID is required.");
      }
  
      // Validate dataset fields
      const dataset = this.model.dataset;
      if (!dataset.name || dataset.name.trim().length === 0) {
        errors.push("Dataset name is required.");
      }
      
      if (dataset.version === undefined || dataset.version <= 0) {
        errors.push("Dataset version must be a positive number.");
      }
  
      // Validate description if provided
      if (dataset.description && dataset.description.trim().length === 0) {
        errors.push("If provided, dataset description must be non-empty.");
      }
  
      // Validate tags (if necessary, ensure it's an array of strings)
      if (dataset.tags && !dataset.tags.every(tag => typeof tag === 'string')) {
        errors.push("Tags should be an array of strings.");
      }
  
      // Validate dataStorage
      if (dataset.dataStorage) {
        if (!dataset.dataStorage.storageType.trim()) {
          errors.push("Storage type is required.");
        }
        if (!dataset.dataStorage.uri.trim()) {
          errors.push("URI is required.");
        }
      }
  
      if (errors.length > 0) {
        console.error("Validation errors:", errors.join(" "));
        return false;
      }
  
      return true;
    }

  saveDataset() {

     // Debugging log

  console.log("Dataset before request:", this.model);
  if (this.validateModel()) {
    console.log("Dataset validation request:", this.model);
    
  } else {
    console.error("Model validation failed. Check required fields.");
  }
    // console.log("dataset", this.model);
    this.updateProjectId();
   
    this.datasetservice.register(this.model).subscribe(
      (response) => {
     
        this.toaster.success(115);
       
        
        console.log('registration succesfull',response);
      },
      (error) => {
        this.toaster.failure(106);
       

        console.log('registration failed ',error);
      }
    );


   
  }




childdata(data){
  console.log('data:',data);

}
@HostListener('window:resize', ['$event'])
  onResize(event: Event) {
    this.adjustLayout();
  }

  adjustLayout() {
    // Example of dynamic adjustment, you can set or adjust styles or sizes here
    const container = this.elRef.nativeElement.querySelector('.scrollable-container');
    if (container) {
      // Example: setting container height dynamically based on window height
      this.renderer.setStyle(container, 'height', `${window.innerHeight - 100}px`);
    }


  }
  getDatasetDetails(id:string) {
    this.datasetservice.getDatasetById(this.model.id).subscribe((res)=>{
      this.model.dataset=res.data.dataset.dataset
      this.model.isDataLoaded=true;
      console.log('geydatadataset:',this.model);
    });
  }

  updateMode(){
    const parent=this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('datasets');
    if (index!==-1 && index+1 < urlsegment.length) {
      parent.model.mode= urlsegment[index+1] || '';
      console.log('mode:',parent.model.mode);
    }
    else {
      console.error("Dataset ID not found in the URL.");
    }
    
  }

  updateDatasetService(): void {
    if (this.model.id) {
      this.datasetservice.updateDataset(this.model.id,this.model).subscribe(
        res => {
          this.toaster.success(112);
          console.log('Dataset updated successfully', res);
          // Handle success (e.g., show a success message, navigate to another page, etc.)
        },
        error => {
          console.error('Error updating dataset', error);
          this.toaster.failure(106);
          // Handle error (e.g., show an error message)
        }
      );
    }
  }
  open(content) {
    const parent = this;
    parent.openConfirmDialog(content);
}

// open modal window
private openConfirmDialog(content) {
    const parent = this;
    parent.modalService
    .open(content, {
      centered: true,
      windowClass: 'square-modal',
    });  }

  
 
  
  

}

export interface Storage {
  value: string;
  viewValue: string;
}

