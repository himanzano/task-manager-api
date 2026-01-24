from fastapi.testclient import TestClient
import time


def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "newpassword"},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Email already registered"


def test_login_success(client: TestClient):
    # Create user first
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect email or password"


def test_login_non_existent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect email or password"


def test_refresh_token_success(client: TestClient):
    # Register and login
    client.post(
        "/auth/register",
        json={"email": "refresh@example.com", "password": "password123"},
    )
    login_res = client.post(
        "/auth/login",
        json={"email": "refresh@example.com", "password": "password123"},
    )
    refresh_token = login_res.json()["refresh_token"]

    time.sleep(2)
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != login_res.json()["access_token"]


def test_refresh_token_invalid(client: TestClient):
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token_string"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Could not validate credentials"
