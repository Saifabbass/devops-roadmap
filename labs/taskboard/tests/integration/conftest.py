"""Only a database with the explicit taskboard_test name may be modified."""
import os
from uuid import uuid4
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict
import pytest
from reference.migrate import apply
from reference.postgres import PostgresStore, OPTIONS

@pytest.fixture
def database():
    dsn = os.getenv("TEST_DATABASE_URL")
    if not dsn:
        pytest.fail("Set TEST_DATABASE_URL to the disposable taskboard_test database; see README")
    config = conninfo_to_dict(dsn)
    if config.get("dbname") != "taskboard_test" or config.get("host") not in {"127.0.0.1", "localhost", "test-db", "postgres"}:
        pytest.fail("Refusing integration tests: require taskboard_test on a documented local/CI host")
    schema = "test_" + uuid4().hex
    with psycopg.connect(dsn, connect_timeout=2, options=OPTIONS) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    try:
        yield dsn, schema
    finally:
        # Drop only this random schema in the explicitly guarded test database.
        with psycopg.connect(dsn, connect_timeout=2, options=OPTIONS) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))

@pytest.fixture
def store(database):
    dsn, schema = database
    apply(dsn, schema)
    return PostgresStore(dsn, schema)
