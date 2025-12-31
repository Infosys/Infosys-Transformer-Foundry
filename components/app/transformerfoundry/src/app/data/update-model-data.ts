/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class UpdateModelData{
    constructor(
        public name:        string = '',
        public version:     number = 1,
        public description: string = '',
        public projectId:   string = '',
        public container:   Container = new Container(),
        public artifacts:   Artifacts = new Artifacts(),
        public metadata:    Metadata = new Metadata()
    ) { }
}

export class Artifacts {
    constructor(
  public storageType: string = '',
  public uri:         string = ''){}
}

export class Container {
    constructor(
  public imageUri:       string = '',
  public envVariables:   EnvVariable[] = [new EnvVariable()],
  public ports:          EnvVariable[] = [new EnvVariable()],
  public labels:         EnvVariable[] = [new EnvVariable()],
  public command:        string[] = [''],
  public args:           string[] = [''],
  public healthProbeUri: string = ''){}
}

export class EnvVariable {
    constructor(
  public name:  string = '',
  public value: string = ''){}
}

export class Metadata {
    constructor(
        public modelDetails:         ModelDetails = new ModelDetails(),
        public modelParameters:      ModelParameters = new ModelParameters(),
        public quantitativeAnalysis: QuantitativeAnalysis = new QuantitativeAnalysis(),
        public considerations:       Considerations = new Considerations()
    ) { }
}

export class Considerations {
    constructor(
  public users:                       Limitation[] = [new Limitation()],
  public useCases:                    Limitation[] = [new Limitation()],
  public limitations:                 Limitation[] = [new Limitation()],
  public tradeoffs:                   Limitation[] = [new Limitation()],
  public ethicalConsiderations:       EthicalConsideration[] = [new EthicalConsideration()],
  public environmentalConsiderations: EnvironmentalConsideration[] = [new EnvironmentalConsideration()]){}
}

export class EnvironmentalConsideration {
    constructor(
  public hardwareType:  string = '',
  public hoursUsed:     string = '',
  public cloudProvider: string = '',
  public computeRegion: string = '',
  public carbonEmitted: string = ''){}
}

export class EthicalConsideration {
    constructor(
  public name:               string = '',
  public mitigationStrategy: string = ''){}
}

export class Limitation {
    constructor(
  public description: string = ''){}
}

export class ModelDetails {
    constructor(
        public displayName:    string = '',
        public tasktype:       string = '',
        public customTags:     CustomTag[] = [new CustomTag()],
        public overview:       string = '',
        public documentation:  string = '',
        public owners:         Owner[] = [new Owner()],
        public versionHistory: VersionHistory[] = [new VersionHistory()],
        public licenses:       License[] = [new License()],
        public references:     Reference[] = [new Reference()],
        public citations:      Citation[] = [new Citation()],
        public path:           string = ''
    ) { }
}

export class Citation {
    constructor(
  public style:    string = '',
  public citation: string = ''){}
}

export class CustomTag {
    constructor(
  public tags: string = ''){}
}

export class License {
    constructor(
  public identifier: string = '',
  public customText: string = ''){}
}

export class Owner {
    constructor(
  public name:    string = '',
  public contact: string = ''){}
}

export class Reference {
    constructor(
  public reference: string = ''){}
}

export class VersionHistory {
    constructor(
      public name: string = '',
      public date: string = '',
      public diff: string = ''
    ) { }
}

export class ModelParameters {
    constructor(
      public modelArchitecture: string = '',
      public data:              Datum[] = [new Datum()],
      public inputFormat:       string = '',
      public inputFormatMap:    FormatMap[] = [new FormatMap()],
      public outputFormat:      string = '',
      public outputFormatMap:   FormatMap[] = [new FormatMap()]
    ) { }
}

export class Datum {
    constructor(
      public name:           string = '',
      public link:           string = '',
      public sensitive:      Sensitive[] = [new Sensitive()],
      public classification: string = ''
    ) { }
}

export class Sensitive {
    constructor(
      public Fields: string[] = ['']
    ) { }
}

export class FormatMap {
    constructor(
      public key:   string = '',
      public value: string = ''
    ) { }
}

export class QuantitativeAnalysis {
    constructor(
      public performanceMetrics: PerformanceMetric[] = [new PerformanceMetric()]
    ) { }
}

export class PerformanceMetric {
    constructor(
      public type:               string = '',
      public value:              string = '',
      public slice:              string = '',
      public confidenceInterval: ConfidenceInterval = new ConfidenceInterval()
    ) { }
}

export class ConfidenceInterval {
    constructor(
      public lowerBound: string = '',
      public upperBound: string = ''
    ) { }
}
