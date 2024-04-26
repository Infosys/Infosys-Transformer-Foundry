/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  constructor() { }
    model: any = {
      standaloneFlag:false,
    }

  ngOnInit(): void {
    const parent = this;
    const urlCheck = window.location.hash;
    console.log(urlCheck);

    if(!urlCheck){
      parent.model.standaloneFlag = true;
      console.log(parent.model.standaloneFlag);
    }
  }
}

