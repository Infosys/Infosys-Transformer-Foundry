/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class LeaderFilterData {
  constructor(  
    public toDate?:         string,
    public fromDate?:       string,
    public metricName?:     string,
    public isSortingClicked?: Boolean,
    public modelName?:      string,
    public datasetName?:    string,
    public benchmarkName?: string,
  ){}
}

