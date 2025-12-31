/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import { Arg, BenchmarkData, Data, Model } from '../../../data/benchmark-data';
import { NgbModal } from "@ng-bootstrap/ng-bootstrap";
import { BenchmarkServiceService } from '../../../service/benchmark-service.service';
import { ToasterServiceService } from '../../../service/toaster-service.service';
import { NgModel } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { CONSTANTS } from '../../../common/constants';

@Component({
  selector: 'app-job-submit',
  templateUrl: './job-submit.component.html',
  styleUrls: ['./job-submit.component.scss'],
})
export class JobSubmitComponent implements OnInit {
  @Input()
  set jobHeight(jobHeight: number) {
    this.model.jobHeight = jobHeight;
  }
  @Input() submitWidth: number = 0;
  @Input()
  set modelListData(modelListData: []){
    this.model.modelListData = modelListData;
    console.log('receiving modelListData', this.model.modelListData);
  }
  @Input()
  set projectId(projectId: any){
    this.model.projectId = projectId;
    console.log("receiving projectId",this.model.projectId);
  }
  @Output() showPopup = new EventEmitter<boolean>();
  @Input() submitBenchmark: boolean = false;
  @Input() 
  set userId(userId: any){
    this.model.userId = userId;
    console.log("receiving userId",this.model.userId);
  }

  modality = ['code', 'text', 'embedding'];
  dataType = ['fp16', 'fp32', 'int4', 'int8'];
  scope = ['public', 'infosys'];
  taskList: any = [];
  datasets: any = [];
  modelGenArgs: any = [];
  quantizeMethod = ['static', 'dynamic'];
  quantizeNA = ['NA'];
  gpuMemory = ['20GB', '40GB', '80GB'];

  showSection: any = {
    models: true,
    modelConfig: true,
    modelArguments: true,
    data: true,
    storage: true,
    resourceConfig: true,
    isBtnDisabled: false,
    modelBtnDisable: false,
  };

  model: any = {
    jobHeight: 0,
    benchmarkData: new BenchmarkData(),
    aiClouds3: "s3://",
    disableQuantize: [true],
    modelListData: [],
    projectId: '',
    urlCheck: false,
    userId: '',
    modelName: '',
    infyDatasets: [],
    publicDatasets: []
  };

