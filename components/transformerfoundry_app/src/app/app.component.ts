/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, ViewChild} from "@angular/core";
// import { AppUtilServices } from "../app/services/app-util.services";
import { PerfectScrollbarConfigInterface } from "ngx-perfect-scrollbar";
import { DataStorageService } from "./services/data-storage.service";
import { ActivatedRoute, Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent {
  model = {
    projectId: undefined,
    projectName: '',
    userId: '',
    mzoolink: '/modelZoo',
    versionNumber: ''
  }

  constructor( 
    // private codeCp: AppUtilServices, 
    private router: Router,
    private storageService: DataStorageService, 
    private route: ActivatedRoute, 
    private http: HttpClient
  ) { }

  //ngOnInit method used to get the projectId from the url, get the version number and set the middle height of the code container
  ngOnInit(): void {
    const parent = this;
    parent.route.params.subscribe(params => {
      parent.model.projectId = params['pid'];
    });
    // this.codeCp.middleHeight();
    parent.getVersionNumber();
  }

  //hide menu on click of body
  @HostListener("document:click", ["$event"]) onDocumentClick(event) {
    document.getElementById("nav").classList.add("tf_Hide");
    // document.body.style.overflow = 'auto';
  }

  clickactive(eventObj) {
    this.model.userId = this.storageService.getData().userId;
    // this.codeCp.clickactiveClass(eventObj);
  }

  skipLinkPath: string;

  tf_mainHamburger(eventObj) {
    // this.codeCp.tf_hamburger_Click(eventObj);
  }

  tf_mainMenu() {
    // this.codeCp.tf_menu_Click();
  }

  tf_mainSearch() {
    // this.codeCp.tf_mainSearch_Click();
  }
  fullView() {
    // this.codeCp.fullView_Click();
  }

  // ripcolor = this.codeCp.ripcolor;

  codeView = false;
  designView = true;

  codeCopy(thisElement) {
    // this.codeCp.codeCopyFunc(thisElement);
  }

  changeView(thisElement, designViewParam) {
    // this.codeCp.changeViewService(thisElement, designViewParam);
  }

  public scrollConfig: PerfectScrollbarConfigInterface = {
    suppressScrollX: true,
    wheelSpeed: 4,
    minScrollbarLength: 20,
    maxScrollbarLength: 80,
  };

  setpreference() {
    this.tabs.realignInkBar();
    document.getElementById("NotificationCtr").style.display = "none";
    document.getElementById("PreferenceCtr").style.display = "block";
  }
  
  backtoNotification() {
    document.getElementById("NotificationCtr").style.display = "block";
    document.getElementById("PreferenceCtr").style.display = "none";
  }

  tf_toggleRightpanel() {
    // this.codeCp.tf_toggleRightpanel_Click();
  }

  @ViewChild("tabs") tabs;
  selectedIndex: number;

  //function to navigate to model zoo page
  navigateToModelZoo() {
    this.router.navigate(['/modelZoo']);
  }

  //function to check if the current page is login page
  isLoginPage(): boolean {
    return this.router.url.includes('/login');
  }

  //Write a function to read the version.txt file and display the version number in the footer
  getVersionNumber() {
    const parent = this;
    parent.http.get('assets/app-version.txt', {responseType: 'text'}).subscribe(data => {
      const content = data.split('\n');
      content.forEach(line => {
        if(parent.model.versionNumber !== ''){
          parent.model.versionNumber += '.';
        }
        const parts = line.split('=');
        if (parts.length === 2) {
          parent.model.versionNumber+= parts[1].trim();
        }
      });
    },
      _error => {
        console.log(_error)
        }
      );

  }

}
