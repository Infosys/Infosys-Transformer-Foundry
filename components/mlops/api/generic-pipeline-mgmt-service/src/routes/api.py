# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from fastapi import APIRouter
from endpoints import pipeline_definition
from endpoints import pipeline_execution
from endpoints import pipeline_operator

router = APIRouter()
router.include_router(pipeline_definition.router)
router.include_router(pipeline_execution.router)
router.include_router(pipeline_operator.router)