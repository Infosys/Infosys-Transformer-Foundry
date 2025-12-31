
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { Component, Input, OnInit } from "@angular/core";

@Component({
  selector: "chat-message",
  templateUrl: "./message-content.component.html",
  styleUrls: ["./message-content.component.scss"],
})
export class ChatMessageComponent implements OnInit {
  @Input() messageData: any;
  @Input() selectedState: boolean = false;

  constructor() {}

  ngOnInit(): void {}
}
