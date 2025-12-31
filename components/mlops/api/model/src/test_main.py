# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from fastapi.testclient import TestClient
from main import app
from mms.routing import model_router
 
client = TestClient(app)
 
def test_listmodel():
    
    response = client.get("/models", headers={"accept": "application/json", "userId":"testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "status": "Success",
        "data": response['data']
    }