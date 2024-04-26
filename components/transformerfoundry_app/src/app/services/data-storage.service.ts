/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { LocalSessionData } from '../data/local-session-data';
import { ConfigDataHelper } from '../utils/config-data-helper';

@Injectable({
  providedIn: 'root'
})
export class DataStorageService {

  private localSessionDataKey: string;
  constructor() {
    const browserUrl = location.pathname;
    this.localSessionDataKey = 'lsd-' + browserUrl.replace(/\//g, '').replace('index.html', '').split(';')[0];
  }

  //getData method used to get the local session data
  getData() {
    const localSessionData: LocalSessionData = JSON.parse(localStorage.getItem(this.localSessionDataKey));
    if(!localSessionData){
      return new LocalSessionData('',0,0,0,0);
    }
    return localSessionData;
  }

  //setData method used to set the local session data
  setData(localSessionData: LocalSessionData) {
    localStorage.setItem(this.localSessionDataKey, JSON.stringify(localSessionData));
  }

  //clearData method used to clear the local session data
  clearData() {
    localStorage.removeItem(this.localSessionDataKey);
  }

}
