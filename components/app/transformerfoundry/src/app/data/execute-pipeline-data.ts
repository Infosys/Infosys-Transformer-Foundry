/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class ExecutePipelineData {
    constructor(
    pipeline: Pipeline){}
}

export class Pipeline {
    constructor(
    dataStorage:     DataStorage[],
    variables:       object,
    globalVariables: object){}
}

export class DataStorage {
    constructor(
    storageType: string,
    name:        string,
    uri:         string){}
}

