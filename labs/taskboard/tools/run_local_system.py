"""Start an actual memory-mode listener, test over HTTP, then stop only that child."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
ROOT = Path(__file__).resolve().parents[1]
with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
url = f"http://127.0.0.1:{port}"
(ROOT / "reports").mkdir(exist_ok=True)
with (ROOT / "reports" / "local-server.log").open("w", encoding="utf-8") as log:
    process = subprocess.Popen([sys.executable, "-m", "uvicorn", "reference.stage03:app",
        "--host", "127.0.0.1", "--port", str(port), "--no-access-log"], cwd=ROOT, stdout=log, stderr=log)
    try:
        for attempt in range(100):
            if process.poll() is not None:
                raise SystemExit("Server exited; inspect reports/local-server.log")
            try:
                with urllib.request.urlopen(url + "/livez", timeout=1):
                    break
            except OSError:
                time.sleep(0.1)
        else:
            raise SystemExit("Server did not become ready within 10 seconds")
        env = {**os.environ, "TASKBOARD_BASE_URL": url, "TASKBOARD_TEST_MODE": "memory"}
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/system", "-q",
                                 "--junitxml=reports/system-memory.xml"], cwd=ROOT, env=env)
        raise SystemExit(result.returncode)
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
