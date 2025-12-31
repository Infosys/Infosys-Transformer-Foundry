/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MessageInfo } from '../utils/message-info';
import { timer } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ToasterServiceService {
  message: string = '';
  config: any = {
    verticalPosition: "top",
    horizontalPosition: "center"
  }
  constructor(private messageBar: MatSnackBar,
    private msgInfo: MessageInfo) { }

  // function to show success message
  success(msgCode: number) {
    const parent = this;
    this.message = parent.msgInfo.getMessage(msgCode);
    const snackBarRef = this.messageBar.openFromComponent(SuccessMessagebarComponent, this.config);
  }

  // function to show failure message based on the code
  failure(msgCode: number) {
    const parent = this;
    this.config.duration = undefined;
    this.message = parent.msgInfo.getMessage(msgCode);
    const snackBarRef = this.messageBar.openFromComponent(FailureMessagebarComponent, this.config);
  }

  // function to show failure message based on the message
  failureWithMessage(msg: string) {
    const parent = this;
    this.config.duration = undefined;
    parent.message = msg;
    const snackBarRef = this.messageBar.openFromComponent(FailureMessagebarComponent, this.config);
  }
}

@Component({
  selector: "success-messagebar-component",
  template:
  '<div class="alert alert-success d-flex align-items-center">'
  +'<i class="bi bi-check-circle-fill me-2"></i>'
  +'<div>{{message}}</div>' 
  +"</div>",
  styles: [],
})
export class SuccessMessagebarComponent {
  constructor(private toaster: ToasterServiceService, private messageBar: MatSnackBar) { }

  ngOnInit() {
    this.message = this.toaster.message
    this.setTimeout();
  }
  message: string = '';

  // function to close the message bar after 2.5 seconds
  setTimeout(){
    timer(2500).subscribe(() => {
      this.messageBar.dismiss();
    });
  }
}

@Component({
  selector: "failure-messagebar-component",
  template:
  '<div class="alert alert-danger d-flex align-items-center justify-content-between">'
  +'<div>{{message}}</div>'
  +'<span class="material-icons ms-2" style="padding-right:8px; cursor: pointer;" (click)="close()">close</span>'
  +'</div>',
  styles: [],
})
export class FailureMessagebarComponent {
  constructor(private toaster: ToasterServiceService, private messageBar: MatSnackBar) { }

  ngOnInit() {
    this.message = this.toaster.message
  }
  message: string = '';

  // function to close the message bar
  close(){
    this.messageBar.dismiss();
  }
}