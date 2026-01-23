from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.core import security
from app.models.task import Task, TaskStatus
from app.models.user import User

def test_create_task_success(client: TestClient, auth_headers: dict):
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Do something"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Do something"
    assert data["status"] == "TODO"
    assert "id" in data
    assert "owner_id" in data

def test_create_task_missing_fields(client: TestClient, auth_headers: dict):
    response = client.post(
        "/tasks",
        json={"description": "Missing title"},
        headers=auth_headers,
    )
    assert response.status_code == 422

def test_create_task_ignores_owner_id(client: TestClient, auth_headers: dict):
    # Attempt to inject a different owner_id
    response = client.post(
        "/tasks",
        json={"title": "Task", "owner_id": 999},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    # verify the owner_id was ignored/overwritten by the current user's id
    # We can't easily check the exact ID here without querying the user from DB,
    # but we know it shouldn't be 999 unless the test user has ID 999 (unlikely).
    assert data["owner_id"] != 999

def test_read_tasks_own_only(
    client: TestClient, auth_headers: dict, db_session: Session, test_user: User
):
    # Create task for current user
    task1 = Task(title="My Task", owner_id=test_user.id)
    db_session.add(task1)
    
    # Create another user and their task
    other_user = User(
        email="other@example.com",
        hashed_password=security.get_password_hash("pass"),
    )
    db_session.add(other_user)
    db_session.commit()
    
    task2 = Task(title="Other Task", owner_id=other_user.id)
    db_session.add(task2)
    db_session.commit()

    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "My Task"

def test_read_tasks_pagination(client: TestClient, auth_headers: dict, db_session: Session, test_user: User):
    # Create 15 tasks
    for i in range(15):
        db_session.add(Task(title=f"Task {i}", owner_id=test_user.id))
    db_session.commit()

    # Default limit is 10
    response = client.get("/tasks", headers=auth_headers)
    assert len(response.json()) == 10

    # Limit 5, offset 0
    response = client.get("/tasks?limit=5&offset=0", headers=auth_headers)
    assert len(response.json()) == 5
    assert response.json()[0]["title"] == "Task 0"

    # Limit 5, offset 5
    response = client.get("/tasks?limit=5&offset=5", headers=auth_headers)
    assert len(response.json()) == 5
    assert response.json()[0]["title"] == "Task 5"

def test_read_task_success(client: TestClient, auth_headers: dict, db_session: Session, test_user: User):
    task = Task(title="My Task", owner_id=test_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My Task"

def test_read_task_not_found(client: TestClient, auth_headers: dict):
    response = client.get(f"/tasks/{uuid.uuid4()}", headers=auth_headers)
    assert response.status_code == 404

def test_read_task_other_owner_404(
    client: TestClient, auth_headers: dict, db_session: Session
):
    other_user = User(
        email="other@example.com",
        hashed_password=security.get_password_hash("pass"),
    )
    db_session.add(other_user)
    db_session.commit()
    
    task = Task(title="Other Task", owner_id=other_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404

def test_update_task_success(client: TestClient, auth_headers: dict, db_session: Session, test_user: User):
    task = Task(title="Old Title", owner_id=test_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "New Title", "status": "IN_PROGRESS"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "IN_PROGRESS"

def test_update_task_other_owner_404(
    client: TestClient, auth_headers: dict, db_session: Session
):
    other_user = User(
        email="other@example.com",
        hashed_password=security.get_password_hash("pass"),
    )
    db_session.add(other_user)
    db_session.commit()
    
    task = Task(title="Other Task", owner_id=other_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "Hacked Title"},
        headers=auth_headers,
    )
    assert response.status_code == 404

def test_delete_task_success(client: TestClient, auth_headers: dict, db_session: Session, test_user: User):
    task = Task(title="To Delete", owner_id=test_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.delete(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404

def test_delete_task_other_owner_404(
    client: TestClient, auth_headers: dict, db_session: Session
):
    other_user = User(
        email="other@example.com",
        hashed_password=security.get_password_hash("pass"),
    )
    db_session.add(other_user)
    db_session.commit()
    
    task = Task(title="Other Task", owner_id=other_user.id)
    db_session.add(task)
    db_session.commit()

    response = client.delete(f"/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404
