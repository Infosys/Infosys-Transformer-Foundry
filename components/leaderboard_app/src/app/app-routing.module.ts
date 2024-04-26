/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ModelLeaderboardComponent } from './component/model/model-leaderboard/model-leaderboard.component';
const routes: Routes = [
  { path: '', component: ModelLeaderboardComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
