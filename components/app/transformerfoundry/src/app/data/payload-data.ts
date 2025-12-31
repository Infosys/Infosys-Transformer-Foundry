/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class PayloadData {
    constructor(
    public flowData:     FlowData= new FlowData(),
    public pipelineData: PipelineData = new PipelineData(),
    public pipelineId?:   string,
    public projectId?:    string){
    }
}
export class FlowData {
    constructor(
        public nodes:string[]=[],
        public edges:string[]=[],
        public sequence:object={}
    ){}
}
export class PipelineData {
    constructor(
        public variables={},
        public globalVariables={}
    ){}
}