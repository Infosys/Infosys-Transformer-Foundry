/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class ExecuteTrailData {
    constructor(
    public projectId:        string,
    public pipelineId:       string,
    public name:             string='',
    public description:      string='',
    public modelName:        string='',
    public modelVersion:     string='',
    public runArguments:     RunArgument[]=[],
    public resourceConfig:   ResourceConfig = new ResourceConfig(),
    public experimentConfig: ExperimentConfig = new ExperimentConfig()){}
}

export class ExperimentConfig {
    constructor(
        public name: string=''){}
}

export class ResourceConfig {
    constructor(
        public computes:       Compute[] = [],
        public volumeSizeinGB: number=0.1){}
}

export class Compute {
    constructor(
        public type:   string='CPU',
        public maxQty: number=5,
        public memory: string='1GB',
        public minQty: number=1){}
}

export class RunArgument {
    constructor(
        public name:     string = '',
        public argValue: number | string = ''){}
}
