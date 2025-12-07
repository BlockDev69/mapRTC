import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_redis_acess(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"redis": "connected", "status": "healthy"}

def test_create_session(client):
    response = client.post("/session/init")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data and data["status"] == "Session initialized"
    assert "user_id" in data

# 422 UNPROCESSABLE ENTITY ISSUE
def test_verifier_session_with_valid_id(client):
    init_response = client.post("/session/init")
    assert init_response.status_code == 200
    cookie_value = init_response.cookies.get("anon_session_id")
    assert cookie_value is not None

    # response = client.get("/session/me", cookies={"anon_session_id": cookie_value})
    client.cookies.set("anon_session_id", cookie_value)
    response = client.get("/session/me")
    print("Status Code:", response.status_code)
    print("Response", response.text)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data

# NOT FINISHED
def test_verifier_session_without_valid_id(client):
    reponse = client.get("/session/me")
    assert reponse.status_code == 200
    pass