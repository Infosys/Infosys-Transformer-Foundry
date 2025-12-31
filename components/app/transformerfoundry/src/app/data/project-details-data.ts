/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export class ProjectDetailsData {
    constructor(
        public tenantId: string,
        public name: string = '',
        public description: string = '',
        public userLists: UserList[] = [new UserList()]) { }
}

export class UserList {
    constructor(
        public userEmail: string = '',
        public permissions: Permissions = new Permissions()) { }
}

export class Permissions {
    constructor(
        public createPipeline: boolean = false,
        public executePipeline: boolean = false,
        public deployModel: boolean = false,
        public uploadDataset: boolean = false,
        public view: boolean = true,
        public workspaceAdmin: boolean = false) { }
}
