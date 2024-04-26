/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
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
import { LazyElementsModule} from '@angular-extensions/elements';
import { WindowscrollDirective } from './directive/windowScroll/windowScroll.directive';
import { CollapseMenuDirective } from './directive/collapseMenu/collapse-menu.directive';
import { ScrollSpyDirective } from './directive/scrollSpy/scrollSpy.directive';
import { ListModelComponent } from './component/model/list-model/list-model.component';
import { ModelDetailsComponent } from "./component/model/model-details/model-details.component";
import { DateFormatPipe } from './date-format.pipe';
import { CommonModule, DatePipe } from '@angular/common';
import { ConfigDataHelper } from './utils/config-data-helper';
import { BreadcrumbComponent } from './component/breadcrumb/breadcrumb.component';
import { UtcToLocalPipe } from "./pipes/utc-to-local.pipe";
import { ErrorPageComponent } from './component/error-page/error-page.component';
import { ModelLeaderBoardComponent } from './component/model/model-leader-board/model-leader-board.component';
import { ModelHomeComponent } from "./component/model/model-home/model-home.component";
import { ModelBenchmarksComponent } from './component/model/model-benchmarks/model-benchmarks.component';

export function initConfig(configDataHelper: ConfigDataHelper) {
  return () => {
    return configDataHelper.load().then(function (data) {});
  };
}

@NgModule({
  declarations: [
    AppComponent,
    WindowscrollDirective,
    CollapseMenuDirective,
    ScrollSpyDirective,
    ListModelComponent,
    ModelDetailsComponent,
    DateFormatPipe,
    BreadcrumbComponent,
    UtcToLocalPipe,
    ErrorPageComponent,
    ModelLeaderBoardComponent,
    ModelHomeComponent,
    ModelBenchmarksComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AppMaterialModule,
    AppPluginsModule,
    AppBootstrapModule,
    BrowserAnimationsModule,
    // NoopAnimationsModule,
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
      deps: [ConfigDataHelper],
      multi: true
    },
    ConfigDataHelper,
    BreadcrumbComponent,
    DatePipe //required in model zoo for binding date to ui.
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent],
  exports: [CollapseMenuDirective]
})
export class AppModule { }