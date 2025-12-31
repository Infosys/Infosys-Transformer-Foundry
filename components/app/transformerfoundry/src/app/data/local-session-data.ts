/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class LocalSessionData {
    constructor(
        public userId?: string,
        public pipelineTabIndex?:number,
        public jobTabIndex?:number,
        public deployModelTabIndex?:number,
        public modelZooTabIndex?:number,
    ) { }
}
