/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { LocalSessionData } from '../data/local-session-data';

@Injectable({
  providedIn: 'root'
})
export class DataStorageService {

  private localSessionDataKey: string;
  constructor() {
    const browserUrl = location.pathname;
    this.localSessionDataKey = 'lsd-' + browserUrl.replace(/\//g, '').replace('index.html', '').split(';')[0];
  }

  // funcrion to get data from local storage
  getData() {
    const localSessionData: LocalSessionData = JSON.parse(localStorage.getItem(this.localSessionDataKey));
    if(!localSessionData){
      return new LocalSessionData('',0,0,0,0);
    }
    return localSessionData;
  }

  // function to set data in local storage
  setData(localSessionData: LocalSessionData) {
    localStorage.setItem(this.localSessionDataKey, JSON.stringify(localSessionData));
  }

  // function to clear data from local storage
  clearData() {
    localStorage.removeItem(this.localSessionDataKey);
  }

}
