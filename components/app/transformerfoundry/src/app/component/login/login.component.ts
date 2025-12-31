/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import {
  Component,
  ElementRef,
  HostListener,
  OnInit,
  ViewChild,
} from "@angular/core";
import { DataStorageService } from "src/app/services/data-storage.service";
import { ActivatedRoute, Router } from "@angular/router";
import { FormControl, NgModel, Validators } from "@angular/forms";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.scss"],
})
export class LoginComponent implements OnInit {
  @ViewChild("loginBtnRef") loginBtnRef: ElementRef;
  @ViewChild("loginRef") loginRef: ElementRef;

  emailFormControl = new FormControl("", [
    Validators.required,
    Validators.pattern("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
  ]);

  constructor(
    private storageService: DataStorageService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  model: any = {
    loginId: "",
    returnURL: "",
  };

  //function to handle login btn click
  handleLogin = () => {
    const parent = this;
    // initialize the value of uId in sesStorage
    const sessionData = parent.storageService.getData();
    sessionData.userId = parent.model.loginId;
    this.storageService.setData(sessionData);
    // console.log("local storage", parent.storageService.getData());

    // navigate on login success to the source screen
    this.router.navigate([this.model.returnURL]);
  };

  ngOnInit() {
    this.model.returnURL = this.route.snapshot.queryParams["returnUrl"] || "";
  }

  validateLogin(loginRef: NgModel) {
    this.model.loginId = this.model.loginId.toLowerCase();
    console.log("loginRef", loginRef);
  }

  focusLoginButton() {
    this.loginBtnRef.nativeElement.focus();
  }
}
