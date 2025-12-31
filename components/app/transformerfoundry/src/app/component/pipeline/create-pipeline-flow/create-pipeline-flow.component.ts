/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Component, OnInit, Renderer2, EventEmitter, Output, Input } from "@angular/core";
import { PayloadData} from "../../../data/payload-data"
import { PipelineDetailsData } from "../../../data/pipeline-details-data"
import { FlowSectionData } from "../../../data/flow-section-data";
import { PipelineServiceService } from "../../../services/pipeline-service.service";
import { UtilityService } from "src/app/services/utility.service";

@Component({
  selector: "app-create-pipeline-flow",
  templateUrl: "./create-pipeline-flow.component.html",
  styleUrls: ["./create-pipeline-flow.component.scss"]
})

export class CreatePipelineFlowComponent implements OnInit {
  // node payload event emitter
  @Output() nodePayload = new EventEmitter<{}>();
  // flow payload event emitter
  @Output() flowData = new EventEmitter<{}>();
  // input payload data
  @Input() inputPayloadData: PayloadData;
  // height
  @Input() height: number;
  // read only flag
  @Input() isReadOnly: boolean;
  // input pipeline data
  @Input() pipelineDetailData: PipelineDetailsData;
  @Input() inputFlowData: FlowSectionData;
  @Input() inputPipelineData: PipelineDetailsData;

  // constructor
  constructor(
    private renderer: Renderer2,
    private pipelineService: PipelineServiceService,
    public utilservice: UtilityService) {
  }

  sampleJson = { "testTitle": "pipeline" };
  model = {
    nodeData: undefined,
    dataLoaded: false,
  }

  // on init method
  ngOnInit(): void {
    this.renderer.listen('window', 'onPipelineChange',
      (event: CustomEvent) => { this.handlePipelineChange(event) });
    this.renderer.listen('window', 'onFlowChange',
      (event: CustomEvent) => { this.handleNodePropChange(event) });
    console.log("payload", this.inputPayloadData);
  }

  // after view init method
  ngAfterViewInit() {
    const parent = this;
    parent.pipelineService.getNodeConfigData().then((data) => {
      const flowData = parent.pipelineDetailData?.pipeline?.flow || {}
      const transformFlowData = parent.utilservice.transformFlowData_Reverse(flowData);
      const pipelineData = {
        "pipelineVariables": parent.pipelineDetailData?.pipeline?.variables,
        "nodes": parent.inputPayloadData?.flowData?.nodes,
        "edges": parent.inputPayloadData?.flowData?.edges,
        "sequence": parent.inputPayloadData?.flowData?.sequence,
        "flowdata": transformFlowData
      };
      console.log("pipelineData123", pipelineData)
      window.dispatchEvent(new CustomEvent('receiveDataFromParent', {
        detail: {
          nodeData: data,
          pipeline: pipelineData,
          isReadOnlyMode: parent.isReadOnly,
        }
      }));
    })
  }

  // handle pipeline change 
  handlePipelineChange(event: CustomEvent<any>) {
    const parent = this;
    const receivedPipelineData = event.detail;
    const edges = receivedPipelineData.edges;
    const nodes = receivedPipelineData.nodes;
    const sequence = receivedPipelineData.sequence;
    const flowData = { nodes: nodes, edges: edges, sequence: sequence }
    console.log("testconsole", receivedPipelineData);
    parent.nodePayload.emit({ flowData: flowData });
  }

  // handle node prop change
  handleNodePropChange(event: CustomEvent<any>) {
    const parent = this;
    const transformFlowData = parent.utilservice.transformFlowData(event.detail)
    console.log("handleNodePropChange", transformFlowData);

    parent.flowData.emit(transformFlowData);
  }
}
