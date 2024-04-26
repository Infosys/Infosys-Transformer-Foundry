import { Component, Input, OnInit } from '@angular/core';
import { Arg, BenchmarkData, Model } from '../../../data/benchmark-data';
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
    modelName: ''
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

  //initialize the component with the benchmark metadata
  ngOnInit(): void {
    const parent = this;
    parent.model.urlCheck = window.location.hash;
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

  //create a benchmark
  createBenchmark() {
    const parent = this;
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
        if (data?.error?.detail?.message) {
          console.log(data);
          parent.toaster.failureWithMessage(data?.error?.detail?.message); 
        } else {
          parent.toaster.failure(102);
        }
      });
  }

  //add models to the benchmark
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

  //add arguments to the model
  addArgs(index: number) {
    if (!this.model.benchmarkData.configuration.model.args) {
      this.model.benchmarkData.configuration.model.args = [];
    }
    this.model.benchmarkData.configuration.model[index].args.push({
      name: '',
      value: '',
    });
  }

  //filter the input to allow only valid characters
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

  //on change of datatype, enable/disable quantize method
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

  //show arguments based on modality
  showArgs(i: number){
    const parent = this;
    if(parent.model.benchmarkData.type != CONSTANTS.BENCHMARK_MODALITIES.CODE)
    {
      parent.model.benchmarkData.configuration.model[i].args = [];
      return false;
    }
    else
      return true;
  }

  //show batch and limit based on modality
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
    })
      .catch((error) => {
        console.log(error);
      });
  }

  //removing models from the UI
  removeModel(modelIndex: number) {
    this.model.benchmarkData.configuration.model.splice(modelIndex, 1);
    this.model.disableQuantize.splice(modelIndex, 1);
    this.model.modelBtnDisable = false;
  }

  //removing arguments from the UI
  removeArgs(modelIndex: number, argIndex: number) {
    this.model.benchmarkData.configuration.model[modelIndex]?.args.splice(
      argIndex,
      1
    );
  }

  //open the modal confirmation window
  open(content: any, isBtnDisabled: boolean) {
    const parent = this;
    parent.openConfirmDialog(content);
  }

  //open the modal confirmation window
  private openConfirmDialog(content: any) {
    const parent = this;
    parent.modalService
      .open(content, {
        ariaLabelledBy: 'modalTitle',
        windowClass: 'web_custom_modal tf_modal-sm',
      })
      .result.then(
        () => {
          document
            .getElementsByTagName('html')[0]
            .classList.remove('tf_modaloverflow');
        },
        () => {
          document
            .getElementsByTagName('html')[0]
            .classList.remove('tf_modaloverflow');
        }
      );
    document.getElementsByTagName('html')[0].classList.add('tf_modaloverflow');
    document.getElementsByTagName('ngb-modal-backdrop')[0].removeAttribute('style')
  }
}
export interface Storage {
  value: string;
  viewValue: string;
}
