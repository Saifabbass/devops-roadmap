"""Bounded DB service wait for an ephemeral CI job; does not apply migrations."""
import time
import psycopg

def wait(dsn):
    for attempt in range(20):
        try:
            with psycopg.connect(dsn, connect_timeout=2) as conn:
                conn.execute("SELECT 1")
            return
        except psycopg.OperationalError:
            time.sleep(1)
    raise SystemExit("PostgreSQL did not become reachable within the startup window")
