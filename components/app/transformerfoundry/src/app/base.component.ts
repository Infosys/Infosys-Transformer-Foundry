/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, OnInit, Directive } from '@angular/core';
import { CONSTANTS } from './common/constants';
import { FeatureAccessMode } from './data/feautre-access-data';
import { SessionService } from './services/session.service';
import { ConfigDataHelper } from './utils/config-data-helper';

@Directive()
export abstract class BaseComponent implements OnInit {
  constructor(public sessionService: SessionService,
              public configDataHelper: ConfigDataHelper) 
  { }
  
  bmodel: any = {
    FID: CONSTANTS.FEATURE_ID_CONFIG,
    FID_ERR_MSG: CONSTANTS.FEATURE_ERROR_MSG,
  }

  ngOnInit() { }

  // function to get feature access mode
  getFeature(featureId: string): FeatureAccessMode {
    return this.sessionService.getFeatureAccessModeDataFor(featureId);
  }

}
