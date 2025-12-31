
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 /** ===============================================================================================================*
 * (C) 2023 Infosys Limited, Bangalore, India. All Rights Reserved.                                                *
 * Version: 2.0                                                                                                    *
 *                                                                                                                 *
 * Except for any open source software components embedded in this Infosys proprietary software program            *
 * ("Program"), this Program is protected by copyright laws, international treaties and other pending or           *
 * existing intellectual property rights in India, the United States and other countries. Except as expressly      *
 * permitted, any unauthorized reproduction, storage, transmission in any form or by any means (including          *
 * without limitation electronic, mechanical, printing, photocopying, recording or otherwise), or any              *
 * distribution of this Program, or any portion of it, may result in severe civil and criminal penalties, and will *
 * be prosecuted to the maximum extent possible under the law.                                                     *
 * =============================================================================================================== *
 */

import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot } from '@angular/router';
import { DataStorageService } from 'src/app/services/data-storage.service';

@Injectable({
  providedIn: 'root'
})
export class LoginGuard implements CanActivate, CanActivateChild {

  isLoggedIn = false;

  constructor(private storageService: DataStorageService, private router: Router) { }

  checkUserId(): boolean {
    const sessionData = this.storageService.getData();
    console.log("checkUserId", sessionData);
    //return true if it empty
    return sessionData.userId === "";
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    //if userId empty this runs
    if (this.checkUserId()) {
      this.router.navigate(['login'], { queryParams: { returnUrl: state.url } })
      // alert("You should login first")
      return false;
    } else {
      return true;
    }
  }

  canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    //if userId empty this runs
    if (this.checkUserId()) {
      this.router.navigate(['login'], { queryParams: { returnUrl: state.url } })
      // alert("You should login first")
      return false;
    } else {
      return true;
    }
  }

}