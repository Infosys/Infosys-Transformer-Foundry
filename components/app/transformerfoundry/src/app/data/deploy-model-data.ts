/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class DeployedModelData {
  constructor(  
    public endpointId:      string='',
    public modelId:         string='',
    public version:         number = 1,
    public inferenceConfig: InferenceConfig = new InferenceConfig(),
  ){}
}

export class InferenceConfig {
  constructor(
    public servingFramework: string='Custom',
    public inferenceSpec:    InferenceSpec = new InferenceSpec(),
    public servingSpec:      ServingSpec = new ServingSpec()
  ){}
}

export class InferenceSpec {
  constructor(
    public minReplicaCount:         number = 1,
    public maxReplicaCount:         number = 1,
    public containerResourceConfig: ContainerResourceConfig = new ContainerResourceConfig(),
    public modelSpec: ModelSpec[] = [new ModelSpec()],
  ){}
}

export class ContainerResourceConfig {
  constructor(
    public computes:       Compute[] = [new Compute()],
    public volumeSizeinGB: number = 1,
  ){}
}

export class Compute {
  constructor(
    public type:   string ='GPU',
    public memory: string ='20GB',
    public maxQty: number = 1,
    public minQty: number = 1,
  ){}
}

export class ModelSpec {
  constructor(
    public modelUris:   ModelUris = new ModelUris(),
    public tritonServingConfig: TritonServingConfig = new TritonServingConfig()
  ){}
}

export class ModelUris {
  constructor(
    public prefixUri: string ='',
    public predictUri: string ='',
    public explainUri: string = '',
    public feedbackUri: string = ''
  ){}
}

export class TritonServingConfig {
  constructor(
    public dependencyFileRepo: DependencyFileRepo = new DependencyFileRepo()
  ){}
}

export class DependencyFileRepo {
  constructor(
    public storageType: string ='',
    public uri: string =''
  ){}
}

export class ServingSpec {
  constructor(
    public tritonSpec: TritonSpec = new TritonSpec()
  ){}
}

export class TritonSpec {
  constructor(
    public logLevel: string = ''
  ){}
}
