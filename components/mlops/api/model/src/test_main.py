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