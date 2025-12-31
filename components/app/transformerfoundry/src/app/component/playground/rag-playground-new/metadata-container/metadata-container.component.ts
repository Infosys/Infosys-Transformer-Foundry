
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import { Component, Input, OnInit } from "@angular/core";
import { ChatMessage, MessageMetadata } from "src/app/data/rag-playground-data";

@Component({
  selector: "message-metadata-container",
  templateUrl: "./metadata-container.component.html",
  styleUrls: ["./metadata-container.component.scss"],
})
export class MetadataContainerComponent implements OnInit {
  @Input() messageData: ChatMessage = new ChatMessage();
  @Input() messageMetadata: MessageMetadata[] = [];

  constructor() {}

  model = {
    messageDataArray: [] as MessageMetadata[],
  };

  carouselOptions = {
    nav: true,
    dots: false,
    items: 1,
    navText: ["<", ">"],
  };

  ngOnInit(): void {
    console.log("In metadata container Metadata", this.messageMetadata);
    this.model.messageDataArray = this.messageMetadata;
  }

  ngOnChanges(): void {
    console.log("In metadata container onchange", this.messageMetadata);
    console.log(
      "In metadata container Metadata array",
      this.model.messageDataArray
    );
  }
}
