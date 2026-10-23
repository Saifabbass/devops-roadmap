"""A bounded readiness wait used in CI; no arbitrary sleeps as proof of health."""
import os
import time
import urllib.request
url = os.getenv("TASKBOARD_BASE_URL", "http://app:8000") + "/readyz"
for attempt in range(30):
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status == 200:
                print("Application ready")
                break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit("Application readiness deadline expired")
