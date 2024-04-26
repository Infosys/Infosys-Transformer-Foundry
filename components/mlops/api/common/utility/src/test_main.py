from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# GET Method to call search api in elastic search associated with modelity
def test_search_elasticsearch():
    response = client.get("/utilities/elastic/code/search", headers={"accept": "application/json"})
    print("*********")
    print(response)
    assert response.status_code == 200
    assert response.json() == {}