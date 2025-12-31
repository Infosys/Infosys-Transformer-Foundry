/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { EndpointData } from 'src/app/data/endpoint-data';
import { ModelService } from 'src/app/services/models.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';

@Component({
  selector: 'app-model-endpoint-details',
  templateUrl: './model-endpoint-details.component.html',
  styleUrls: ['./model-endpoint-details.component.scss']
})
export class ModelEndpointDetailsComponent implements OnInit {
  // event emitters
  @Output() nextTab = new EventEmitter<number>();
  @Output() endpointDt = new EventEmitter<{}>();
  @Output() endpointId = new EventEmitter<{}>();

  // input variables for the height and width of the tab
  @Input() height: number;
  @Input() width: number;

  // input variables for the endpoint data, endpoint id, model id, model version and project id
  @Input()
  set inputEndpointData(inputEndpointData: EndpointData) {
    this.model.endpointData = inputEndpointData;
  }
  @Input() 
  set inputModelId(inputModelId: string) {
    this.model.modelId = inputModelId;
  }
  @Input() 
  set inputModelVersion(inputModelVersion: string) {
    this.model.modelVersion = inputModelVersion;
  }
  @Input() 
  set inputProjectId(inputProjectId: string) {
    this.model.endpointData.projectId = inputProjectId;
  }
  @Input()
  set inputEndpointId(inputEndpointId: any) {
    this.model.endpointId = inputEndpointId;
    console.log("Receiving endpoint id in enpoint details", inputEndpointId, this.model.endpointId)
  }

  // model object to store the UI values
  model: any = {
    endpointData: new EndpointData(),
    endpointList: [],
    message: 'No Data Found.',
    isDataLoaded: true,
    isReadOnly: false,
    isBtnDisabled: false,
    modelId: '',
    modelVersion: '',
    endpointId: '',
    disableContextUri: false
  }

  // show section object to show the section in the UI
  showSection = {
    endpointDetails: true
  }

  // constructor to inject the services
  constructor(
    private modelService: ModelService, 
    private toaster: ToasterServiceService, 
    private modalService: NgbModal
  ) { }

  // on init function to get the endpoint list
  ngOnInit(): void {
    const parent = this;
    parent.modelService.getEndPointList(parent.model.endpointData.projectId).then((response: any) => {
      this.model.endpointList = response;
      console.log("ngOninit", this.model.endpointList, this.model.endpointData);
    }).catch(error => {
      this.model.endpointList = [];
    });

  }

  // function to check the changes in the input variables
  ngOnChanges(changes: SimpleChanges) {
    console.log("checking changes in update details", this.model.endpointData);
    if (changes.inputEndpointData && !changes.inputEndpointData.firstChange) {
      console.log("calling to emit update details", this.model.endpointData);
      this.handleDetailChanges();
    }
  }

  // function to get the endpoint details if the endpoint is selected from the dropdown or entered manually
  getEndpoint(event: any) {
    const parent = this;
    console.log(event);
    if (event?.id !== undefined){
      parent.model.endpointData.name = event.id.name;
      parent.model.endpointData.contextUri = event.id.contextUri;
      parent.model.endpointId = event.id.id;
      parent.model.disableContextUri = true;
      parent.emitEndpointId()
      console.log("Existing endpoint chosen", parent.model.endpointData, "from the list:", parent.model.endpointList);
    }
    else{
      parent.model.endpointData.name = event;
      parent.model.endpointId = '';
      parent.model.disableContextUri = false;
      parent.emitEndpointId()
      console.log("New endpoint entered is:", event, "The endpoint Object is:", parent.model.endpointData);
    }
  }

  // function to create the endpoint
  createEndpoint() {
    const parent = this;
    parent.model.isReadOnly = true;
    parent.model.isBtnDisabled = true;
    parent.model.isDataLoaded = false;
    console.log(parent.model.endpointData)
    try {
      parent.modelService.createEndpoint(parent.model.endpointData)
        .then(
          (responseData: any) => {
            parent.model.isReadOnly = true;
            parent.model.isBtnDisabled = false;
            parent.model.isDataLoaded = true;
            var value = {'id': responseData.id, 'name': responseData.name}
            parent.model.endpointId = responseData.id;
            parent.endpointId.emit(value);
            parent.toaster.success(113);
            console.log("ResponseData:", responseData);
          }).catch(
            data => {
              parent.model.isReadOnly = false;
              parent.model.isBtnDisabled = false;
              parent.model.isDataLoaded = true;
              if (data) {
                parent.toaster.failureWithMessage(data?.["details"]?.[0]?.message || data?.["detail"]?.message || data?.Error || data?.["error"]?.["details"]?.[0]?.message );
              } else {
                parent.toaster.failure(104);
              }
              parent.model.endpointId = '';
            });
    } catch {
      parent.toaster.failure(104);
      parent.model.endpointId = '';
      parent.model.isReadOnly = false;
      parent.model.isBtnDisabled = false;
    }

  }

  // function to emit the endpoint id
  emitEndpointId(){
    const parent = this;
    var value = {'id': parent.model.endpointId, 'name': parent.model.endpointData.name}
    parent.endpointId.emit(value);
  }

  // function to disable the context uri field if the endpoint is selected from the dropdown
  disableContextUri(){
    const parent = this;
    // console.log(parent.model.endpointId !== '', parent.model.endpointId !== '' || parent.model.endpointId !== undefined);
    return parent.model.endpointId !== '';
  }

  // function to call the confirm dialog
  open(confirmAction){
    const parent = this;
    console.log(parent.model.endpointData)
    if (parent.model.endpointId == undefined || parent.model.endpointId == '')
      parent.openConfirmDialog(confirmAction);
  }

  // function to open the confirm dialog
  private openConfirmDialog(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });
  }

  // function to handle the changes in the endpoint details
  private handleDetailChanges() {
    const parent = this;
    parent.endpointDt.emit(parent.model.endpointData);
    console.log("emiting values", parent.model.endpointData);
  }
}
