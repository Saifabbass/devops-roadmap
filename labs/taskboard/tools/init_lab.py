"""Generate lab credentials locally, never print them, never overwrite existing ones."""
from pathlib import Path
import os
import secrets
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / ".env"
values = {"TASKBOARD_STAGE": "07", "POSTGRES_PASSWORD": secrets.token_hex(24),
          "TEST_DB_PASSWORD": secrets.token_hex(24), "LAB_ALICE_TOKEN": secrets.token_urlsafe(32),
          "LAB_BOB_TOKEN": secrets.token_urlsafe(32)}
try:
    # O_EXCL refuses replacement; 0o600 limits access on Linux.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    raise SystemExit(".env already exists; kept it unchanged. Continue with the existing lab credentials.")
with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as file:
    file.write("".join(f"{key}={value}\n" for key, value in values.items()))
print("Created .env for this disposable local lab. No credentials printed.")
