/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { NgModule } from '@angular/core';
import { PerfectScrollbarModule, PERFECT_SCROLLBAR_CONFIG, PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CarouselModule } from 'ngx-owl-carousel-o';
import { NgxMaterialTimepickerModule } from 'ngx-material-timepicker';
import { BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { PopoverModule } from 'ngx-bootstrap/popover';
import { Ng5SliderModule } from 'ng5-slider';
import { JoyrideModule } from 'ngx-joyride';
const DEFAULT_PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
  suppressScrollX: true,
  minScrollbarLength: 20,
  maxScrollbarLength: 80
};
@NgModule({
  declarations: [],
  imports: [
    BsDatepickerModule.forRoot(),
    PopoverModule.forRoot(),
    PerfectScrollbarModule,
    NgbModule,
    CarouselModule,
    NgxMaterialTimepickerModule,
    Ng5SliderModule,
    JoyrideModule.forRoot()
  ],
  exports: [
    PerfectScrollbarModule,
    NgbModule,
    CarouselModule,
    NgxMaterialTimepickerModule,
    BsDatepickerModule,
    PopoverModule,
    Ng5SliderModule,
    JoyrideModule

  ],
  providers: [
    {
      provide: PERFECT_SCROLLBAR_CONFIG,
      useValue: DEFAULT_PERFECT_SCROLLBAR_CONFIG
    }
  ]
})

export class AppPluginsModule {


}

