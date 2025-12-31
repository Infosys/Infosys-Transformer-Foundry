# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from pydantic import BaseModel, Field,ValidationError
from datetime import datetime
from typing import Optional
from abc import ABC,abstractmethod
from fastapi.responses import JSONResponse
from aicloudlibs.constants.error_constants import ErrorCode,SUCCESS_CODE,SUCCESS_STATUS_MESSAGE,FAILURE_STATUS_MESSAGE
from pydantic.errors import PydanticValueError
from aicloudlibs.db_management.core.db_utils import *
import pydantic
from pymongo import database
from bson import ObjectId

class APIDBUtils(object):
      @classmethod
      def findOneById(cls,entityName,id):
        mongodb_client=connect_mongodb()
        db=get_db(mongodb_client)
        projectObj=db[entityName].find_one({"id": id,"isDeleted": pydantic.parse_obj_as(bool, "false")})
        close_db_conn(mongodb_client)
        return projectObj 
      
      @classmethod
      def updateEntity(cls,entityName,filter,newValues):
        mongodb_client=connect_mongodb()
        db=get_db(mongodb_client)
        Obj=db[entityName].update_one(filter,newValues)
        close_db_conn(mongodb_client)
        return Obj