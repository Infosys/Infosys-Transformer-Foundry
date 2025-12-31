/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable()
export class MessageInfo {
  private msgArray;
  constructor(private httpClient: HttpClient) { }

  // Even though this method contains an async call, it will be called on application load
  // and ensures config file is read completely before loading rest of the application
  load() {
    const parent = this;
    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.get('assets/message-info.json')
        .subscribe(data => {
          parent.msgArray = data['message'];
        });
    });
  }

  /**
   * Method to get message based on message code
   */
  public getMessage(id: number) {
    let msg = ' ';
    this.msgArray.forEach(function (value) {
      if (value.msgCode === id) {
        msg = value.msgText;
      }
      return msg;
    });
    return msg;
  }
}
