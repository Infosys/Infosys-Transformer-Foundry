/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-dialog-confirm',
  templateUrl: './dialog-confirm.component.html',
  styleUrls: ['./dialog-confirm.component.scss']
})
export class DialogConfirmComponent implements OnInit {

  @Output() close = new EventEmitter<string>();
  @Output() confirm = new EventEmitter<string>();

  constructor() { }
  ngOnInit(): void {
  }
  //function called on closing the modal window
  onClose() {
    const parent = this;
    parent.close.emit('window closed');
    console.log(this.close);
  }
  //function called on clicking the yes button in the modal window
  onConfirm() {
    const parent =this;
    parent.confirm.emit('yes');
    parent.onClose();
    console.log('yes');
  }
}
