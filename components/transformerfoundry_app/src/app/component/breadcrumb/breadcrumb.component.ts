/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2024 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Injectable } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd, UrlSegment } from "@angular/router";
import { filter } from 'rxjs/operators'

@Component({
  selector: 'app-breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrls: ['./breadcrumb.component.scss']
})
export class BreadcrumbComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) { }

  model: any = {
    breadcrumbItems: [],
    projectName: '',
  };

  //ngOnInit method used to get the url segments and extract the breadcrumb
  ngOnInit(): void {
    const parent = this;
    parent.router.events.pipe(filter(event => event instanceof NavigationEnd)).subscribe(() => {
      const urlsegments = parent.getUrlSegments();
      parent.extractBreadcrumb(urlsegments);
    });
  }

  //updateProjectName method used to update the project name from the query params
  updateProjectName() {
    const parent = this;
    this.route.queryParamMap.subscribe(queryParams => {
      if (queryParams.has('pn')) {
        parent.model.projectName = queryParams.get('pn');
      }
      else {
        parent.model.projectName = '';
      }
    });
  }

  //getUrlSegments method used to get the url segments
  getUrlSegments(): (UrlSegment[]) {
    return this.router.parseUrl(this.router.url).root.children.primary.segments;
  }

  //extractBreadcrumb method used to extract the breadcrumb from the url segments
  extractBreadcrumb(urlSegments: UrlSegment[]): void {
    const parent = this;
    parent.model.breadcrumbItems = [];
    var index = urlSegments.findIndex(segment => segment.path === 'login');
    if (index !== -1) {
      urlSegments.splice(urlSegments.length - 1, 1);
    }
    if (urlSegments && urlSegments.length > 0) {
      index = urlSegments.findIndex(segment => segment.path === '#');
      if (index >= -1) {
        for (let i = index + 1; i < urlSegments.length; i++) {
          var currentSegment = urlSegments[i]?.path;
          currentSegment = currentSegment.charAt(0).toUpperCase() + currentSegment.slice(1);
          if (i === urlSegments.length - 1 || (!currentSegment || !(/^[0-9a-zA-Z]{24}$/.test(currentSegment) || /^[0-9a-zA-Z]{32}$/.test(currentSegment)))) {
            const breadcrumbItem = {
              path: currentSegment,
              routerLink: i !== urlSegments.length - 1 ? `/${urlSegments.slice(0, i + 1).map(segment => segment.path).join('/')}` : ''
            };
            if (breadcrumbItem.path && breadcrumbItem.path !== '') {
              parent.model.breadcrumbItems.push(breadcrumbItem);
            }
          }
        }
      }
    }
    console.log(parent.model.breadcrumbItems);
    parent.updateProjectName();
  }
}
