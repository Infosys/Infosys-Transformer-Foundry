from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Method to test getBenchmarkStatus with 200 response
def test_getBenchmarkStatus():
    response = client.get("/benchmarks/464645645", headers={"accept": "application/json", "userId":"testuser@example.com"})
    print("*********")
    print(response)
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "status": "Success",
        "data": {
            "id": "464645645",
            "status": "Succeeded"
        }
    }

# Method to test getBenchmarkStatus with 400 response
def test_getBenchmarkStatus():
    response = client.get("/benchmarks/6b543a2350c", headers={"accept": "application/json", "userId":"testuser@example.com"})
    print("*********")
    print(response)
    assert response.status_code == 400
    assert response.json() == {
        "code": 2835,
        "status": "FAILURE",
        "status": "Benchmark not found"
    }