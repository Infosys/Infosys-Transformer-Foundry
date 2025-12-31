#  ================================================================================================================# 
# # ===============================================================================================================# 
# # Copyright 2024 Infosys Ltd.                                                                                    # 
# # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# # http://www.apache.org/licenses/                                                                                # 
#  ================================================================================================================# 

from flask import Response, jsonify

def create_response_message(message: str, status_code: int) -> Response:
    response = jsonify({'status': message})
    response.status_code = status_code
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response