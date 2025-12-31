/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class Dataset {
  constructor(
    datasetName: string,
    scope: string,
    size: number,
    task: string,
    modality: string,
    language: string,
    tags: Array<string[]>,
    storage: any[],
    license: string = "",
    purpose: string = "",
    usecase: string = "",
    format: string = "",
    limitation: string = "",
    dataStorage: DataStorage
  ) {}
}

export class DataStorage {
  constructor(storageType: string, uri: string) {}
}
