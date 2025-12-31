/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class JobDetailsData {
    constructor(
        public createdBy: string='',
        public createdOn: string='',
        public isDeleted: boolean=false,
        public updatedBy: string='',
        public modifiedOn: string='',
        public projectId: string='',
        public version: number=1,
        public name: string='',
        public originalName: string='',
        public description: string='',
        public scope: string='',
        public jobArguments: JobArgument[] = [],
        public steps: Step[] = [new Step()],
        public id: string='',
        public status: string='',
    ) { }
}

export class JobArgument {
    constructor(
        public name: string = '',
        public defaultVal: string = '',
        public dataType: string = '',
    ) { }
}

export class Step {
    constructor(
        public trainingStep: TrainingStep = new TrainingStep(),
    ) { }
}

export class TrainingStep {
    constructor(
        public name: string = '',
        public inputArtifacts: Artifacts = new Artifacts(),
        public stepArguments: StepArguments = new StepArguments(),
        public container: Container = new Container(),
        public framework: Framework = new Framework,
        public preTrainedModelDetails: PreTrainedModelDetails = new PreTrainedModelDetails(),
        public outputArtifactBaseUri: string = '',
        public metricDetails: MetricDetails = new MetricDetails(),
    ) { }
}

export class Container {
    constructor(
        public imageUri: string = '',
        public envVariables: EnvVariables[] = [],
        public ports: Ports[] = [],
        public labels: Labels[] = [],
        public command: string[] = [],
        public args: string[] = [],
    ) { }
}

export class EnvVariables {
    constructor(
        public name: string = '',
        public value: string = '',
    ) { }
}

export class Ports {
    constructor(
        public name: string='',
        public value: string='',
    ) { }
}

export class Labels {
    constructor(
        public name: string='',
        public value: string='',
    ) { }
}

export class Framework {
    constructor(
        public name: string = '',
        public version: string = '',
    ) { }
}

export class Artifacts {
    constructor(
        public storageType: string = '',
        public uri: string = '',
    ) { }
}

export class MetricDetails {
    constructor(
        public goal: string = '',
        public name: string = '',
        public regex: string = '',
        public logFileUri: string = '',
    ) { }
}

export class PreTrainedModelDetails {
    constructor(
        public name: string = '',
        public version: string = '',
        public artifacts: Artifacts = new Artifacts(),
    ) { }
}

export class StepArguments {
    constructor(
        public jobArgNames: string[] = [],
    ) { }
}
