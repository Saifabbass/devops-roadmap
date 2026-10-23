"""Explicit migration command; startup checks readiness but never silently migrates."""
import hashlib
import os
from pathlib import Path

import psycopg
from psycopg import sql
from reference.postgres import OPTIONS, schema_name

MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"


def apply(dsn, schema="public", through=None):
    with psycopg.connect(dsn, connect_timeout=2, options=OPTIONS) as conn:
        conn.execute(sql.SQL("SET LOCAL search_path TO {}").format(sql.Identifier(schema)))
        conn.execute("SELECT pg_advisory_xact_lock(54738291)")
        conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations ("
                     "version integer PRIMARY KEY, sha256 text NOT NULL, "
                     "applied_at timestamptz NOT NULL DEFAULT clock_timestamp())")
        applied = dict(conn.execute("SELECT version, sha256 FROM schema_migrations").fetchall())
        for file in sorted(MIGRATIONS.glob("[0-9][0-9][0-9]_*.sql")):
            version = int(file.name.split("_")[0])
            if through is not None and version > through:
                continue
            content = file.read_text(encoding="utf-8")
            checksum = hashlib.sha256(content.encode()).hexdigest()
            if version in applied:
                if applied[version] != checksum:
                    raise RuntimeError("An applied migration changed; restore the original file")
                continue
            conn.execute(content)
            conn.execute("INSERT INTO schema_migrations (version, sha256) VALUES (%s,%s)", (version, checksum))
    # Context manager commits all changes or rolls them all back on an exception.


if __name__ == "__main__":
    try:
        apply(os.environ["DATABASE_URL"], schema_name())
    except Exception:
        raise SystemExit("Migration failed. No partial migration committed. Check private database/configuration evidence.")
    print("Schema is at version 2; existing migration checksums match.")
