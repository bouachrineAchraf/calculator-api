from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_calculation():
    expression = "5 3 +"
    response = client.post(f"/calculations/{expression}")
    assert response.status_code == 201
    data = response.json()
    assert "expression" in data
    assert "result" in data
    assert data["expression"] == expression
    assert isinstance(data["result"], str)


