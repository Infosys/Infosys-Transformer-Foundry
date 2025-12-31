/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PerformanceMetric, Sensitive, UpdateModelData } from 'src/app/data/update-model-data';
import { ModelService } from 'src/app/services/models.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';

@Component({
  selector: 'app-update-model-details',
  templateUrl: './update-model-details.component.html',
  styleUrls: ['./update-model-details.component.scss']
})
export class UpdateModelDetailsComponent implements OnInit {
  // event emitters
  @Output() nextTab = new EventEmitter<number>();

  // event emitter for the update model data
  @Output() updateModeldtData = new EventEmitter<{}>();

  // input values for the height and width of the tab
  @Input() height: number;
  @Input() width: number;

  // input values for the update model details, project id
  @Input() 
  set inputModelName(inputModelName: string) {
    this.model.updateModelObject.name = inputModelName;
  }
  @Input() 
  set inputModelId(inputModelId: string) {
    this.model.modelId = inputModelId;
  }
  @Input() 
  set inputModelVersion(inputModelVersion: number) {
    //convert if the value is string to number
    if(typeof inputModelVersion === 'string'){
      inputModelVersion = parseInt(inputModelVersion);
    }
    this.model.updateModelObject.version = inputModelVersion;
  }
  @Input() 
  set inputProjectId(inputProjectId: string) {
    this.model.updateModelObject.projectId = inputProjectId;
  }

  // input artifacts 
  @Input() 
  set inputArtifacts(inputArtifacts: string) {
    this.model.updateModelObject.artifacts.storageType = inputArtifacts['storageType'];
    this.model.updateModelObject.artifacts.uri = inputArtifacts['uri'];
  }

  // input model data
  @Input() 
  set inputUpdateModelData(inputUpdateModelData: UpdateModelData) {
    this.model.updateModelObject = inputUpdateModelData;
    console.log("input values", this.model.updateModelObject);
  }

  // model object
  model: any = {
    updateModelObject: new UpdateModelData(),
    isBtnDisabled: false,
    isReadOnly:false,
    modelId: ''
  }

  // show section object
  showSection = {
    container: true,
    envVariables: true,
    ports: true,
    labels: true,
    command: true,
    args: true,
    metadata: true,
    customTags: true,
    owners: true,
    history: true,
    licenses: true,
    references: true,
    citations: true,
    modelDetails: true,
    modelParams: true,
    data: true,
    inputFormatMap: true,
    outputFormatMap: true,
    sensitive: true,
    qAnalysis: true,
    considerations: true,
    storage: true
  }

  // constructor to inject the required services
  constructor(
    private modelService: ModelService,
    private toaster: ToasterServiceService,
    private modalService: NgbModal
  ) { }

  ngOnInit(): void {
  }

  // ngOnChanges to check the changes in the input values
  ngOnChanges(changes: SimpleChanges) {
    console.log("checking changes in update details", this.model.updateModelObject);
    if (changes.inputUpdateModelData && !changes.inputUpdateModelData.firstChange) {
      console.log("calling to emit update details", this.model.updateModelObject);
      this.handleDetailChanges();
    }
  }

  // function to toggle the section
  toggleShowSection(sectionName: string) {
    this.showSection[sectionName] = !this.showSection[sectionName];
  }

  // function to update the model data
  updateModelData() {
    const parent = this;
    parent.model.isReadOnly = true;
    parent.model.isBtnDisabled = true;
    try {
      parent.modelService.updateModelData(parent.model.modelId, parent.model.updateModelObject)
        .then(
          (responseData: any) => {
            parent.model.isReadOnly = true;
            parent.model.isBtnDisabled = false;
            console.log("ResponseData:", responseData);
            parent.toaster.success(112);
          }).catch(
            data => {
              parent.model.isReadOnly = false;
              parent.model.isBtnDisabled = false;
              if (data) {
                parent.toaster.failureWithMessage(data?.["details"]?.[0]?.message || data?.["detail"]?.message || data?.Error || data?.["error"]?.["details"]?.[0]?.message );
              } else {
                parent.toaster.failure(104);
              }
            });
    } catch {
      parent.toaster.failure(104);
    }
  }

  // function to open the confirm dialog
  openConfirmDialog(content) {
    const parent = this;
    parent.modalService
      .open(content, {
        centered: true,
        windowClass: 'square-modal',
      });
  }

  // function to add and remove fields from the UI
  addNewEnvVariables() {
    this.model.updateModelObject.container.envVariables.push({ name: '', value: '' });
  }

  removeEnvVariables(index: number) {
    this.model.updateModelObject.container.envVariables.splice(index, 1);
  }

  addNewPort() {
    this.model.updateModelObject.container.ports.push({ name: '', value: '' });
  }

  removePort(index: number) {
    if(this.model.updateModelObject.container.ports.length != 1)
      this.model.updateModelObject.container.ports.splice(index, 1);
  }

  addNewLabel() {
    this.model.updateModelObject.container.labels.push({ name: '', value: '' });
  }

  removeLabel(index: number) {
    this.model.updateModelObject.container.labels.splice(index, 1);
  }

  addNewCommand() {
    this.model.updateModelObject.container.command.push("");
  }

  removeCommand(index: number) {
    this.model.updateModelObject.container.command.splice(index, 1);
  }

  addNewArgument() {
    this.model.updateModelObject.container.args.push("");
  }

