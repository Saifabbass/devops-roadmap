"""Backup + restore into a NEW database; never overwrite source or an existing database."""
import json
from pathlib import Path
import subprocess
from uuid import uuid4
ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ["docker", "compose", "--project-name", "devopps-taskboard", "--file", str(ROOT / "compose.yaml")]
restore_db = "taskboard_restore_" + uuid4().hex[:12]

def pg(*args, input=None):
    result = subprocess.run(COMPOSE + ["exec", "-T", "db", *args], cwd=ROOT,
                            input=input, capture_output=True)
    if result.returncode:
        raise SystemExit("Database command failed; inspect the private local lab. Source database was not overwritten.")
    return result.stdout

query = "SELECT row_to_json(t) FROM (SELECT id, owner_id, title, completed, created_at, completed_at FROM tasks ORDER BY id) t"
backup = pg("pg_dump", "-U", "taskboard", "-d", "taskboard", "--format=custom", "--no-owner", "--no-privileges")
expected = pg("psql", "-U", "taskboard", "-d", "taskboard", "-At", "-c", query)
# No drop/reuse path exists: createdb must succeed for this new random name.
pg("createdb", "-U", "taskboard", restore_db)
pg("pg_restore", "-U", "taskboard", "-d", restore_db, "--exit-on-error", "--no-owner", "--no-privileges", input=backup)
actual = pg("psql", "-U", "taskboard", "-d", restore_db, "-At", "-c", query)
assert actual == expected, "Restored IDs, owners, titles or completion values differ"
count = len(actual.splitlines())
assert count > 0, "Seed at least one task before testing restoration"
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports" / "restore.json").write_text(json.dumps({"database": restore_db,
    "rows": count, "all_task_fields_match": True}, indent=2))
print(f"PASS: {count} rows match all six stored fields in {restore_db}.")
print("Restore database deliberately retained for inspection; see README for explicit scoped cleanup.")
