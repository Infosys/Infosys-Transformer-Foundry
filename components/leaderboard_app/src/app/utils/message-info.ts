/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MESSAGE } from '../common/message-info';
@Injectable()
export class MessageInfo {
  private msgArray:any = [];
  constructor(private httpClient: HttpClient) { }

  // Even though this method contains an async call, it will be called on application load
  // and ensures config file is read completely before loading rest of the application
  load() {
    const parent = this;
    parent.msgArray = MESSAGE.message;
  }

  // Method to get value of a property from message file
  public getMessage(id: number) {
    let msg = ' ';
    this.msgArray.forEach(function (value:any) {
      if (value.msgCode === id) {
        msg = value.msgText;
      }
      return msg;
    });
    return msg;
  }
}
