# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from common.app_config_manager import AppConfigManager
app_config = AppConfigManager().get_app_config()
security = HTTPBasic()


def basic_authorize(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username_bytes = app_config['AUTHENTICATION']['username'].encode(
        'utf-8')
    correct_password_bytes = app_config['AUTHENTICATION']['password'].encode(
        'utf-8')
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
