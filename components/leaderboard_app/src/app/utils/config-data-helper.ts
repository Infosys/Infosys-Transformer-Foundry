/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CONFIG } from '../common/config-data';

@Injectable()
export class ConfigDataHelper {
  private configData: any;
  constructor(private httpClient: HttpClient) { }

  // Even though this method contains an async call, it will be called on application load
  // and ensures config file is read completely before loading rest of the application
  load() {
    const parent = this;
    parent.configData = CONFIG.config;
    
  }

  // Method to get value of a property from config file
  getValue(propertyName: string) {
    if (this.configData) {
      const value = this.readValue(propertyName)
      if (value) {
        return this.updateSchemeIfUrl(value);
      }
    }
    return null;
  }

  /**
   * Method to read nested properties
   */
  private readValue(propertyName:string) {
    let obj = this.configData
    propertyName.split(".").forEach(element => {
      obj = obj[element]
    });
    return obj
  }

  /**
   * Method to convert http:// to https:// and vice versa depending on current
   * scheme of application obtained from current URL of web page.
   * Applications cannot have a mix of http and https so this conversion is
   * mandatory.
   */
  private updateSchemeIfUrl(value: any) {
    if (!((typeof value === 'string') || (value instanceof String))) {
      return value
    }
    const urlTokens = value.split("//")
    if (urlTokens.length!=2) {
      return value
    }
    const urlScheme = urlTokens[0].toLowerCase()
    if ((urlScheme != "http:") && (urlScheme != "https:") ) {
      return value
    }
    const currentScheme = window.location.protocol.toLowerCase();
    if (urlScheme!= currentScheme) {
      value = value.replace(urlScheme, currentScheme)
    }
    if (currentScheme=='https:') {
      value = value.replace(':80/', '/')
    } else if (currentScheme=='http:') {
      value = value.replace(':443/', '/')
    }
    return value;
  }
}
