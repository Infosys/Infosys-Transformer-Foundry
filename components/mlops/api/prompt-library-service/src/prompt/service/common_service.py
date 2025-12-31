# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from typing import List
import datetime
from bson.objectid import ObjectId
from aicloudlibs.exceptions.global_exception import *
from prompt.constants.local_constants import ErrorMessageCode

class ModelsBaseService:
    def __init__(self, app, customlog, userId=None):
        self.log = app.logger
        self.app = app
        self.customlog = customlog
        self.loggedUser = userId

class CommonService(ModelsBaseService):
    
    def __init__(self, app, customlog, userId=None):
        ModelsBaseService.__init__(self, app, customlog, userId)

    """ Get the project details from the database """
    def getProjectDetails(self, projectId: str) :

        self.customlog.debug('START getProjectDetails')
        projectColl = self.app.database['project']
        if projectId is not None:
            try:
                projectObj = projectColl.find_one({"id": projectId, "isDeleted": False})
            except:
                error_detail=ErrorMessageCode.PROJECT_NOT_FOUND_ERROR
                raise NotFoundException(error_detail.value.code, error_detail.value.message)
        self.customlog.debug('END getProjectDetails')
        
        return projectObj