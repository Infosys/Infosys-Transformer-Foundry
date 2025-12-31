/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class PipelineData {
  pipeline: {
    name: string;
    version: string;
  };
  description: string;
  createdOn: string;
  status: string;
    constructor(
    
    pipeline_id: string,
    version:     number,
    description: string,
    createdDtm:  string,
    status:      string){}
}