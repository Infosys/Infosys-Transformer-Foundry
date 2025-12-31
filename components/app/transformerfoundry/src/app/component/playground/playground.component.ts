/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
import { Component, OnInit, ViewEncapsulation,ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataStorageService } from '../../services/data-storage.service';
import { ToasterServiceService } from 'src/app/services/toaster-service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import axios from 'axios';
import { MatSelectChange } from '@angular/material/select';  // Import MatSelectChange type for event
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-playground',
  templateUrl: './playground.component.html',
  styleUrls: ['./playground.component.scss', './playground.css', './playground-editor.css'],
  encapsulation: ViewEncapsulation.ShadowDom
  

})
export class PlaygroundComponent implements OnInit {
  model: any = {
    height: 0,
    width: 0
  };
  userId: string;
  savePayload: any;
    // Object to store dialog form data
    dialogData = {
      domain: '', // Comma-separated list of domains
      name: '',
      conversationRole: 'user', // Default role
      // Purpose: '',
      mode: 'chat', // Default mode
      usecase:''  
    };
    isFormValid(): boolean {
      return (
        this.dialogData.name.trim() !== '' &&
        this.dialogData.conversationRole.trim() !== '' &&
        this.dialogData.mode.trim() !== '' &&
        this.dialogData.usecase.trim() !== ''
      );
    }
    modes = [
      { value: 'text', viewValue: 'Text' },
      { value: 'chat', viewValue: 'Chat' },
      { value: 'video', viewValue: 'Video' },
    ];

   

  @ViewChild('confirmAction') confirmAction;

  constructor(private httpClient: HttpClient, private storageService: DataStorageService,private toaster: ToasterServiceService, private modalService: NgbModal) { }

  ngOnInit() {
    this.userId = this.storageService.getData().userId;
    console.log('userId', this.userId);
    this.sendUserIdToReactApp();

    this.listenToShowToasterEvent();
    this.listenToOpenSaveConfirmDialog();
    
  }
  sendUserIdToReactApp(): void {

   
    console.log('Dispatching sendUserId event with userId:', this.userId); // Log before dispatching
    const event = new CustomEvent('sendUserId', { detail: this.userId });
    window.dispatchEvent(event);
  }

 
  // this is for showing toaster message for save button in open playground
  listenToShowToasterEvent(): void {
    window.addEventListener('showToaster', (event: CustomEvent) => {
      const msgCode = event.detail.msgCode;
      if (msgCode === 105) {
        this.toaster.success(msgCode); // Show success message
      } else if (msgCode === 125) {
        this.toaster.failure(msgCode); // Show error message
      } else {
        this.toaster.failure(999); // Show error message if code is not found
      }
    });}

    // this is for showing save confirmation dialog in open playground
    listenToOpenSaveConfirmDialog(): void {
       
      window.addEventListener('openSaveConfirmDialog', (event: CustomEvent) => {
        console.log('Received payload from event:', event.detail.payload); // Debugging: Log the payload from the event
        this.savePayload = event.detail.payload || {}; // Initialize savePayload with the payload from the event
        this.openConfirmDialog(); 
      });
    }

    openConfirmDialog(): void {
      const modalRef = this.modalService.open(this.confirmAction, {
        centered: true,
        windowClass: 'square-modal playground-modal',
      });
  
      modalRef.result.then(
        (result) => {
          if (result === 'confirm') {
         
            this.handleConfirmSave(modalRef);
          }
        },
        (reason) => {
          console.log('Dismissed');
        }
      );
    }

    

    handleConfirmSave(modal:any): void {
      // const payload = this.savePayload;

      // Merge dialogData into the payload
      console.log('Dialog Data:', this.dialogData); // Debugging: Log the dialogData object
      console.log('Save Payload before merge:', this.savePayload); // Debugging: Log the savePayload object
      const domains = this.dialogData.domain
      .split(',')
      .map((d: string) => d.trim())
      .filter((d: string) => d);

      // const payload
      this.savePayload= {
      ...this.savePayload,
      domain: domains,
      name: this.dialogData.name,
      conversationRole: this.dialogData.conversationRole,
      mode: this.dialogData.mode,
      usecase: this.dialogData.usecase // Include usecase if it's part of the form
    };
    console.log('Updated Save Payload:', this.savePayload); // Debugging: Log the updated savePayload

  const payload = this.savePayload;
    console.log('Final Payload:', payload);
    // Dispatch the payload to react app
    // const event = new CustomEvent('updatePromptLibrary', { detail: payload });
    // console.log('Dispatching updatePromptLibrary event withlll payload:', payload);
    // window.dispatchEvent(event);
    modal.close();
   
      this.httpClient.post("http://localhost:30008/api/v1/library/prompt", payload, {
        headers: {
          'userId': "admin@xyz.com" // Ensure this header is included if required
        },
        params: {
          projectId: '85e24b401351d13eb2c2f7c3da101' // Include necessary parameters
        }
      })
     
      .subscribe({
        next: (response) => {
          // Success handling
          console.log('Save response:', response);
          this.toaster.success(105); // Show success message
           // Notify React to refresh the data
      const event = new CustomEvent('updatePromptLibrary');
      console.log('Dispatching  updatePromptLibrary event');
      window.dispatchEvent(event);

          modal.close(); // Close the modal after success
        },
        error: (error) => {
          // Error handling
          console.error('Error saving data:', error);
          this.toaster.failure(125); // Show error message
        }
      });
    }
 



  
 

  }

  
