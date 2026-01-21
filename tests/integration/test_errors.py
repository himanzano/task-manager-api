from fastapi import APIRouter
from fastapi.testclient import TestClient
from app.main import app

# We need to import the app to mount a route, but for testing 500s with TestClient,
# we need raise_server_exceptions=False.

def test_validation_error_structure(client: TestClient):
    # Missing required field 'email'
    response = client.post("/auth/register", json={"password": "short"})
    assert response.status_code == 422
    data = response.json()
    assert "message" in data
    assert "details" in data
    assert data["message"] == "Validation error"
    assert isinstance(data["details"], list)
    assert data["details"][0]["field"] == "body.email"

def test_http_exception_structure_404(client: TestClient, auth_headers: dict):
    response = client.get("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert "message" in data
    assert data["message"] == "Task not found"
    # details can be None for simple HTTPExceptions
    assert "details" in data 

def test_http_exception_structure_401(client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 401
    data = response.json()
    assert "message" in data
    assert data["message"] == "Not authenticated"

def test_unhandled_exception_500():
    # Create a router that raises an exception
    router = APIRouter()
    
    @router.get("/force-error")
    def force_error():
        raise ValueError("Boom!")
    
    app.include_router(router)
    
    # Create a client that suppresses exceptions so we can check the 500 response
    with TestClient(app, raise_server_exceptions=False) as error_client:
        response = error_client.get("/force-error")
        assert response.status_code == 500
        data = response.json()
        assert data["message"] == "Internal server error"
        assert "stack_trace" not in data