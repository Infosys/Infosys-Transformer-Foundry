/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from '@angular/core';
import { ProjectServiceService } from './project-service.service';
import { DataStorageService } from './data-storage.service';

@Injectable()
export class UtilityService {

  constructor(
    private project: ProjectServiceService,
    private storageService: DataStorageService
  ) { }

  isListHasValue(objectList: any): boolean {
    return objectList !== undefined && objectList !== null && objectList.length > 0;
  }

  isStringHasValue(str: string): boolean {
    return str !== undefined && str !== null && str.trim().length > 0;
  }
  isAValidValue(obj) {
    return obj !== null && obj !== undefined;
  }

  getIfDuplicatesExist(values) {
    return this.isListHasValue(values) && this.isListHasValue(values.filter((val, i) => values.indexOf(val) !== i));
  }

  testJSON(item: any): boolean {
    let isJson = false;
    try {
      if (item && typeof item === 'string' && typeof JSON.parse(item) === 'object') {
        isJson = true;
      }
    } catch (error) { }
    return isJson;
  }

  //this function changes the flow array right before sending in API request.
  // this structure is expected by the API -
  transformFlowData(flowFromEditor) {

    const flow_Keys = Object.keys(flowFromEditor)
    const transformedFlow = flow_Keys.reduce((acc, key) => {
      const oldObj = flowFromEditor[key]
      console.log("transformFlowData1", { [key]: oldObj })
      if (key !== "undefined") {
        const newObj = {
          type: oldObj.type,
          dependsOn: oldObj.dependsOn,
          input: removeStepConfigFromObject(oldObj.stepConfig.input),
          output: removeStepConfigFromObject(oldObj.stepConfig.output),
          stepConfig: {
            entryPoint: oldObj.stepConfig.entryPoint,
            stepArguments: oldObj.stepConfig.stepArguments,
            imageUri: oldObj.imageUri,
          },
          resourceConfig: oldObj.resourceConfig,
        };
        if (newObj.resourceConfig && newObj.resourceConfig.computes) {
          newObj.resourceConfig.computes.forEach((compute: any) => {
            if (typeof compute.memory === 'number')
              compute.memory = compute.memory + 'GB';
          });
        }
        return { ...acc, [key]: newObj };
      } else return acc;
    }, {});

    function removeStepConfigFromObject(Obj: any): any {
      if (!Obj) {
        return {};
      }
      const newInput = Object.keys(Obj).reduce((acc, key) => {
        acc[key] = Obj[key].replace('stepConfig.', '');
        return acc;
      }, {});
      // console.log(newInput);
      return newInput;
    }

    console.log("transformFlowData", transformedFlow);

    return transformedFlow;
  }

  //this function changes flow data from API to be compactible with the RJSF form structure.
  transformFlowData_Reverse(flowFromAPI) {
    const flow_Keys = Object.keys(flowFromAPI)
    const transformedFlow = flow_Keys.reduce((acc, key) => {
      const newObj = flowFromAPI[key];
      const oldObj = {
        type: newObj.type,
        dependsOn: newObj.dependsOn,
        imageUri: newObj.stepConfig.imageUri,
        stepConfig: {
          input: newObj.input,
          output: newObj.output,
          entryPoint: newObj.stepConfig.entryPoint,
          stepArguments: newObj.stepConfig.stepArguments,
        },
        resourceConfig: newObj.resourceConfig,
      };
      if (oldObj.resourceConfig && oldObj.resourceConfig.computes) {
        oldObj.resourceConfig.computes.forEach((compute: any) => {
          if (typeof compute.memory === 'string')
            compute.memory = parseInt(compute.memory.replace(/[^\d.]/g, ''));
        });
      }
      return { ...acc, [key]: oldObj };
    }, {});
    console.log("transformFlowData_Reverse", transformedFlow);

    return transformedFlow
  }

  // this function is used to check if the user has permission to perform the action.
  isPermissionAllowed(permission, projectId) {
    const parent = this;
    const currentUserId = parent.storageService.getData().userId;
    var retVal = false;
    console.log("isPermissionAllowed", projectId, currentUserId)
    return new Promise(function (fulfilled, rejected) {
      parent.project.getProjectDetailsByID(projectId).then((values) => {
        console.log("isPermissionAllowed, if,", values, values['createdBy'], currentUserId, values['createdBy'] === currentUserId)
        if (values['createdBy'] === currentUserId) {
          console.log("createdBy", values['createdBy'])
          fulfilled(true);
        }
        else {
          const projectData = values['userLists'].filter(user => user.userEmail === currentUserId);
          if (projectData[0]['permissions']['workspaceAdmin']) {
            fulfilled(true);
          }
          if (projectData.length > 0) {
            console.log(projectData[0]['permissions'][permission])
            fulfilled(projectData[0]['permissions'][permission]);
          }
        }
      }).catch(() => {
        rejected()
      })
    })
  }

  // this function is used to get the error message from the error object.
  getErrorMessage(error) {
    var message = '';
    if (error.error.details && error.error.details[0])
      message = error.error.details[0].message;
    else if (error.error.detail)
      message = error.error.detail.message;
    else
      message = error.error.message;
    return message;
  }

}
