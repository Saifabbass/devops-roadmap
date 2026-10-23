"""Operate ONLY the bundled disposable Compose project; prove restarts and a DB outage."""
import json
import subprocess
import time
from pathlib import Path
from uuid import uuid4
import httpx
ROOT = Path(__file__).resolve().parents[1]
ENV = dict(line.split("=", 1) for line in (ROOT / ".env").read_text().splitlines() if line and not line.startswith("#"))
if ENV.get("TASKBOARD_STAGE") != "07":
    raise SystemExit("Use TASKBOARD_STAGE=07 for the authenticated lifecycle drill")
COMPOSE = ["docker", "compose", "--project-name", "devopps-taskboard", "--file", str(ROOT / "compose.yaml")]

def compose(*args):
    subprocess.run(COMPOSE + list(args), cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

def wait_ready(client):
    for attempt in range(30):
        try:
            if client.get("/readyz").status_code == 200:
                return
        except httpx.RequestError:
            pass
        time.sleep(1)
    raise AssertionError("Application not ready within bounded retry window")

with httpx.Client(base_url="http://127.0.0.1:8000", timeout=5,
                  headers={"Authorization": "Bearer " + ENV["LAB_ALICE_TOKEN"]}) as client:
    wait_ready(client)
    response = client.post("/tasks", json={"title": "Persistence " + uuid4().hex})
    assert response.status_code == 201
    path = response.headers["location"]
    completed = client.post(path + "/complete").json()
    for component in ("app", "db"):
        compose("restart", component)
        wait_ready(client)
        assert client.get(path).json() == completed
        print(f"PASS: committed task survives {component} restart")
    try:
        compose("stop", "db")
        started = time.monotonic()
        failure = client.get(path)
        elapsed = time.monotonic() - started
        assert failure.status_code == 503 and failure.json()["error"]["code"] == "DEPENDENCY_UNAVAILABLE"
        assert elapsed < 5, f"Failure took {elapsed:.2f}s; required less than 5s"
        assert client.get("/readyz").status_code == 503
        assert client.get("/livez").json() == {"status": "ok"}
        print(f"PASS: task 503 in {elapsed:.2f}s; readiness 503; liveness 200")
    finally:
        compose("start", "db")
        wait_ready(client)
    assert client.get(path).json() == completed
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports" / "lifecycle.json").write_text(json.dumps({"task_id": completed["id"],
    "app_restart": "passed", "db_restart": "passed", "outage_seconds": round(elapsed, 3)}, indent=2))
