/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class PipelineDetailsData {
    constructor(
        public projectId: string='',
        // public version: number=1,
        public description: string='',
        public pipeline: Pipeline=new Pipeline(),
    ) { }

}

export class Volume {
    constructor(
        public scope: string = "pipeline",
        public name: string  = "",
        public mountPath: string = "",
        public sizeinGB: number = 1
    ) {}
}

export class Pipeline {
    constructor(
        public name: string='',
        public version: number=1,
        public operator: string='',
        public runtime: string='',
        public dataStorage: DataStorage[]=[],
        public volume?: Volume,
        public flow: object={},
        public variables: object={},
        public globalVariables: object={}
    ) { }
}

export class DataStorage {
    constructor(
        public storageType: string='',
        public name: string='',
        public uri: string=''
    ) { }
}

