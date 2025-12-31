/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { BrowserModule } from '@angular/platform-browser';
import { APP_INITIALIZER, CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AppMaterialModule } from './modules/app-material.module';
import { AppPluginsModule } from './modules/app-plugins.module';
import { AppBootstrapModule } from './modules/app-bootstrap.module';
import { HttpClientModule } from '@angular/common/http';
import { MatPaginatorModule } from '@angular/material/paginator';
import { LazyElementsModule} from '@angular-extensions/elements';
import { ListPipelineComponent } from './component/pipeline/list-pipeline/list-pipeline.component';
import { ListModelComponent } from './component/model/list-model/list-model.component';
import { ModelDetailsComponent } from "./component/model/model-details/model-details.component";
import { ListJobComponent } from './component/job/list-job/list-job.component';
import { DateFormatPipe } from './date-format.pipe';
import { CreatePipelineDetailsComponent } from './component/pipeline/create-pipeline-details/create-pipeline-details.component';
import { CreatePipelineFlowComponent } from './component/pipeline/create-pipeline-flow/create-pipeline-flow.component';
import { CreatePipelineSummaryComponent } from './component/pipeline/create-pipeline-summary/create-pipeline-summary.component';
import { CreatePipelineExecutionComponent } from './component/pipeline/create-pipeline-execution/create-pipeline-execution.component';
import { CreatePipelineDialogContentComponent } from './component/pipeline/create-pipeline-dialog-content/create-pipeline-dialog-content.component';
import { CommonModule, DatePipe } from '@angular/common';
import { CreatePipelineHomeComponent } from './component/pipeline/create-pipeline-home/create-pipeline-home.component';
import { ConfigDataHelper } from './utils/config-data-helper';
import { MessageInfo } from './utils/message-info';
import { DialogConfirmComponent } from './component/dialog-confirm/dialog-confirm.component';
import { UtilityService } from './services/utility.service';
import { BreadcrumbComponent } from './component/breadcrumb/tf-breadcrumb.component';
import { UtcToLocalPipe } from "./pipes/utc-to-local.pipe";
import { LoginComponent } from './component/login/login.component';
import { CreateProjectComponent } from './component/project/create-project/create-project.component';
import { ListProjectComponent } from './component/project/list-project/list-project.component'
import { CreateJobHomeComponent } from './component/job/create-job-home/create-job-home.component';
import { CreateJobDetailsComponent } from './component/job/create-job-details/create-job-details.component';
import { CreateJobSummaryComponent } from './component/job/create-job-summary/create-job-summary.component';
import { CreateJobExecutionComponent } from './component/job/create-job-execution/create-job-execution.component';
import { CreateJobDialogContentComponent } from './component/job/create-job-dialog-content/create-job-dialog-content.component';
import { ErrorPageComponent } from './component/error-page/error-page.component';
import { ModelLeaderBoardComponent } from './component/model/model-leader-board/model-leader-board.component';
import { ModelHomeComponent } from "./component/model/model-home/model-home.component";
import { ModelDeployHomeComponent } from './component/model/model-deploy-home/model-deploy-home.component';
import { ModelDeployDetailsComponent } from './component/model/model-deploy-details/model-deploy-details.component';
import { UpdateModelDetailsComponent } from './component/model/update-model-details/update-model-details.component';
import { ModelEndpointDetailsComponent } from './component/model/model-endpoint-details/model-endpoint-details.component';
import { ModelBenchmarksComponent } from './component/model/model-benchmarks/model-benchmarks.component';
import { ImportPipelineComponent } from './component/pipeline/import-pipeline/import-pipeline.component';

export function initConfig(configDataHelper: ConfigDataHelper, msgInfo: MessageInfo) {
  return () => {
    return configDataHelper.load().then(function (data) {
      msgInfo.load();
    });
  };
}

@NgModule({
  declarations: [
    AppComponent,
    ListPipelineComponent,
    ListModelComponent,
    ModelDetailsComponent,
    ListJobComponent,
    DateFormatPipe,
    CreatePipelineDetailsComponent,
    CreatePipelineFlowComponent,
    CreatePipelineSummaryComponent,
    CreatePipelineExecutionComponent,
    CreatePipelineDialogContentComponent,
    CreatePipelineHomeComponent,
    ImportPipelineComponent,
    DialogConfirmComponent,
    BreadcrumbComponent,
    UtcToLocalPipe,
    LoginComponent,
    CreateProjectComponent,
    ListProjectComponent,
    CreateJobHomeComponent,
    CreateJobDetailsComponent,
    CreateJobSummaryComponent,
    CreateJobExecutionComponent,
    CreateJobDialogContentComponent,
    ErrorPageComponent,
    ModelLeaderBoardComponent,
    ModelHomeComponent,
    ModelDeployHomeComponent,
    ModelDeployDetailsComponent,
    ModelEndpointDetailsComponent,
    ModelBenchmarksComponent,
    UpdateModelDetailsComponent,
    ],
    imports: [
    BrowserModule,
    AppRoutingModule,
    AppMaterialModule,
    AppPluginsModule,
    AppBootstrapModule,
    BrowserAnimationsModule,
    MatPaginatorModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    CommonModule,
    AppMaterialModule,
    LazyElementsModule,
  ],
  providers: [
    {
      provide: APP_INITIALIZER,
      useFactory: initConfig,
      deps: [ConfigDataHelper, MessageInfo],
      multi: true
    },
    ConfigDataHelper,
    MessageInfo,
    UtilityService,
    BreadcrumbComponent,
    DatePipe //required in model zoo for binding date to ui.
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent],
  // exports: [CollapseMenuDirective]
})
export class AppModule { }