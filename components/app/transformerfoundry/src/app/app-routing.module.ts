/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { ListPipelineComponent } from "./component/pipeline/list-pipeline/list-pipeline.component";
import { ModelHomeComponent } from "./component/model/model-home/model-home.component";
import { ListModelComponent } from "./component/model/list-model/list-model.component";
import { ModelDetailsComponent } from "./component/model/model-details/model-details.component";
import { ListJobComponent } from "./component/job/list-job/list-job.component";
import { CreatePipelineHomeComponent } from "./component/pipeline/create-pipeline-home/create-pipeline-home.component";
import { ListProjectComponent } from "./component/project/list-project/list-project.component";
import { CreateProjectComponent } from "./component/project/create-project/create-project.component";
import { CreateJobHomeComponent } from "./component/job/create-job-home/create-job-home.component";
import { LoginComponent } from "./component/login/login.component";
import { LoginGuard } from "./component/login/login-guard.guard";
import { ErrorPageComponent } from "./component/error-page/error-page.component";
import { ModelDeployHomeComponent } from "./component/model/model-deploy-home/model-deploy-home.component";
import { ModelBenchmarksComponent } from "./component/model/model-benchmarks/model-benchmarks.component";
import { PlaygroundComponent } from "./component/playground/playground.component";

import { RagDataRegisterComponent } from "./component/dataset/rag-data-register/rag-data-register.component";
import { DatasetHomeComponent } from "./component/dataset/dataset-home/dataset-home.component";
import { RagPlaygroundHomeComponent } from "./component/playground/rag-playground-new/rag-playground-home/rag-playground-home.component";


const routes: Routes = [
 
  //byDefault go to login screen
  { path: "", redirectTo: "modelZoo", pathMatch: "full" },

  

  { path: "login", component: LoginComponent },
  { path: "error", component: ErrorPageComponent },
  {
    path: "modelZoo",
    children: [
      // to show leaderboard tab
      { path: "", component: ModelHomeComponent },

      // { path: '', component: ListModelsComponent },

      { path: ":modelId", component: ModelDetailsComponent },
    ],
    canActivate: [LoginGuard],
    canActivateChild: [LoginGuard],
  },
  {
    path: "playground",
    component: PlaygroundComponent,
  },
  {
    path: "rag-playground",
    component: RagPlaygroundHomeComponent,
  },
  {
    path: "projects",
    children: [
      { path: "", component: ListProjectComponent },
      { path: "create", component: CreateProjectComponent },
      {
        path: ":pid",
        children: [
          {
            path: "pipelines",
            children: [
              { path: "", component: ListPipelineComponent },
              { path: "view/:id", component: CreatePipelineHomeComponent },
              { path: "create", component: CreatePipelineHomeComponent },
            ],
          },
          { path: "view", component: CreateProjectComponent },
          { path: "edit", component: CreateProjectComponent },
          {
            path: "experiments",
            children: [
              { path: "", component: ListJobComponent },
              { path: "view/:id", component: CreateJobHomeComponent },
              { path: ":id", component: CreateJobHomeComponent },
            ],
          },
          {
            path: "benchmarks",
            children: [{ path: "", component: ModelBenchmarksComponent }],
          },
         
          {
            path: "datasets",
            children: [
              {path: "", component: DatasetHomeComponent},
              {path: "create", component: RagDataRegisterComponent},//for creating 
              {path:"update/:id",component:RagDataRegisterComponent},//for updating
              { path: "view", children:[
                {path:":id",component:RagDataRegisterComponent}]},
              

              
              

            ],
            
          },
          {path:"",redirectTo:'/dataset-list',pathMatch:'full'},
          
          {
            path: ":modelType/:modelId",
            children: [
              { path: "", component: ModelDetailsComponent },
              { path: ":deploy", component: ModelDeployHomeComponent },
            ],
          },
          // to show leaderboard
          { path: ":models", component: ModelHomeComponent },
          // Always keep this at the end, this most probably won't be called.
          { path: ":models", component: ListModelComponent },

        ],
      },
     
    ],
    
    canActivate: [LoginGuard],
    canActivateChild: [LoginGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
