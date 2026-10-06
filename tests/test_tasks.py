from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Testing task creation"
    assert data["completed"] is False


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Update Test",
            "description": "Before update",
        },
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Test",
            "description": "This task will be deleted",
        },
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
