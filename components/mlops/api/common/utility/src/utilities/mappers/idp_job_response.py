# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: idp_job_response.py
description: A Pydantic model object for Deployment entity model
             which maps the data model to the Deployment entity schema
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional,List

class ESBulkData(BaseModel):
    data: List[dict]
    esindex: str

class ResponseData(BaseModel):
    response: Optional[dict]
    responseCde: int
    responseMsg: str
    timestamp: str
    responseTimeInSecs: float