  removeArgument(index: number) {
    this.model.updateModelObject.container.args.splice(index, 1);
  }

  addNewTag(){
    this.model.updateModelObject.metadata.modelDetails.customTags.push({ tags: ''});
  }

  removeTag(index: number){
    this.model.updateModelObject.metadata.modelDetails.customTags.splice(index, 1);
  }

  addOwner(){
    this.model.updateModelObject.metadata.modelDetails.owners.push({ name: '', contact: ''});
  }

  removeOwner(index: number){
    this.model.updateModelObject.metadata.modelDetails.owners.splice(index, 1);
  }

  addHistory(){
    this.model.updateModelObject.metadata.modelDetails.versionHistory.push({ name: '', date:'', diff:'' });
  }

  removeHistory(index: number){
    this.model.updateModelObject.metadata.modelDetails.versionHistory.splice(index, 1);
  }

  addLicense(){
    this.model.updateModelObject.metadata.modelDetails.licenses.push({ identifier: '', customText:'' });
  }

  removeLicense(index: number){
    this.model.updateModelObject.metadata.modelDetails.licenses.splice(index, 1);
  }

  addReferences(){
    this.model.updateModelObject.metadata.modelDetails.references.push({ reference: '' });
  }

  removeReferences(index: number){
    this.model.updateModelObject.metadata.modelDetails.references.splice(index, 1);
  }

  addCitations(){
    this.model.updateModelObject.metadata.modelDetails.citations.push({ style: '', citation:'' });
  }

  removeCitations(index: number){
    this.model.updateModelObject.metadata.modelDetails.citations.splice(index, 1);
  }

  addData(){
    this.model.updateModelObject.metadata.modelParameters.data.push({ name: '', link:'', sensitive: new Sensitive(), classification: '' });
  }

  removeData(index: number){
    this.model.updateModelObject.metadata.modelParameters.data.splice(index, 1);
  }

  addInputFormatMap(){
    this.model.updateModelObject.metadata.modelParameters.inputFormatMap.push({ key: '', value:'' });
  }

  removeInputFormatMap(index: number){
    this.model.updateModelObject.metadata.modelParameters.inputFormatMap.splice(index, 1);
  }

  addOutputFormatMap(){
    this.model.updateModelObject.metadata.modelParameters.outputFormatMap.push({ key: '', value:'' });
  }

  removeOutputFormatMap(index: number){
    this.model.updateModelObject.metadata.modelParameters.outputFormatMap.splice(index, 1);
  }

  addMetrics(){
    this.model.updateModelObject.metadata.quantitativeAnalysis.performanceMetrics.push(new PerformanceMetric());
  } 

  removeMetrics(index: number){
    this.model.updateModelObject.metadata.quantitativeAnalysis.performanceMetrics.splice(index, 1);
  }

  addUsers(){
    this.model.updateModelObject.metadata.considerations.users.push({ description: ''});
  }

  removeUsers(index: number){
    this.model.updateModelObject.metadata.considerations.users.splice(index, 1);
  }

  addUseCases(){
    this.model.updateModelObject.metadata.considerations.useCases.push({ description: ''});
  }

  removeUseCases(index: number){
    this.model.updateModelObject.metadata.considerations.useCases.splice(index, 1);
  }

  addLimitations(){
    this.model.updateModelObject.metadata.considerations.limitations.push({ description: ''});
  }

  removeLimitations(index: number){
    this.model.updateModelObject.metadata.considerations.limitations.splice(index, 1);
  }

  addTradeoffs(){
    this.model.updateModelObject.metadata.considerations.tradeoffs.push({ description: ''});
  }

  removeTradeoffs(index: number){
    this.model.updateModelObject.metadata.considerations.tradeoffs.splice(index, 1);
  }

  addEthicalConsiderations(){
    this.model.updateModelObject.metadata.considerations.ethicalConsiderations.push({ name: '', mitigationStrategy:''});
  }

  removeEthicalConsiderations(index: number){
    this.model.updateModelObject.metadata.considerations.ethicalConsiderations.splice(index, 1);
  }

  addEnvironmentalConsiderations(){
    this.model.updateModelObject.metadata.considerations.environmentalConsiderations.push({ hardwareType: '', hoursUsed:'', cloudProvider:'', computeRegion:'', carbonEmitted: ''});
  }

  removeEnvironmentalConsiderations(index: number){
    this.model.updateModelObject.metadata.considerations.environmentalConsiderations.splice(index, 1);
  }

  removeSensitive(i: number, j: number){
    this.model.updateModelObject.metadata.modelParameters.data[i].sensitive.splice(j, 1);
  }

  removeField(i: number, j: number, k: number){
    this.model.updateModelObject.metadata.modelParameters.data[i].sensitive[j].Fields.splice(k, 1);
  }

  addField(i: number, j: number){
    this.model.updateModelObject.metadata.modelParameters.data[i].sensitive[j].Fields.push("");
  }

  addSensitive(i: number){
    this.model.updateModelObject.metadata.modelParameters.data[i].sensitive.push(new Sensitive());
  }

  // function to handle the changes in the model details
  private handleDetailChanges() {
    const parent = this;
    parent.updateModeldtData.emit(parent.model.updateModelObject);
    console.log("emiting values", parent.model.updateModelObject);
  }
}
