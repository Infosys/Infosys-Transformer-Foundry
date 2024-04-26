/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Directive,ElementRef,HostListener } from '@angular/core';

@Directive({
  selector: '[appCollapseMenu]'
})
export class CollapseMenuDirective {

  constructor(Element: ElementRef) {}
  @HostListener('click', ['$event'])
  onClick(eventPanel: any): void{
   console.log('test');
    if(eventPanel.target.nextSibling.style.display=="block" || eventPanel.target.nextSibling.style.display==''){
      eventPanel.target.nextSibling.style.display='none';
     //eventPanel.target.querySelector(".menuButton").innerText='expand_more';
      eventPanel.target.classList.add("expand");
      eventPanel.target.classList.remove("collapse");
    }
   else{
     eventPanel.target.nextSibling.style.display='block';
     //eventPanel.target.querySelector(".menuButton").innerText='expand_less';
     eventPanel.target.classList.add("collapse");
     eventPanel.target.classList.remove("expand");
   }
    
 }
}
