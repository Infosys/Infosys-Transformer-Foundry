/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
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

    // success message
  success(msgCode: number) {
    const parent = this;
    this.message = parent.msgInfo.getMessage(msgCode);
    const snackBarRef = this.messageBar.openFromComponent(SuccessMessagebarComponent, this.config);
  }

  // method to show the appropriate failure message retrieved from the message-info.ts
  failure(msgCode: number) {
    const parent = this;
    this.config.duration = undefined;
    this.message = parent.msgInfo.getMessage(msgCode);
    const snackBarRef = this.messageBar.openFromComponent(FailureMessagebarComponent, this.config);
  }

  // method to show the failure message with the message retrieved from the api
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
    '<div class="tf_msgCtr tf_wb_alert tf_wb_alert-success marB16 clearfix tf_topbarMessage">'
    +'<i aria-hidden="true" class="icon green success-big-icon"></i>'
    +'<div class="tf_alertmsgCtr clearfix"><div class="tf_wb_mainBodyTxt">{{message}}</div>' 
    +'<span aria-label="close message bar"></span></div>' 
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

  setTimeout(){
    timer(2500).subscribe(() => {
      this.messageBar.dismiss();
    });
  }
}

@Component({
  selector: "failure-messagebar-component",
  template:
    '<div class="tf_msgCtr tf_wb_alert tf_wb_alert-error marB16 clearfix">'
    +'<i aria-hidden="true" class="icon icon-rejected red"></i>'
    +'<div class="tf_alertmsgCtr clearfix"><div class="tf_wb_mainBodyTxt">{{message}}</div>' 
    +'<span class="icon black x-16 close-icon tf_vertical-RightCenter" (click)="close()" aria-label="close message bar"></span></div>' 
    +"</div>",
  styles: [],
})
export class FailureMessagebarComponent {
  constructor(private toaster: ToasterServiceService, private messageBar: MatSnackBar) { }

  ngOnInit() {
    this.message = this.toaster.message
  }
  message: string = '';

  close(){
    this.messageBar.dismiss();
  }
}