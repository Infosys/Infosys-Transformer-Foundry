/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { FeatureAccessMode } from '../data/feautre-access-data';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConfigDataHelper } from '../utils/config-data-helper';
import { DataStorageService } from './data-storage.service';
import { CONSTANTS } from '../common/constants';

@Injectable({
  providedIn: 'root'
})
export class SessionService {

  private featureAuthMap = {};
  constructor(private httpClient: HttpClient, public configDataHelper: ConfigDataHelper, private storageService: DataStorageService) {
    const parent = this;
    parent.getData().subscribe((response: any) => {
      console.log(response)
      response.response.featureAuthDataList.map(item => {
        parent.featureAuthMap[item.featureId] = item.accessLevelCde;
      });
    });
   }

   getData(){
    return this.httpClient.get('assets/json/auth-session-data.json');
   }

  getFeatureAccessModeDataFor(featureId: string): FeatureAccessMode {
    const parent = this;
    let featureAccessMode: FeatureAccessMode = new FeatureAccessMode();
    const accessLevelCde = parent.featureAuthMap[featureId];
    if (accessLevelCde != null) {
      const checkForRightToLeftBitPosition = (accessLevelCde, bitRightToLeftPosition) => {
        const accessLevelBinary = (accessLevelCde >>> 0).toString(2);
        const accessLevelEnabledBit = (accessLevelBinary.length >= bitRightToLeftPosition) ? accessLevelBinary.charAt(accessLevelBinary.length - bitRightToLeftPosition) : "0";
        return (accessLevelEnabledBit === "1") ? true : false;
      }
      // right to left. i.e. Visible -> Enabled
      featureAccessMode.isVisible = checkForRightToLeftBitPosition(accessLevelCde, 1);
      featureAccessMode.isEnabled = checkForRightToLeftBitPosition(accessLevelCde, 2);
    }
    // console.log("Access Mode Check for : ", featureId, featureAccessMode);
    return featureAccessMode;
  }
}
