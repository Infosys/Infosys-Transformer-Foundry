/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, HostListener, ViewChild} from "@angular/core";
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
    private router: Router,
    private storageService: DataStorageService, 
    private route: ActivatedRoute, 
    private http: HttpClient) {
  }

  ngOnInit(): void {
    const parent = this;
    parent.route.params.subscribe(params => {
      parent.model.projectId = params['pid'];
    });
    parent.updateProjectName();
    parent.getVersionNumber();
  }

  //hide menu on click of body
  @HostListener("document:click", ["$event"]) onDocumentClick(event) {
    document.getElementById("sidebar").classList.add('sidebar-hide');
    document.getElementById("sidebar").classList.remove('show');
  }

  clickProfile() {
    this.model.userId = this.storageService.getData().userId;
  }

  // function to toggle the sidebar
  toggleSidebar(eventObj) {
    eventObj.stopPropagation();
    const sidebar = document.getElementById('sidebar');
    
    if (sidebar.classList.contains('show')) {
      sidebar.classList.remove('show');
      sidebar.classList.add('sidebar-hide');
      document.body.style.overflow = 'auto';
    } else {
      sidebar.classList.add('show');
      sidebar.classList.remove('sidebar-hide');
      document.body.style.overflow = 'hidden';
      sidebar.focus();
    }
  }

  skipLinkPath: string;
  public scrollConfig: PerfectScrollbarConfigInterface = {
    suppressScrollX: true,
    wheelSpeed: 4,
    minScrollbarLength: 20,
    maxScrollbarLength: 80,
  };

  @ViewChild("tabs") tabs;
  selectedIndex: number;

  isHidden: boolean = true;
  isSidebarOpen = false;

  // function to check if the current page is home page
  isHomePage(): boolean {
    this.updateProjectId();
    const ishome = this.model.projectId == undefined || this.isPathEndswith('/projects')
                   || (this.isPathStartswith('/projects') && this.model.projectName=='') 
                   || this.isPathStartswith('/modelZoo') || this.isPathEndswith('/modelZoo')
                   || (this.isPathStartswith('/playground') && this.model.projectName=='')
                   || (this.isPathStartswith('/rag-playground') && this.model.projectName=='');
    return ishome;
  }

  // function to check if the current page is project page
  private isPathEndswith(path){
    let routePath = this.router.url.split('?')[0];
    return routePath.startsWith(path) && routePath.endsWith(path);
  }

  // function to check if the current page is project page
  private isPathStartswith(path){
    let routePath = this.router.url.split('?')[0];
    return routePath.startsWith(path);
  }

  // function to navigate to model zoo
  navigateToModelZoo() {
    if (this.model.projectId != undefined && this.model.projectName != '') {
      this.router.navigate(['/projects', this.model.projectId, 'modelZoo'], { queryParams: { pn: this.model.projectName}});
    } else {
      this.router.navigate(['/modelZoo']);
    }
  }

  // function to navigate to playground
  navigateToPlayground(playgroundType:string) {
    if (this.model.projectId != undefined && this.model.projectName != '') {
      this.router.navigate([`/${playgroundType}`], { queryParams: { pn: this.model.projectName}});
    } else {
      this.router.navigate([`/${playgroundType}`]);
    }
  }


  // function to check if the current page is login page
  isLoginPage(): boolean {
    return this.router.url.includes('/login');
  }

  // function to update the project id
  updateProjectId() {
    const parent = this;
    let urlsegment = (window.location.href).split('/')
    let index = urlsegment.indexOf('projects');
    if (index !== -1 && index + 1 < urlsegment.length) {
      parent.model.projectId = urlsegment[index + 1];
    }
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

  // function to update the project name
  private updateProjectName() {
    const parent = this;
    parent.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else {
        parent.model.projectName = '';
      }
    });
  }

  // function to logout the user
  logout() {
    const parent = this;
    const sessionData = parent.storageService.getData();
    sessionData.userId = ""
    this.storageService.setData(sessionData);

    parent.router.navigate(['/login'])
  }

}
