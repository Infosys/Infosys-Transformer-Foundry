/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class BenchmarkData {
  constructor(
  public projectId:      string = '',
  public name:           string = '',
  public description:    string = '',
  public type:           string = 'code',
  public configuration:  Configuration = new Configuration(),
  public resourceConfig: ResourceConfig = new ResourceConfig()){}
}

export class ResourceConfig {
  constructor(
  public gpuQty:    number = 1,
  public gpuMemory: string = '80GB',
  public volume:    Volume = new Volume()){}
}

export class Volume {
  constructor(
  public name:      string='',
  public mountPath: string = '',
  public sizeinGB: number = 1){}
}

export class Configuration {
  constructor(
  public model:       Model[] = [new Model()],
  public data:        Data[] = [new Data()],
  public task:        string = '',
  public dataStorage: DataStorage = new DataStorage){}
}

export class Data {
  constructor(
  public name:      string = '',
  public scope:     string = '',
  public language:  string = '',
  public batchSize: number = 1,
  public limit:     number = 1){}
}

export class DataStorage {
  constructor(
  public storageType: string = '',
  public uri:         string = ''){}
}

export class Model {
  constructor(
  public modelName:      string = '',
  public modelPathorId:  string = '',
  public datatype:       string = '',
  public quantizeMethod: string = 'NA',
  public args:           Arg[] = [new Arg()]){}
}

export class Arg {
  constructor(
  public name:  string = '',
  public value: string = ''){}
}
