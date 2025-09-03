from ...src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def create_test_user():
    data = {"name":"Test User", "email":"testuser@example.com"}
    response = client.post("/auth/register/", json=data)
    assert response.status_code == 201
    return data

def get_auth_token(email, password):
    response = client.post("/auth/login/", data={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_get_current_profile():
    
    creds = create_test_user()
    
    token = get_auth_token(creds["email"], creds["password"])
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == creds["email"]
    assert "id" in data
    assert data["is_active"] is True

def test_get_current_profile_unauthorized():
    response = client.get("/me")
    assert response.status_code == 401