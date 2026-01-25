from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User


def test_update_task_invalid_field(
    client: TestClient, auth_headers: dict, db_session: Session, test_user: User
):
    # Create a task
    task = Task(title="Original Title", owner_id=test_user.id)
    db_session.add(task)
    db_session.commit()

    # Attempt update with invalid field 'completed' and missing 'title'
    response = client.put(
        f"/tasks/{task.id}",
        json={"completed": True},
        headers=auth_headers,
    )

    # Should be 422 due to validation error
    assert response.status_code == 422
    data = response.json()
    assert data["message"] == "Validation error"

    # Check details for specific errors
    details = data["details"]
    # We expect errors for:
    # 1. Missing 'title'
    # 2. Extra field 'completed'

    fields = [err["field"] for err in details]
    messages = [err["message"] for err in details]

    assert "body.title" in fields
    assert "body.completed" in fields
    assert "Field required" in messages
    assert "Extra inputs are not permitted" in messages
