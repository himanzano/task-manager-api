from fastapi.testclient import TestClient
from app.core import security

def test_read_users_me_success(client: TestClient):
    # Register and login
    client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "password123"},
    )
    login_res = client.post(
        "/auth/login",
        json={"email": "me@example.com", "password": "password123"},
    )
    access_token = login_res.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

def test_read_users_me_missing_token(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_read_users_me_invalid_token(client: TestClient):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
