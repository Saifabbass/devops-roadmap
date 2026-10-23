import os
from uuid import UUID, uuid4
import pytest


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert response.json()["request_id"] == response.headers["x-request-id"]
    UUID(response.headers["x-request-id"])


def create(client, headers, title):
    response = client.post("/tasks", json={"title": title}, headers=headers)
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == title.strip()  # Intentionally catches 200/201 with the wrong body.
    assert task["completed"] is False and task["completed_at"] is None
    assert set(task) == {"id", "title", "completed", "created_at", "completed_at"}
    assert task["created_at"].endswith("Z")
    assert response.headers["location"] == f"/tasks/{task['id']}"
    return task


def test_positive_path(client, alice):
    title = "System test " + uuid4().hex
    task = create(client, alice, "  " + title + "  ")
    path = f"/tasks/{task['id']}"
    assert client.get(path, headers=alice).json() == task
    items = client.get("/tasks", headers=alice).json()["items"]
    assert task in items
    assert items == sorted(items, key=lambda item: (item["created_at"], item["id"]))
    done = client.post(path + "/complete", headers=alice)
    assert done.status_code == 200
    data = done.json()
    assert data["completed"] is True and data["completed_at"].endswith("Z")
    assert client.post(path + "/complete", headers=alice).json() == data
    assert client.get(path, headers=alice).json() == data


def test_authentication_and_ownership(client, alice, bob):
    for headers in ({}, {"Authorization": "Bearer invalid"}):
        response = client.get("/tasks", headers=headers)
        assert_error(response, 401, "UNAUTHENTICATED")
        assert response.headers["www-authenticate"] == "Bearer"
    a = create(client, alice, "Alice " + uuid4().hex)
    b = create(client, bob, "Bob " + uuid4().hex)
    assert b not in client.get("/tasks", headers=alice).json()["items"]
    assert a not in client.get("/tasks", headers=bob).json()["items"]
    path = f"/tasks/{a['id']}"
    assert_error(client.get(path, headers=bob), 404, "TASK_NOT_FOUND")
    assert_error(client.post(path + "/complete", headers=bob), 404, "TASK_NOT_FOUND")
    assert client.get(path, headers=alice).json() == a

@pytest.mark.parametrize("body", [{"title": ""}, {"title": " "}, {"title": 3}, {"title": None}, {"title": []}, {"title": "x" * 121}, {"title": "x", "owner_id": "lab-bob"}])
def test_invalid_input(client, alice, body):
    assert_error(client.post("/tasks", json=body, headers=alice), 422, "VALIDATION_ERROR")


def test_uuid_errors(client, alice):
    assert_error(client.get("/tasks/invalid", headers=alice), 422, "VALIDATION_ERROR")
    assert_error(client.get(f"/tasks/{uuid4()}", headers=alice), 404, "TASK_NOT_FOUND")


def test_health_and_version(client):
    assert client.get("/livez").json() == {"status": "ok"}
    version = client.get("/version").json()
    assert version["api_contract"] == "1.0" and "git_sha" in version
    if os.getenv("TASKBOARD_TEST_MODE") != "memory":
        assert client.get("/readyz").json() == {"status": "ready"}