  storage: Storage[] = [
    { value: 'INFY_AICLD_MINIO', viewValue: 'INFY_AICLD_MINIO' },
    { value: 'INFY_AICLD_NUTANIX', viewValue: 'INFY_AICLD_NUTANIX' },
  ];
  selectedStorage: string = this.storage[0].value;

  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
  }

  constructor(
    private modalService: NgbModal,
    private benchmarkService: BenchmarkServiceService,
    private toaster: ToasterServiceService,
  ) { }

  ngOnInit(): void {
    const parent = this;
    parent.model.urlCheck = window.location.hash;
    parent.model.benchmarkData.configuration.data[0].scope = 'public';
    const promiseTaskList = parent.benchmarkService.getBenchmarkMetaDataList(
      parent.model.benchmarkData.type,
      'task'
    );
    const promiseModelGenArgs = parent.benchmarkService.getBenchmarkMetaDataList(
      parent.model.benchmarkData.type,
      'modelGenArgs'
    );
    Promise.all([promiseTaskList, promiseModelGenArgs])
      .then((values: any) => {
        console.log('Promises', values);
        parent.taskList = values[0]['tasks'];
        parent.modelGenArgs = values[1]['modelGenArgs'];
        console.log(parent.taskList, this.datasets, this.modelGenArgs);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  //detect the flag change from parent component and call createBenchmark if it is true
  ngOnChanges(){
    console.log('submitBenchmark', this.submitBenchmark);
    if(this.submitBenchmark){
      this.createBenchmark();
    }
  }

  createBenchmark() {
    const parent = this;
    console.log('createBenchmark', parent.model.benchmarkData, parent.model.userId, parent.model.projectId)
    if (parent.model.projectId !== '') 
      parent.model.benchmarkData.projectId = parent.model.projectId;
    parent.model.isBtnDisabled = true;
    parent.benchmarkService
      .createBenchmark(parent.model.benchmarkData, parent.model.userId)
      .then((responseData) => {
        console.log(responseData);
        parent.model.isBtnDisabled = false;
        parent.toaster.success(101);
      })
      .catch((data: any) => {
        parent.model.isReadOnly = false;
        parent.model.isBtnDisabled = false;
        if (data) {
          console.log(data);
          parent.toaster.failureWithMessage(parent.getErrorMessage(data)); //backendFix
        } else {
          parent.toaster.failure(102);
        }
      });
  }

  getErrorMessage(error: any) {
    var message = '';
    if (error.error.details && error.error.details[0])
      message = error.error.details[0].message;
    else if (error.error.detail)
      message = error.error.detail.message;
    else
      message = error.error.message;
    return message;
  }

  addModel() {
    if (this.model.benchmarkData.configuration.model.length < 3) {
      this.model.benchmarkData.configuration.model.push(
        new Model('', '', '', 'NA', [new Arg()])
      );
      this.model.disableQuantize[this.model.benchmarkData.configuration.model.length - 1] = true;
      if (this.model.benchmarkData.configuration.model.length == 3) {
        this.model.modelBtnDisable = true;
      }
    }
  }

  addArgs(index: number) {
    if (!this.model.benchmarkData.configuration.model.args) {
      this.model.benchmarkData.configuration.model.args = [];
    }
    this.model.benchmarkData.configuration.model[index].args.push({
      name: '',
      value: '',
    });
  }

  canAddArgs(index: number) {
    if (this.model.benchmarkData.type == CONSTANTS.BENCHMARK_MODALITIES.EMBEDDING && 
      this.model.benchmarkData.configuration.model[index].args.length == 1)
      return true;
    return false;
  }

  onInput(event: Event, ref: NgModel) {
    const inputElement = event.target as HTMLInputElement;
    const regexPattern = /^[a-z0-9-]+$/;
    const currentValue = inputElement.value;

    console.log(currentValue);
    // Filter the input to allow only valid characters
    const filteredValue = currentValue.split('').filter((char) => regexPattern.test(char)).join('');

    // Update the input value with the filtered value
    inputElement.value = filteredValue;
    ref.control.setValue(filteredValue);
  }

// get the model details from modelListData for the selected model name
  onModelChange(event: any, i:number){
    const parent = this;
    console.log('onModelChange', event);
    parent.model.benchmarkData.configuration.model[i].modelName = event.value.name;
    parent.model.benchmarkData.configuration.model[i].modelPathorId = event.value.artifacts.uri.split(this.model.aiClouds3)[1];
    console.log(parent.model.benchmarkData.configuration.model[i].modelPathorId, parent.model.benchmarkData.configuration.model[i].modelName)
  }
  
  onDataTypeChange(event: MatSelectChange, i: number){
    console.log("onDataTypeChange", event, this.model.benchmarkData.configuration.model[i].datatype)
    this.model.benchmarkData.configuration.model[i].datatype = event;
    if (['','fp16','fp32'].includes(this.model.benchmarkData.configuration.model[i].datatype)){
      this.model.disableQuantize[i] = true;
      this.model.benchmarkData.configuration.model[i].quantizeMethod = 'NA';
    }
    else
      this.model.disableQuantize[i] = false;
  }

  //whenever modality changes, fetch metadata by modality & task
  onModalityChange(value: string) {
    const parent = this;
    console.log(value);
    parent.taskList = [];
    parent.modelGenArgs = [];
    parent.model.benchmarkData.configuration.task = '';
    parent.model.benchmarkData.configuration.data.name = '';
    const promiseTaskList = parent.benchmarkService.getBenchmarkMetaDataList(
      value,
      'task'
    );
    const promiseModelGenArgs = parent.benchmarkService.getBenchmarkMetaDataList(
      value,
      'modelGenArgs'
    );
    Promise.all([promiseTaskList, promiseModelGenArgs])
      .then((value: any) => {
      console.log('PromiseTasklist', value);
      parent.taskList = value[0]['tasks'];
        parent.modelGenArgs = value[1]['modelGenArgs'];
    })
    .catch((error) => {
      console.log(error);
    });
  }

  showArgs(i: number) {
    const parent = this;
    if (parent.model.benchmarkData.type != CONSTANTS.BENCHMARK_MODALITIES.CODE && 
      parent.model.benchmarkData.type != CONSTANTS.BENCHMARK_MODALITIES.EMBEDDING) {
      parent.model.benchmarkData.configuration.model[i].args = [];
      return false;
    }
    else
      return true;
  }

  showBatchAndLimit(){
    const parent = this;
    if(parent.model.benchmarkData.type != CONSTANTS.BENCHMARK_MODALITIES.EMBEDDING)
      return true;
    return false;
  }

  //sets options for task list based on modality
  onTaskChange(value: string) {
    const parent = this;
    console.log('Type/Modality', value);
    parent.datasets = [];
    const promisDatasets = parent.benchmarkService.getBenchmarkDatasets(
      parent.model.benchmarkData.type,
      value
    );
    promisDatasets.then((value: any) => {
      console.log('Promise', value);
      parent.datasets = value['datasets'];
      // extract values that does not contain 'infosys' in its string from datasets
      parent.model.publicDatasets = parent.datasets.filter((dataset: any) => !dataset.includes('infosys'));
      parent.model.infyDatasets = parent.datasets.filter((dataset: any) => dataset.includes('infosys'));
    })
      .catch((error) => {
        console.log(error);
      });
  }
  
  onScopeChange(event: any){
    const parent = this;
    if(event == 'public')
      parent.model.publicDatasets = parent.datasets.filter((dataset: any) => !dataset.includes('infosys'));
    else
      parent.model.infyDatasets = parent.datasets.filter((dataset: any) => dataset.includes('infosys'));
  }

  removeModel(modelIndex: number) {
    this.model.benchmarkData.configuration.model.splice(modelIndex, 1);
    this.model.disableQuantize.splice(modelIndex, 1);
    this.model.modelBtnDisable = false;
  }

  removeArgs(modelIndex: number, argIndex: number) {
    this.model.benchmarkData.configuration.model[modelIndex]?.args.splice(
      argIndex,
      1
    );
  }

  open(content: any) {
    const parent = this;
    console.log("open called");
    parent.openConfirmDialog(content);
  }

  private openConfirmDialog(content: any) {
    const parent = this;
    console.log("opening dialog");
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });
  }
}
export interface Storage {
  value: string;
  viewValue: string;
}
