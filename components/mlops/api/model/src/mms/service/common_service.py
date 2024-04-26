# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#


from typing import List
import datetime
from bson.objectid import ObjectId
from mms.constants.local_constants import *
from mms.exception.exception import ModelAPINotFoundError
from aicloudlibs.exceptions.global_exception import *

class ModelsBaseService:

    def __init__(self, app, customlog, userId=None):
        self.log = app.logger
        self.app = app
        self.customlog = customlog
        self.loggedUser = userId


class CommonService(ModelsBaseService):
    
    #This method will return the project details for the given project id
    def getProjectDetails(self, projectId: str) :
        self.customlog.debug('START getProjectDetails')
        projectColl = self.app.database['project']
        if projectId is not None:
            try:
                projectObj = projectColl.find_one({"id": projectId, "isDeleted": False})
            except:
                raise NotFoundException('1002',errorCodeMsgDict['1002'])
        self.customlog.debug('END getProjectDetails')
        return projectObj
    
    #This method will check for the given project id exist or not
    def checkIfProjectExists(self, projectId:str) -> bool:
        self.customlog.debug('START checkIfProjectExists')
        isProjectPresent = False
        projectObj = self.getProjectDetails(projectId)
        if projectObj is not None:
            isProjectPresent = True
        self.customlog.debug('END checkIfProjectExists==%s', isProjectPresent)
        return isProjectPresent
