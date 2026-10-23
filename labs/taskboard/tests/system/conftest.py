"""Black-box calls to a real listener. No app import and no in-process test client."""
import os
from urllib.parse import urlparse
import httpx
import pytest

@pytest.fixture(scope="session")
def client():
    url = os.getenv("TASKBOARD_BASE_URL")
    if not url:
        pytest.fail("Set TASKBOARD_BASE_URL to your running disposable service; see README")
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "app"}:
        pytest.fail("System suite only targets the local disposable lab, never arbitrary/public hosts")
    with httpx.Client(base_url=url, timeout=5.0) as client:
        yield client

@pytest.fixture(scope="session")
def alice():
    if os.getenv("TASKBOARD_TEST_MODE") == "memory":
        return {}
    token = os.getenv("LAB_ALICE_TOKEN")
    if not token:
        pytest.fail("LAB_ALICE_TOKEN is required for authenticated system tests")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def bob():
    if os.getenv("TASKBOARD_TEST_MODE") == "memory":
        pytest.skip("Stage 03 intentionally has no authentication; use stage 07 to prove isolation")
    token = os.getenv("LAB_BOB_TOKEN")
    if not token:
        pytest.fail("LAB_BOB_TOKEN is required for authenticated system tests")
    return {"Authorization": f"Bearer {token}"}
