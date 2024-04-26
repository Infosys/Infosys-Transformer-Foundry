/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Directive,ElementRef,HostListener } from '@angular/core';

@Directive({
  selector: '[appwindowScroll]'
})
export class WindowscrollDirective {

  constructor(el: ElementRef) {
    //el.nativeElement.style.backgroundColor = 'yellow';
  
 }


 @HostListener('window:scroll', ['$event'])
 public onWindowScroll(e) {
   
      if (window.pageYOffset > 100) {
        let element = document.getElementById('scrollHeader2');
        element.classList.add('StickyHeader');
      } else {
       let element = document.getElementById('scrollHeader2');
        element.classList.remove('StickyHeader'); 
      }
   }


}
