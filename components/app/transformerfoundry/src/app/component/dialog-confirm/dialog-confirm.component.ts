/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-dialog-confirm',
  templateUrl: './dialog-confirm.component.html',
  styleUrls: ['./dialog-confirm.component.scss']
})
export class DialogConfirmComponent implements OnInit {

  // close and confirm event emitters
  @Output() close = new EventEmitter<string>();
  @Output() confirm = new EventEmitter<string>();

  constructor() { }
  ngOnInit(): void {
  }

  // close the dialog on cancel or close button click
  onClose() {
    const parent = this;
    parent.close.emit('window closed');
    console.log(this.close);
  }

  // confirm the opened dialog window
  onConfirm() {
    const parent =this;
    parent.confirm.emit('yes');
    parent.onClose();
    console.log('yes');
  }


}
