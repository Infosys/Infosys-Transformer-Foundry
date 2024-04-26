# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#


from typing import List
import datetime
import random
from dotenv import dotenv_values
from bson.objectid import ObjectId
from mms.constants.local_constants import *
from mms.exception.exception import *
from mms.config.logger import CustomLogger
from mms.service.common_service import ModelsBaseService, CommonService
#from aicloudlibs.schemas.model_mappers import *
from aicloudlibs.exceptions.global_exception import *
from aicloudlibs.validations.global_validations import GlobalValidations
from aicloudlibs.constants.util_constants import *

class ModelService(ModelsBaseService):

    def __init__(self, app, customlog, userId=None):
        self.commonService = CommonService(app, customlog, userId)
        self.modelColl = app.database['model']
        ModelsBaseService.__init__(self, app, customlog, userId)

    #This method will return the list of models associated with the projectID.
    def getAllModels(self, projectId):
        print("inside getAllModels")
        
        modelColl = self.app.database["model"]
        isProjectPresent = self.commonService.checkIfProjectExists(projectId)
        if isProjectPresent == False:
            raise NotFoundException('1002',errorCodeMsgDict['1002'])            
        hasUserAccess: bool = GlobalValidations.hasAccess(self.loggedUser, projectId, VIEW)
        if hasUserAccess == True :
            modelList = list(modelColl.find({'projectId': projectId, 'isDeleted': False},{"_id" : 0}))
            modelList_sorted=sorted(modelList, key=lambda i: (i['createdOn']), reverse=True) 
        else :
            raise ForbiddenException()
        return modelList_sorted    

    