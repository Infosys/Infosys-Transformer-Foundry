/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { ApplicationRef, NgModule, Injector, APP_INITIALIZER,CUSTOM_ELEMENTS_SCHEMA } from '@angular/core'; //Needed for MFE Application
import { BrowserModule } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements'; //Needed for MFE Application 
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppMaterialModule } from './modules/app-material.module';
import { AppPluginsModule } from './modules/app-plugins.module';
import { AppBootstrapModule } from './modules/app-bootstrap.module';
import { CommonModule, DatePipe } from '@angular/common';
import { ConfigDataHelper } from './utils/config-data-helper';
import { MessageInfo } from './utils/message-info';
import { UtcToLocalPipe } from "./pipes/utc-to-local.pipe";
import { ModelLeaderboardComponent } from './component/model/model-leaderboard/model-leaderboard.component';
import { JobSubmitComponent } from './component/model/job-submit/job-submit.component';
import { TextLeaderboardComponent } from './component/model/text-leaderboard/text-leaderboard.component';
import { CodeLeaderboardComponent } from './component/model/code-leaderboard/code-leaderboard.component';
import { JobListComponent } from './component/model/job-list/job-list.component';
import { DialogConfirmComponent } from './component/dialog-confirm/dialog-confirm.component';
import { EmbeddingLeaderboardComponent } from './component/model/embedding-leaderboard/embedding-leaderboard.component';

export function initConfig(configDataHelper: ConfigDataHelper, msgInfo: MessageInfo) {
  return () => {
    configDataHelper.load()
    msgInfo.load();
  };
}

@NgModule({
  declarations: [
    AppComponent,
    ModelLeaderboardComponent,
    JobSubmitComponent,
    TextLeaderboardComponent,
    CodeLeaderboardComponent,
    JobListComponent,
    UtcToLocalPipe,
    DialogConfirmComponent,
    EmbeddingLeaderboardComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AppMaterialModule,
    AppPluginsModule,
    AppBootstrapModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    HttpClientModule,
    BrowserAnimationsModule

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
    DatePipe
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  entryComponents: [ModelLeaderboardComponent]
})
export class AppModule { 
  //Needed for MFE Application
  constructor(private injector: Injector, private appRef: ApplicationRef) {}

  private appElementName = 'app-mfe-tf-leaderboard';

  ngDoBootstrap(){
    const parent = this;
    const urlCheck = window.location.hash;
    console.log(urlCheck);

    if(urlCheck){
      //run as integrated application
      const element = createCustomElement(ModelLeaderboardComponent,{ injector:parent.injector });
      //  customElements.define(parent.appElementName,element);
      if (!customElements.get(parent.appElementName)) { customElements.define(parent.appElementName, element); }
    }
    else{
      //run as standalone application
      const appElement = document.createElement(parent.appElementName);
      document.body.appendChild(appElement);
      parent.appRef.bootstrap(AppComponent, appElement);
    }
  }
}