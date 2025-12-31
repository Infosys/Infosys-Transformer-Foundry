/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class FlowSectionData {
    constructor(
    type:           string,
    input:          Input,
    output:         Output,
    stepConfig:     StepConfig,
    resourceConfig: ResourceConfig,
    dependsOn:      string[]){}
}

export class Input {
    constructor(
    data_path:  string,
    request_id: string){}
}

export class Output {
    constructor(
    status: string){}
}

export class ResourceConfig {
    constructor(
    cpuLimit:     string,
    memoryLimit?: string,
    gpuLimit?:    string){}
}

export class StepConfig {
    constructor(
    entryPoint:    string[],
    stepArguments: string[],
    imageUri:      string){}
}
