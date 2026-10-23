"""In-process adapter checks. These do NOT substitute for running-server system tests."""
import json
import logging
from uuid import UUID, uuid4
from fastapi.testclient import TestClient
import pytest
from reference.api import make_app
from reference.domain import DependencyUnavailable
from reference.memory import MemoryStore

ALICE = "a" * 40
BOB = "b" * 40

@pytest.fixture
def client():
    return TestClient(make_app(MemoryStore(), stage="07", auth_tokens={ALICE: "lab-alice", BOB: "lab-bob"}))

def auth(token=ALICE):
    return {"Authorization": f"Bearer {token}"}

def error(response, status, code):
    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert response.json()["request_id"] == response.headers["x-request-id"]
    UUID(response.headers["x-request-id"])


def test_complete_contract_and_ownership(client):
    response = client.post("/tasks", json={"title": "  Ship  "}, headers=auth())
    assert response.status_code == 201
    task = response.json()
    path = response.headers["location"]
    assert task["title"] == "Ship"
    assert task["completed"] is False and task["completed_at"] is None
    assert set(task) == {"id", "title", "completed", "created_at", "completed_at"}
    assert client.get(path, headers=auth()).json() == task
    assert client.get("/tasks", headers=auth(BOB)).json() == {"items": []}
    error(client.get(path, headers=auth(BOB)), 404, "TASK_NOT_FOUND")
    error(client.post(path + "/complete", headers=auth(BOB)), 404, "TASK_NOT_FOUND")
    assert client.get(path, headers=auth()).json() == task
    done = client.post(path + "/complete", headers=auth()).json()
    assert done["completed"] is True and done["completed_at"].endswith("Z")
    assert client.post(path + "/complete", headers=auth()).json() == done
    assert client.get(path, headers=auth()).json() == done

@pytest.mark.parametrize("headers", [{}, auth("invalid"), {"Authorization": "Basic abc"}])
def test_auth_failure(client, headers):
    response = client.get("/tasks", headers=headers)
    error(response, 401, "UNAUTHENTICATED")
    assert response.headers["www-authenticate"] == "Bearer"

@pytest.mark.parametrize("body", [{"title": ""}, {"title": " "}, {"title": "x" * 121}, {"title": 1}, {"title": None}, {"title": []}, {"title": "x", "owner_id": "bob"}, []])
def test_validation(client, body):
    error(client.post("/tasks", json=body, headers=auth()), 422, "VALIDATION_ERROR")


def test_unknown_and_malformed_ids(client):
    error(client.get("/tasks/not-a-uuid", headers=auth()), 422, "VALIDATION_ERROR")
    error(client.get(f"/tasks/{uuid4()}", headers=auth()), 404, "TASK_NOT_FOUND")


def test_empty_completion_body(client):
    path = client.post("/tasks", json={"title": "x"}, headers=auth()).headers["location"]
    error(client.post(path + "/complete", json={}, headers=auth()), 422, "VALIDATION_ERROR")
    assert client.get(path, headers=auth()).json()["completed"] is False


def test_logs_have_no_raw_path_title_or_credentials(client, caplog):
    with caplog.at_level(logging.INFO, logger="taskboard.requests"):
        response = client.post("/tasks?secret=never-log-this", json={"title": "private-title"},
                               headers={**auth(), "X-Request-ID": "forged-identifier"})
    assert "never-log-this" not in caplog.text and "private-title" not in caplog.text and ALICE not in caplog.text
    assert "forged-identifier" not in caplog.text
    record = json.loads(caplog.records[-1].message)
    assert record["request_id"] == response.headers["x-request-id"]
    assert record["path"] == "/tasks" and record["status"] == 201


@pytest.mark.parametrize("exception,status,code", [(DependencyUnavailable("secret-dsn"), 503, "DEPENDENCY_UNAVAILABLE"), (RuntimeError("secret-dsn"), 500, "INTERNAL_ERROR")])
def test_sanitized_failures(exception, status, code):
    class BrokenStore(MemoryStore):
        async def list(self, owner):
            raise exception
    client = TestClient(make_app(BrokenStore(), stage="03"), raise_server_exceptions=False)
    response = client.get("/tasks")
    error(response, status, code)
    assert "secret-dsn" not in response.text
    assert client.get("/livez").status_code == 200


def test_tokens_must_be_distinct_and_long():
    with pytest.raises(RuntimeError):
        make_app(MemoryStore(), stage="07", auth_tokens={"short": "alice", "also-short": "bob"})
