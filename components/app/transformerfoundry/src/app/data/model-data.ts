/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class ModelData {
    constructor(
    createdBy:    string,
    createdOn:    string,
    isDeleted:    boolean,
    updatedBy:    string,
    modifiedOn:   string,
    name:         string,
    version:      number,
    description:  string,
    projectId:    string,
    pipl_tmpl_id: string,
    container:    Container = new Container(),
    artifacts:    Artifacts = new Artifacts(),
    metadata:     Metadata = new Metadata(),
    id:           string,
    status:       string,
    ){}
}

export class Artifacts {
    constructor(
    storageType: string='',
    uri:         string='',
    ){}
}

export class Container {
    constructor(
    imageUri:       string='',
    envVariables:   EnvVariable[]=[],
    ports:          Ports[]=[],
    labels:         Labels[]=[],
    command:        string='' ,
    args:           string='',
    healthProbeUri: string='',
    ){}
}

export class EnvVariable {
    constructor(
        name:  string='',
        value: string='',
    ){}
}

export class Ports {
    constructor(
        name:  string='',
        value: string='',
    ){}
}
export class Labels {
    constructor(
        name:  string='',
        value: string='',
    ){}
}

export class Metadata {
    constructor(
    modelDetails:         ModelDetails= new ModelDetails(),
    modelParameters:      ModelParameters= new ModelParameters,
    quantitativeAnalysis: QuantitativeAnalysis= new QuantitativeAnalysis,
    considerations:       Considerations = new Considerations,
    ){}
}

export class Considerations {
    constructor(
    users:                       Users[]=[],
    useCases:                    UseCases[]=[],
    limitations:                 Limitation[]=[],
    tradeoffs:                   Tradeoffs[]=[],
    ethicalConsiderations:       EthicalConsideration[]=[],
    environmentalConsiderations: EnvironmentalConsideration[]=[],
    ){}  
}

export class Users {
    constructor(
    description: string='',
    ){}
}
export class UseCases {
    constructor(
    description: string='',
    ){}
}
export class Tradeoffs {
    constructor(
    description: string='',
    ){}
}

export class EnvironmentalConsideration {
    constructor(
    hardwareType:  string='',
    hoursUsed:     string='',
    cloudProvider: string='',
    computeRegion: string='',
    carbonEmitted: string='',
    ){}
}

export class EthicalConsideration {
    constructor(
    name:               string='',
    mitigationStrategy: string='',
    ){}
}

export class Limitation {
    constructor(
    description: string='',
    ){}
}

export class ModelDetails {
    constructor(
    displayName:    string='',
    overview:       string='',
    tasktype:       string='',
    customTags:     CustomTag[]=[],
    documentation:  string='',
    owners:         Owner[]=[],
    versionHistory: VersionHistory[]=[],
    licenses:       License[]=[],
    references:     Reference[]=[],
    citations:      Citation[]=[],
    path:           string='',
    ){}
}

export class Citation {
    constructor(
    style:    string='',
    citation: string='',
    ){}
}

export class CustomTag {
    constructor(
    tags: string='',
    ){}
}

export class License {
    constructor(
    identifier: string='',
    customText: string='',
    ){}
}

export class Owner {
    constructor(
    name:    string='',
    contact: string,
    ){}
}

export class Reference {
    constructor(
    reference: string='',
    ){}
}

export class VersionHistory {
    constructor(
    name: string='',
    date: string='',
    diff: string='',
    ){}
}

export class ModelParameters {
    constructor(
    modelArchitecture: string='',
    data:              Data[]=[],
    inputFormat:       string='',
    inputFormatMap:    InputPutFormatMap[]=[],
    outputFormat:      string='',
    outputFormatMap:   OutputPutFormatMap[]=[],
    ){}
}

export class Data {
    constructor(
    name:           string='',
    link:           string='',
    sensitive:      Sensitive[]=[],
    classification: string='',
    ){}
}

export class Sensitive {
    constructor(
    Fields: string[]=[],
    ){}
}

export class InputPutFormatMap {
    constructor(
    key:   string='',
    value: string='',
    ){}
}

export class OutputPutFormatMap {
    constructor(
    key:   string='',
    value: string='',
    ){}
}

export class QuantitativeAnalysis {
    constructor(
    performanceMetrics: PerformanceMetric[]=[],
    ){}
}

export class PerformanceMetric {
    constructor(
    type:               string='',
    value:              string='',
    slice:              string='',
    confidenceInterval: ConfidenceInterval= new ConfidenceInterval(),
    ){}
}

export class ConfidenceInterval {
    constructor(
    lowerBound: string='',
    upperBound: string='',
    ){}
}
