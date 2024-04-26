/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ModelHomeComponent } from "./component/model/model-home/model-home.component";
import { ListModelComponent } from "./component/model/list-model/list-model.component";
import { ModelDetailsComponent } from "./component/model/model-details/model-details.component";
import { ErrorPageComponent } from "./component/error-page/error-page.component";
import { ModelBenchmarksComponent } from "./component/model/model-benchmarks/model-benchmarks.component";


const routes: Routes = [
  //byDefault go to login screen
  { path: "", redirectTo: "modelZoo", pathMatch: "full" },
  {
    path: 'modelZoo',
    children: [
      // to show the list of models
      { path: '', component: ModelHomeComponent },
      // to show the model metadata and model benchmarks
      { path: ":modelId", component: ModelDetailsComponent },
    ],
  },
  { path: "benchmarks", component: ModelBenchmarksComponent },
  { path: "error", component: ErrorPageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }