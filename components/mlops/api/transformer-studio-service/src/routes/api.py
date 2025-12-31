# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from fastapi import APIRouter
from endpoints import pipeline_formdata, user_controller, template_controller


router = APIRouter()
router.include_router(pipeline_formdata.router)
router.include_router(user_controller.router)
router.include_router(template_controller.router)
